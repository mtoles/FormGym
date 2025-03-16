from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from pydantic import BaseModel, Field
from typing import List
from lmformatenforcer import JsonSchemaParser
from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn

# Define the expected JSON schema using Pydantic
class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class FormField(BaseModel):
    field_name: str
    bounding_box: BoundingBox

class FormFieldsResponse(BaseModel):
    form_fields: List[FormField]

def get_image_dimensions(image_path):
    """Get the dimensions of the image."""
    with Image.open(image_path) as img:
        return img.size

def get_prompt(image_path):
    img_width, img_height = get_image_dimensions(image_path)

    prompt = f"""
    Analyze this form image and extract all form fields.
    
    YOUR RESPONSE MUST CONTAIN NOTHING BUT VALID JSON - NO EXPLANATION, NO CODE BLOCKS, NO MARKDOWN.
    
    Format your entire response as this exact JSON structure:
    {{
        "form_fields": [
            {{
                "field_name": "exact label from form",
                "bounding_box": {{
                    "x": float,
                    "y": float,
                    "width": float,
                    "height": float
                }}
            }}
        ]
    }}

    Notes:
    - Coordinates must be normalized between 0-1 (divide by image width {img_width} and height {img_height})
    - (0,0) is top-left, (1,1) is bottom-right
    - The bounding box should cover the entire input area
    - Include ALL form fields requiring user input
    - Copy field names exactly as they appear
    """

    return prompt

def extract_form_fields(image_path, model_id="llava-hf/llava-1.5-13b-hf", device=0):
    """
    Extract form fields from an image using LLAVA with format enforcement.
    
    Args:
        image_path: Path to the form image
        model_id: LLAVA model to use
        device: GPU device to use (0 for first GPU)
        
    Returns:
        FormFieldsResponse object containing extracted form fields
    """
    # Load model and processor
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True,
        cache_dir='/local/data/rds_hf_cache',
    ).to(device)

    processor = AutoProcessor.from_pretrained(model_id)
    
    # Prepare input
    prompt_text = get_prompt(image_path)
    raw_image = Image.open(image_path)
    
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
    inputs = processor(images=raw_image, text=prompt, return_tensors='pt').to(device, torch.float16)
    
    # Create format enforcer
    parser = JsonSchemaParser(FormFieldsResponse.schema())
    prefix_function = build_transformers_prefix_allowed_tokens_fn(processor.tokenizer, parser)
    
    # Generate with format enforcement
    output = model.generate(
        **inputs, 
        max_new_tokens=2000, 
        do_sample=False,
        prefix_allowed_tokens_fn=prefix_function
    )
    
    # Extract response
    raw_response = processor.decode(output[0][2:], skip_special_tokens=True)
    
    # Optionally save raw response
    with open("output.txt", "w") as f:
        f.write(raw_response)
    
    # Convert to Pydantic model to validate structure
    try:
        response_obj = FormFieldsResponse.parse_raw(raw_response)
        return response_obj
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {raw_response}")
        return None

if __name__ == "__main__":
    image_path = "./processed_pngs/grid_al_1_page_1.png"
    form_fields = extract_form_fields(image_path)
    
    if form_fields:
        print(f"Extracted {len(form_fields.form_fields)} form fields:")
        for field in form_fields.form_fields:
            print(f"- {field.field_name}: {field.bounding_box}")