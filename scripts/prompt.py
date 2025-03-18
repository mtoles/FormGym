from PIL import Image
import json
import base64
import re

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


def parse_and_reconstruct_fields(response_text):
    # Two regex patterns to match both escaped and non-escaped variants
    # Pattern 1: For escaped format with backslashes (field\_name)
    pattern_escaped = r'\{\s*"field\\_name":\s*"([^"]+)",\s*"bounding\\_box":\s*\{\s*"x":\s*([0-9.]+),\s*"y":\s*([0-9.]+),\s*"width":\s*([0-9.]+),\s*"height":\s*([0-9.]+)\s*\}\s*\}'
    
    # Pattern 2: For standard format without escapes (field_name)
    pattern_standard = r'\{\s*"field_name":\s*"([^"]+)",\s*"bounding_box":\s*\{\s*"x":\s*([0-9.]+),\s*"y":\s*([0-9.]+),\s*"width":\s*([0-9.]+),\s*"height":\s*([0-9.]+)\s*\}\s*\}'
    
    # Find all matches for both patterns
    matches_escaped = re.finditer(pattern_escaped, response_text)
    matches_standard = re.finditer(pattern_standard, response_text)
    
    # Combine the matches
    form_fields = []
    
    # Process escaped matches
    for match in matches_escaped:
        field_name = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        width = float(match.group(4))
        height = float(match.group(5))
        
        field_entry = {
            "field_name": field_name,
            "bounding_box": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            }
        }
        form_fields.append(field_entry)
    
    # Process standard matches
    for match in matches_standard:
        field_name = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        width = float(match.group(4))
        height = float(match.group(5))
        
        field_entry = {
            "field_name": field_name,
            "bounding_box": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            }
        }
        form_fields.append(field_entry)
    
    # Create the final structure
    result = {
        "form_fields": form_fields
    }
    
    return result