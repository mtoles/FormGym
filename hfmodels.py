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

from prompt import get_prompt, parse_and_reconstruct_fields
import json
from vllm.sampling_params import GuidedDecodingParams
from pydantic import BaseModel
import time
from vllm.distributed.parallel_state import destroy_model_parallel, destroy_distributed_environment
from torch.distributed import destroy_process_group

import gc
import torch

class BaseHFModel:
    def __init__(self):
        self.engine_args: EngineArgs = None
        self.stop_token_ids: Optional[List[int]] = None

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        """Subclasses must override this with prompt-building logic."""
        raise NotImplementedError("Subclasses must implement get_prompt()")

# ARIA Model
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

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = (
                "<|im_start|>user\n<fim_prefix><|img|><fim_suffix>"
                f"{question}"
                "<|im_end|>\n<|im_start|>assistant\n"
            )
            prompts.append(prompt)
        return prompts


class LlavaModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="llava-hf/llava-1.5-7b-hf",
            max_model_len=4096,
        )
        self.stop_token_ids = None  # LLaVA might not need special stop tokens

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = f"USER: <image>\n{question}\nASSISTANT:"
            prompts.append(prompt)
        return prompts

class MolmoModel(BaseHFModel):
    def __init__(self):
        super().__init__()
        self.engine_args = EngineArgs(
            model="allenai/Molmo-7B-D-0924",
            trust_remote_code=True,
            dtype="bfloat16",
        )
        self.stop_token_ids = None

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = (
                f"<|im_start|>user <image>\n{question}<|im_end|> "
                "<|im_start|>assistant\n"
            )
            prompts.append(prompt)

        return prompts

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

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = f"{question}Picture 1: <img></img>\n"
            prompts.append(prompt)

        return prompts

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

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = f"<|User|>: <image>\n{question}\n\n<|Assistant|>:"
            prompts.append(prompt)

        return prompts

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

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        prompts = []
        for image in images:
            question = get_prompt(image)
            prompt = (
                "<bos><start_of_turn>user\n"
                f"<start_of_image>{question}<end_of_turn>\n"
                "<start_of_turn>model\n"
            )
            prompts.append(prompt)

        return prompts

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
            self.engine_args.model,
            trust_remote_code=self.engine_args.trust_remote_code
        )

    def get_prompt(self, images: List[Image.Image]) -> List[str]:
        questions = []
        for image in images:
            question = get_prompt(image)
            questions.append(question)

        messages = [
            [{
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": question}
                ]
            }]
            for question in questions
        ]

        prompts = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False
        )

        return prompts
    
# HF E2E Class
class HFE2EModel:
    def __init__(self, model_name: str, download_dir: str = "/local/data/rs4478/vllm_cache", seed=None):
        model_registry = {
            "aria": AriaModel,
            "llava": LlavaModel,
            "molmo": MolmoModel, 
            "qwen_vl": QwenVLModel,
            "deepseek_vl2": DeepseekVL2Model,
            "gemma3": Gemma3Model,
            "mllama": MLLamaModel,
            # add more models here (MyFancyModel, etc.)
        }

        if model_name not in model_registry:
            raise ValueError(f"Unsupported model: {model_name}")

        self.model = model_registry[model_name]()

        engine_args_dict = asdict(self.model.engine_args)
        engine_args_dict["download_dir"] = download_dir
        engine_args_dict["seed"] = seed
        # Argument for multiple GPUs
        # engine_args_dict["tensor_parallel_size"] = 4

        self.llm = LLM(**engine_args_dict)

        self.sampling_params = SamplingParams(
            temperature=0.2,
            max_tokens=64,
            stop_token_ids=self.model.stop_token_ids,
        )

        self.model_name = model_name

    def forward(self, images: List[Image.Image]):
        prompts = self.model.get_prompt(images)

        all_inputs = []
        for img, prompt in zip(images, prompts):
            all_inputs.append(
                {
                    "prompt": prompt,
                    "multi_modal_data": {"image": img},
                }
            )

        start_time = time.time()
        outputs = self.llm.generate(all_inputs, sampling_params=self.sampling_params)
        elapsed_time = time.time() - start_time
        print(f"[HFE2EModel.forward] Generation time: {elapsed_time:.2f} s")
        return outputs
    
    def cleanup(self):
        destroy_model_parallel()
        destroy_distributed_environment()
        destroy_process_group()
        
        if hasattr(self, 'llm') and hasattr(self.llm, 'llm_engine'):
            if hasattr(self.llm.llm_engine, 'driver_worker'):
                del self.llm.llm_engine.driver_worker

        if hasattr(self, 'llm'):
            del self.llm

        gc.collect()
        torch.cuda.empty_cache()

        if torch.distributed.is_initialized():
            torch.distributed.destroy_process_group()

        print("Successfully deleted the llm pipeline and freed the GPU memory!")

    
def main():
    # 1) List all the models you want to run
    models = ["deepseek_vl2"]
    
    # 2) Folder containing your PNG images
    png_folder = "./pngs"
    # 3) Output folder
    output_root = "./output"

    # 4) Find all .png files
    png_files = [f for f in os.listdir(png_folder) if f.lower().endswith(".png")]
    png_files.sort()  # optional, if you want sorted order

    # 5) Convert each .png into a PIL Image
    images = []
    for filename in png_files:
        path = os.path.join(png_folder, filename)
        img = Image.open(path).convert("RGB")
        images.append(img)

    # 6) For each model in the list of models:
    for model_name in models:
        print(f"\n{'='*60}")
        print(f"Running model: {model_name}")
        print(f"{'='*60}\n")

        # Create an instance of HFE2EModel for this model
        model = HFE2EModel(model_name=model_name)

        # 7) Generate outputs for all images in a single forward pass
        start_time = time.time()
        outputs = model.forward(images)
        elapsed_time = time.time() - start_time
        print(f"[Timing] {model_name}: Generation took {elapsed_time:.2f}s")

        # 8) Process each output + image, and save to the desired directory structure
        for i, out in enumerate(outputs):
            # raw text from the LLM
            raw_text = out.outputs[0].text

            # parse the text into a structured format (dict, list, etc.)
            parsed_response = parse_and_reconstruct_fields(raw_text)
            parsed_output_json = json.dumps(parsed_response, indent=2)

            # image filename (without extension)
            image_name = os.path.splitext(png_files[i])[0]

            # create directory: ./output/{model_name}/{image_name}
            save_dir = os.path.join(output_root, model_name, image_name)
            os.makedirs(save_dir, exist_ok=True)

            # write the raw response
            raw_response_path = os.path.join(save_dir, "raw_response.txt")
            with open(raw_response_path, "w", encoding="utf-8") as f:
                f.write(raw_text)

            # write the parsed response
            parsed_response_path = os.path.join(save_dir, "parsed_response.txt")
            with open(parsed_response_path, "w", encoding="utf-8") as f:
                f.write(parsed_output_json)

            # Print to stdout as well (optional)
            print(f"\n=== Output for {png_files[i]} (Model: {model_name}) ===")
            print(raw_text)
            print("\nParsed Output:")
            print(parsed_output_json)
            print()

        # 9) Cleanup model resources before loading the next model
        # model.cleanup()

if __name__ == "__main__":
    main()

#https://chatgpt.com/c/67e8cd1a-3acc-8002-bb9c-865e7acad4c4?model=o1