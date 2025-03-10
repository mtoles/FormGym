from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
import os
import requests
from prompt import get_prompt

# model_id = "llava-hf/llava-1.5-7b-hf"
model_id = "llava-hf/llava-1.5-13b-hf"

model = LlavaForConditionalGeneration.from_pretrained(
    model_id, 
    torch_dtype=torch.float16, 
    low_cpu_mem_usage=True,
    cache_dir='/local/data/rds_hf_cache',
    # load_in_4bit=True,
    # use_flash_attention_2=True
).to(0)

processor = AutoProcessor.from_pretrained(model_id)

local_image_path = "../processed_pngs/grid_al_1_page_1.png"
prompt_text = get_prompt(local_image_path)

conversation = [
    {

      "role": "user",
      "content": [
          {"type": "text", "text": prompt_text},
          {"type": "image"},
        ],
    },
]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

raw_image = Image.open(local_image_path)
inputs = processor(images=raw_image, text=prompt, return_tensors='pt').to(0, torch.float16)

output = model.generate(**inputs, max_new_tokens=500, do_sample=False)
print(processor.decode(output[0][2:], skip_special_tokens=True))