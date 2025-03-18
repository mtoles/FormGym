from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from prompt import get_prompt, parse_json_from_response, encode_image, parse_and_reconstruct_fields
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
import json

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct", 
    device_map="auto", 
    load_in_8bit=True,       
)

processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
)

local_image_path = "./processed_pngs/grid_al_1_page_1.png"
prompt_text = get_prompt(local_image_path)
base64_image = encode_image(local_image_path)

conversation = [
    {
        "role":"user",
        "content":[
            {
                "type":"image",
                "url": f"data:image/png;base64,{base64_image}"
            },
            {
                "type":"text",
                "text":prompt_text
            }
        ]
    }
]

inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)

output_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
raw_response = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
raw_response = raw_response[0]

parsed_response = parse_and_reconstruct_fields(raw_response)
parsed_output = json.dumps(parsed_response, indent=2)

print(parsed_output)

with open("output_qwen2vl.txt", "w") as f:
    f.write(raw_response)

with open("output_qwen2vl_parsed.txt", "w") as f:
    f.write(parsed_output)