import os
import random
from dataclasses import asdict
from typing import NamedTuple, Optional, List
from PIL import Image

from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from vllm import LLM, EngineArgs, SamplingParams
from vllm.assets.image import ImageAsset
from vllm.assets.video import VideoAsset
from vllm.lora.request import LoRARequest
from vllm.utils import FlexibleArgumentParser

from prompt import parse_and_reconstruct_fields
import json
from vllm.sampling_params import GuidedDecodingParams
from pydantic import BaseModel
import time
from vllm.distributed.parallel_state import (
    destroy_model_parallel,
    destroy_distributed_environment,
)
from torch.distributed import destroy_process_group

import gc
import torch
import textwrap


class BaseHFModel:
    def __init__(self):
        self.engine_args: EngineArgs = None
        self.stop_token_ids: Optional[List[int]] = None

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        """Subclasses must override this with prompt-building logic."""
        raise NotImplementedError("Subclasses must implement get_prompt()")


class AriaModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="rhymes-ai/Aria",
            max_model_len=4096,
            max_num_seqs=2,
            dtype="bfloat16",
        )
        self.stop_token_ids = [93532, 93653, 944, 93421, 1019, 93653, 93519]

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = (
                "<|im_start|>user\n<fim_prefix><|img|><fim_suffix>"
                f"{prompt}"
                "<|im_end|>\n<|im_start|>assistant\n"
            )
            template_prompts.append(template_prompt)
        return template_prompts


class LlavaModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="llava-hf/llava-1.5-7b-hf",
            max_model_len=4096,
            max_num_seqs=2,
            ngram_prompt_lookup_max=0,
            ngram_prompt_lookup_min=0,
        )
        self.stop_token_ids = None  # LLaVA might not need special stop tokens

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = f"USER: <image>\n{prompt}\nASSISTANT:"
            template_prompts.append(template_prompt)
        return template_prompts


class MolmoModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="allenai/Molmo-7B-D-0924",
            trust_remote_code=True,
            dtype="bfloat16",
        )
        self.stop_token_ids = None

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = (
                f"<|im_start|>user <image>\n{prompt}<|im_end|> "
                "<|im_start|>assistant\n"
            )
            template_prompts.append(template_prompt)
        return template_prompts


class QwenVLModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="Qwen/Qwen-VL",
            trust_remote_code=True,
            max_model_len=1024,
            max_num_seqs=2,
            hf_overrides={"architectures": ["QwenVLForConditionalGeneration"]},
        )
        self.stop_token_ids = None

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = f"{prompt}Picture 1: <img></img>\n"
            template_prompts.append(template_prompt)
        return template_prompts


class DeepseekVL2Model(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="deepseek-ai/deepseek-vl2-tiny",
            max_model_len=4096,
            max_num_seqs=2,
            hf_overrides={"architectures": ["DeepseekVLV2ForCausalLM"]},
        )
        self.stop_token_ids = None

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = f"<|User|>: <image>\n{prompt}\n\n<|Assistant|>:"
            template_prompts.append(template_prompt)
        return template_prompts


class Gemma3Model(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="google/gemma-3-4b-it",
            max_model_len=2048,
            max_num_seqs=2,
            mm_processor_kwargs={"do_pan_and_scan": True},
        )
        self.stop_token_ids = None

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        template_prompts = []
        for prompt in base_prompts:
            prompt = textwrap.dedent(prompt).strip()
            template_prompt = (
                "<bos><start_of_turn>user\n"
                f"<start_of_image>{prompt}<end_of_turn>\n"
                "<start_of_turn>model\n"
            )
            template_prompts.append(template_prompt)
        return template_prompts


class MLLamaModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="meta-llama/Llama-3.2-90B-Vision-Instruct",
            max_model_len=4096,
            max_num_seqs=16,
        )
        self.stop_token_ids = None

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.engine_args.model, trust_remote_code=self.engine_args.trust_remote_code
        )

    def get_templated_prompts(self, base_prompts: List[str]) -> List[str]:
        messages = [
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": textwrap.dedent(p).strip()},
                    ],
                }
            ]
            for p in base_prompts
        ]

        template_prompts = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )

        return template_prompts
