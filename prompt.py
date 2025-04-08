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