from PIL import Image
import json
import base64

def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
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

import json

def parse_json_from_response(raw_response: str, start_text: str):
    """
    Locates 'ASSISTANT:' in the response (if present). Then extracts and parses
    the substring from the first '{' after that (or from the first '{' in the
    entire string if 'ASSISTANT:' isn't found) to the final '}' in the entire string.

    Returns the parsed JSON (as a Python object) on success, or None if extraction/parsing fails.
    """

    # Attempt to locate "ASSISTANT:"
    assistant_index = raw_response.find(start_text)
    
    # If found, search for the first '{' after "ASSISTANT:"
    if assistant_index != -1:
        first_brace_index = raw_response.find("{", assistant_index)
    else:
        # If not found, just locate the first '{' in the entire string
        first_brace_index = raw_response.find("{")

    if first_brace_index == -1:
        print("No '{' found in the response.")
        return None

    # Find the last '}' in the entire string
    last_brace_index = raw_response.rfind("}")
    if last_brace_index == -1:
        print("No '}' found in the response.")
        return None

    # Ensure the first '{' is before the last '}'
    if first_brace_index > last_brace_index:
        print("First '{' occurs after the last '}'. Invalid JSON structure.")
        return None

    # Extract the substring containing the potential JSON
    json_str = raw_response[first_brace_index : last_brace_index + 1]

    return json_str

    # Attempt to parse as JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        print("Failed to parse JSON.")
        return None
