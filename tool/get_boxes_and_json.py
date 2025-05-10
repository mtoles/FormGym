import os
import json
import uuid
from PIL import Image

def get_image_dimensions(image_path):
    """
    Get the width and height of an image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (width, height)
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error reading image {image_path}: {str(e)}")
        return (1224, 1584)  # Default dimensions if image can't be read

def process_annotation_file(json_file_path, images_dir):
    """
    Process a single annotation file and convert it to the desired format.
    
    Args:
        json_file_path: Path to the JSON annotation file
        images_dir: Directory containing the corresponding images
        
    Returns:
        Tuple of (processed_annotation_dict, list_of_uuids)
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Get the filename without extension
    filename = os.path.basename(json_file_path)
    filename_without_ext = os.path.splitext(filename)[0]
    
    # Get image dimensions from the corresponding image file
    image_path = os.path.join(images_dir, f"{filename_without_ext}.png")
    image_width, image_height = get_image_dimensions(image_path)
    
    # Create the output structure
    output = {
        "item": {
            "slots": [
                {
                    "width": image_width,
                    "height": image_height
                }
            ]
        },
        "annotations": []
    }
    
    # List to store UUIDs
    uuids = []
    
    # Process each annotation
    for item in data.get('form', []):
        if item.get('label') == 'answer':
            box = item.get('box', [])
            if len(box) == 4:
                x_min, y_min, x_max, y_max = box
                
                # Calculate width and height
                width = x_max - x_min
                height = y_max - y_min
                
                # Generate UUID
                component_id = str(uuid.uuid4())
                uuids.append(component_id)
                
                # Create annotation entry
                annotation = {
                    "id": component_id,
                    "name": item.get('text', '').strip(),  # Use the text as the field name
                    "bounding_box": {
                        "x": x_min,
                        "y": y_min,
                        "w": width,
                        "h": height
                    }
                }
                
                output["annotations"].append(annotation)
    
    return output, uuids

def process_all_annotations(input_dir, output_dir, images_dir):
    """
    Process all annotation files in the input directory and save them to the output directory.
    
    Args:
        input_dir: Directory containing input JSON annotation files
        output_dir: Directory where processed annotations will be saved
        images_dir: Directory containing the corresponding images
    """
    # Create output directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    targets_dir = "./dataset/processed/funsd/targets"
    os.makedirs(targets_dir, exist_ok=True)
    
    # Process each JSON file
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
            targets_path = os.path.join(targets_dir, f"{os.path.splitext(filename)[0]}_targets.json")
            
            # Process the file
            processed_data, uuids = process_annotation_file(input_path, images_dir)
            
            # Save the processed data
            with open(output_path, 'w') as f:
                json.dump(processed_data, f, indent=2)
            
            # Save the targets data
            targets_data = {"selected_ids": uuids}
            with open(targets_path, 'w') as f:
                json.dump(targets_data, f, indent=2)
            
            print(f"Processed {filename} -> {os.path.basename(output_path)} and {os.path.basename(targets_path)}")

if __name__ == "__main__":
    # Directories
    input_dir = "dataset/funsd/annotations"
    output_dir = "dataset/processed/funsd/bounding_boxes"
    images_dir = "dataset/funsd/images"
    
    # Process all annotations
    process_all_annotations(input_dir, output_dir, images_dir)