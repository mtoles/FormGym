import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def add_grid_overlay(image_path, output_path):
    """
    Add a 10x10 grid overlay to an image with coordinates and dots at intersections.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path where the processed image will be saved
    """
    # Open and convert image to RGB if necessary
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Calculate grid spacing
    x_spacing = width / 10
    y_spacing = height / 10
    
    # Draw vertical and horizontal lines
    for i in range(11):
        # Vertical lines
        x = i * x_spacing
        draw.line([(x, 0), (x, height)], fill='red', width=2)
        
        # Horizontal lines
        y = i * y_spacing
        draw.line([(0, y), (width, y)], fill='red', width=2)
        
        # Add dots at intersections
        for j in range(11):
            x = i * x_spacing
            y = j * y_spacing
            # Draw a filled circle at each intersection
            dot_radius = 5
            draw.ellipse([(x - dot_radius, y - dot_radius), 
                         (x + dot_radius, y + dot_radius)], 
                        fill='blue')
            
            # Add coordinates
            if i < 10 and j < 10:
                coord_x = round(i / 10, 1)
                coord_y = round(j / 10, 1)
                text = f"({coord_x}, {coord_y})"
                # Position text slightly offset from the intersection
                draw.text((x + 10, y + 10), text, fill='green')
    
    # Save the processed image
    img.save(output_path)

def process_directory(input_dir, output_dir):
    """
    Process all PNG images in the input directory and save them to the output directory.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory where processed images will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all PNG files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"grid_{filename}")
            add_grid_overlay(input_path, output_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    # Get the parent directory (where pngs and processed_pngs folders are)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Set input and output directories relative to parent directory
    input_dir = os.path.join(parent_dir, "pngs")
    output_dir = os.path.join(parent_dir, "processed_pngs")
    
    process_directory(input_dir, output_dir)
