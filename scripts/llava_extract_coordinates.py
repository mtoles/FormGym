from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from huggingface_hub import login
import os

# login(token='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')
# os.environ['HF_HOME'] = '/local/data/rds_hf_cache'

# Set up model and processor
model_id = "llava-hf/llava-1.5-7b-hf"
model = LlavaForConditionalGeneration.from_pretrained(
    model_id, 
    torch_dtype=torch.float16, 
    low_cpu_mem_usage=True,
    cache_dir='/local/data/rds_hf_cache',
    # load_in_4bit=True,
    # use_flash_attention_2=True
).to(0)
processor = AutoProcessor.from_pretrained(model_id)

# Local image path in the same folder
local_image_path = "../processed_pngs/grid_al_1_page_1.png"

# Define a conversation with the local image
conversation = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What are these?"},
            {"type": "image", "image_path": local_image_path},  # Use image_path for local files
        ],
    },
]

# Process the conversation
inputs = processor.apply_chat_template(
    conversation, 
    add_generation_prompt=True,
    tokenize=True,
    return_tensors="pt",
    return_dict=True
).to(0, torch.float16)

# Generate output
output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
print(processor.decode(output[0][2:], skip_special_tokens=True))