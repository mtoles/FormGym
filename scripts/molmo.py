from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from prompt import get_prompt, parse_json_from_response, encode_image
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import requests

processor = AutoProcessor.from_pretrained(
    'allenai/Molmo-7B-D-0924',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)

model = AutoModelForCausalLM.from_pretrained(
    'allenai/Molmo-7B-D-0924',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)

inputs = processor.process(
    images=[Image.open(requests.get("https://picsum.photos/id/237/536/354", stream=True).raw)],
    text="Describe this image."
)

inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

output = model.generate_from_batch(
    inputs,
    GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
    tokenizer=processor.tokenizer
)

generated_tokens = output[0,inputs['input_ids'].size(1):]
generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

print(generated_text)

# local_image_path = "./processed_pngs/grid_al_1_page_1.png"
# prompt_text = get_prompt(local_image_path)
# base64_image = encode_image(local_image_path)

# query = tokenizer.from_list_format([
#     {'image': f"data:image/png;base64,{base64_image}"},
#     {'text': prompt_text},
# ])