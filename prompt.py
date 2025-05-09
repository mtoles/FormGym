from PIL import Image
import json
import base64
import re
import textwrap

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

def parse_raw_output(raw_text):
    """
    Parse 'raw_text' that is intended to be a JSON array of objects with
    keys: 'action', 'cx', 'cy', and 'value'. If the text is not strictly
    valid JSON (for example because it ends abruptly), fall back to a
    regex approach to extract valid dictionary blocks. 
    """
    # Remove any leading/trailing backticks or ```json fences.
    raw_text = raw_text.strip().strip('`')
    raw_text = raw_text.replace('```json', '').replace('```', '').strip()
    
    # Attempt 1: Try loading as valid JSON
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        data = None
    
    # If direct JSON parsing failed or returned something invalid,
    # fall back to a regex approach.
    if not isinstance(data, list):
        data = []
        # Regex to capture minimal well-formed objects of the kind:
        # {"action": "...", "cx": 0.5, "cy": 0.5, "value": "..."}
        pattern = re.compile(
            r'\{\s*"action":\s*"([^"]+)"\s*,'
            r'\s*"cx":\s*([\d.]+)\s*,'
            r'\s*"cy":\s*([\d.]+)\s*,'
            r'\s*"value":\s*"([^"]+)"\s*\}'
        )
        for match in pattern.finditer(raw_text):
            entry = {
                "action": match.group(1),
                "cx": float(match.group(2)),
                "cy": float(match.group(3)),
                "value": match.group(4)
            }
            data.append(entry)
    
    # Filter out anything that does not have the required keys
    required_keys = {"action", "cx", "cy", "value"}
    valid_entries = []
    for item in data:
        # Check that it's a dictionary and has all keys
        if isinstance(item, dict) and required_keys.issubset(item.keys()):
            valid_entries.append({
                "action": item["action"],
                "cx": item["cx"],
                "cy": item["cy"],
                "value": item["value"]
            })
    
    return valid_entries