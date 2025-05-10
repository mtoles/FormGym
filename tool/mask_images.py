import os
import json
import cv2
import numpy as np
from PIL import Image

def load_bounding_boxes(filepath):
    """
    Load the bounding boxes from the file.
    
    Args:
        filepath: Path to the file containing bounding boxes
        
    Returns:
        Dictionary of filename -> bounding boxes
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def create_masked_image(image_path, bounding_boxes, output_path):
    """
    Create a masked image with white overlay at the bounding box locations.
    
    Args:
        image_path: Path to the input image
        bounding_boxes: List of bounding boxes [x_min, y_min, x_max, y_max]
        output_path: Path to save the masked image
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: Could not read image {image_path}")
        return False
    
    # Create a copy of the image
    masked_img = img.copy()
    
    # Fill each bounding box with solid white
    for box in bounding_boxes:
        x_min, y_min, x_max, y_max = box
        # Fill the area with solid white (255, 255, 255)
        masked_img[y_min:y_max, x_min:x_max] = [255, 255, 255]
    
    # Save the masked image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, masked_img)
    return True

def process_images(bounding_boxes_file, images_dir, output_dir):
    """
    Process all images based on the bounding boxes.
    
    Args:
        bounding_boxes_file: Path to the file containing bounding boxes
        images_dir: Directory containing the input images
        output_dir: Directory to save the masked images
    """
    # Load bounding boxes
    bounding_boxes_dict = load_bounding_boxes(bounding_boxes_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Keep track of successful operations
    successful = 0
    failed = 0
    
    # Process each image
    for filename, boxes in bounding_boxes_dict.items():
        # Check for different possible image extensions
        for ext in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
            image_path = os.path.join(images_dir, filename + ext)
            if os.path.exists(image_path):
                output_path = os.path.join(output_dir, filename + ext)
                if create_masked_image(image_path, boxes, output_path):
                    successful += 1
                else:
                    failed += 1
                break
        else:
            print(f"Warning: No image file found for {filename}")
            failed += 1
    
    print(f"Processing complete: {successful} images processed successfully, {failed} failed")

if __name__ == "__main__":
    # Paths
    bounding_boxes_file = "./dataset/funsd/all_bounding_boxes.txt"
    images_dir = "./dataset/funsd/images"
    output_dir = "./dataset/processed/funsd/images"
    
    # Process images
    process_images(bounding_boxes_file, images_dir, output_dir)
