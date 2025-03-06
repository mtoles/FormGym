import base64
import json
from pathlib import Path
from openai import OpenAI
import os
from PIL import Image
import argparse

# List of models to use
MODELS = ["gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4.5-preview"]

def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_image_dimensions(image_path):
    """Get the dimensions of the image."""
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)

def extract_form_fields(image_path, model):
    """Extract form fields and their coordinates from an image."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
        
    client = OpenAI(api_key=api_key)
    base64_image = encode_image(image_path)
    img_width, img_height = get_image_dimensions(image_path)

    # Craft the prompt to specifically ask for form field information
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

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=4096,
        )
        
        # Extract the response and parse it as JSON
        result = response.choices[0].message.content
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            print(f"Error parsing JSON from response for {image_path} using {model}")
            print("Raw response:", result)
            return None
            
    except Exception as e:
        print(f"Error processing {image_path} with {model}: {str(e)}")
        return None

def process_all_images(model_names=None):
    """Process all PNG images from the pngs directory."""
    # Get the directories
    parent_dir = Path(__file__).parent.parent
    pngs_dir = parent_dir / 'pngs'
    
    # Get all PNG files
    png_files = list(pngs_dir.glob('*.png'))
    if not png_files:
        print(f"No PNG files found in {pngs_dir}")
        return
    
    # Use specified models or default to all models
    models_to_use = model_names if model_names else MODELS
    
    # Process each image with specified models
    for png_file in sorted(png_files):
        for model in models_to_use:
            print(f"\nProcessing {png_file.name} with {model}...")
            process_single_image(png_file.name, model)

def process_single_image(image_name, model_name=None):
    """Process a single PNG image from the pngs directory with specified model or all models."""
    # Get the directories
    parent_dir = Path(__file__).parent.parent
    pngs_dir = parent_dir / 'processed_pngs'
    form_data_dir = parent_dir / 'processed_form_data'
    form_data_dir.mkdir(exist_ok=True)

    # Get the specific image
    png_file = pngs_dir / image_name
    if not png_file.exists():
        print(f"Error: {image_name} not found in {pngs_dir}")
        return

    # Use specified model or default to all models
    models_to_use = [model_name] if model_name else MODELS
    
    # Process with each model
    for model in models_to_use:
        print(f"\nProcessing {png_file.name} with {model}...")
        
        # Create model-specific directory
        model_dir = form_data_dir / model
        model_dir.mkdir(exist_ok=True)
        
        # Extract form fields
        form_data = extract_form_fields(png_file, model)
        
        if form_data:
            # Save the results
            output_file = model_dir / f"{png_file.stem}_fields.json"
            with open(output_file, 'w') as f:
                json.dump(form_data, f, indent=2)
            print(f"Saved field data to {output_file}")
        else:
            print(f"No data extracted from {png_file.name} using {model}")

if __name__ == "__main__":
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        exit(1)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract form fields from images using OpenAI Vision API')
    parser.add_argument('--image', type=str, help='Name of specific image to process (e.g., bl_0_page_1.png)')
    parser.add_argument('--model', type=str, choices=MODELS, help='Specific model to use for processing')
    parser.add_argument('--all', action='store_true', help='Process all images in the pngs directory')
    
    args = parser.parse_args()
    
    # Process based on arguments
    if args.all:
        process_all_images([args.model] if args.model else None)
    else:
        # If no specific image is provided, use default
        image_name = args.image if args.image else "grid_bl_0_page_1.png"
        process_single_image(image_name, args.model)