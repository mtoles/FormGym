from PIL import Image

def get_image_dimensions(image_path):
    """Get the dimensions of the image."""
    with Image.open(image_path) as img:
        return img.size
    
def get_prompt(image_path):
    img_width, img_height = get_image_dimensions(image_path)

    prompt = f"""
    Analyze this form image and identify all form fields where information needs to be filled in.
    Return ONLY valid JSON. Do not include any code blocks, markdown, or extra text in your response. 
    For each field:
    1. Extract the field label/name exactly as it appears in the form
    2. Identify the bounding box coordinates of where the value should be filled (the empty space, box, or line where user input goes)
    3. Return the information in this exact JSON format:
    {{
        "form_fields": [
            {{
                "field_name": "exact label from form",
                "bounding_box": {{
                    "x": float between 0 and 1 (normalized x-coordinate of top-left corner),
                    "y": float between 0 and 1 (normalized y-coordinate of top-left corner),
                    "width": float between 0 and 1 (normalized width of input area),
                    "height": float between 0 and 1 (normalized height of input area)
                }}
            }}
        ]
    }}

    Important Notes:
    - Coordinates should be NORMALIZED between 0 and 1, where:
        * (0,0) is the top-left corner of the image
        * (1,1) is the bottom-right corner
        * x values are normalized by dividing by image width ({img_width})
        * y values are normalized by dividing by image height ({img_height})
    - Include ALL form fields where user input is expected
    - Be precise with field names, copying them exactly as they appear
    - For each field, the bounding box should cover the entire area where the answer/value should be written
    - Include checkboxes, text fields, signature areas, date fields, etc.
    - If a field has multiple input areas (like separate boxes for each digit), combine them into one bounding box
    """

    return prompt