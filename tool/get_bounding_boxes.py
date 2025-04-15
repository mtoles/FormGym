import os
import json

def extract_answer_bounding_boxes(json_file_path):
    """
    Extract bounding boxes of all elements labeled as "answer" from a JSON annotation file.
    
    Args:
        json_file_path: Path to the JSON annotation file
        
    Returns:
        List of bounding boxes [x_min, y_min, x_max, y_max]
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    bounding_boxes = []
    for item in data.get('form', []):
        if item.get('label') == 'answer':
            box = item.get('box', [])
            if len(box) == 4:
                bounding_boxes.append(box)
    
    return bounding_boxes

def process_annotation_files(annotations_dir, output_file):
    """
    Process all JSON annotation files and save their bounding boxes to a file.
    
    Args:
        annotations_dir: Directory containing JSON annotation files
        output_file: Path to the output file
    """
    bounding_boxes_dict = {}
    
    # Iterate through all JSON files in the directory
    for filename in os.listdir(annotations_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(annotations_dir, filename)
            bounding_boxes = extract_answer_bounding_boxes(json_path)
            
            # Store the filename (without extension) and its bounding boxes
            file_key = os.path.splitext(filename)[0]
            bounding_boxes_dict[file_key] = bounding_boxes
    
    # Save to output file
    with open(output_file, 'w') as f:
        json.dump(bounding_boxes_dict, f)
    
    print(f"Bounding boxes saved to {output_file}")
    print(f"Processed {len(bounding_boxes_dict)} files")

if __name__ == "__main__":
    # Directories
    annotations_dir = "dataset/raw/annotations"
    output_file = "dataset/all_bounding_boxes.txt"
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process annotation files
    process_annotation_files(annotations_dir, output_file)
