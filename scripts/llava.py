from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from prompt import get_prompt, parse_json_from_response, parse_and_reconstruct_fields
import json

# model_id = "llava-hf/llava-1.5-7b-hf"
model_id = "llava-hf/llava-1.5-13b-hf"

model = LlavaForConditionalGeneration.from_pretrained(
    model_id, 
    torch_dtype=torch.float16, 
    low_cpu_mem_usage=True,
    cache_dir='/local/data/rds_hf_cache',
).to(0)

processor = AutoProcessor.from_pretrained(model_id)

local_image_path = "./processed_pngs/grid_al_1_page_1.png"
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

output = model.generate(**inputs, max_new_tokens=2000, do_sample=False)
raw_response = processor.decode(output[0][2:], skip_special_tokens=True)

# parsed_response = parse_json_from_response(raw_response, "ASSISTANT: ")
parsed_response = parse_and_reconstruct_fields(raw_response)
parsed_output = json.dumps(parsed_response, indent=2)

print(parsed_output)

with open("output_llava.txt", "w") as f:
    f.write(raw_response)

with open("output_llava_parsed.txt", "w") as f:
    f.write(parsed_output)