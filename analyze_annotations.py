#!/usr/bin/env python3
"""
Script to analyze the form-nlu annotation scheme and visualize annotations on the first image.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import os


def load_annotations(file_path):
    """Load annotations from JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def get_first_image_annotations(annotations_data):
    """Get annotations for the first image in the dataset."""
    if "annotations" in annotations_data:
        annotations = annotations_data["annotations"]
    else:
        annotations = annotations_data

    # Group annotations by image_id
    image_annotations = {}
    for ann in annotations:
        img_id = ann["image_id"]
        if img_id not in image_annotations:
            image_annotations[img_id] = []
        image_annotations[img_id].append(ann)

    # Get the first image ID
    first_image_id = min(image_annotations.keys())
    return first_image_id, image_annotations[first_image_id]


def find_image_file(image_id, annotations_data, images_dir):
    """Find the image file corresponding to the image_id."""
    # Look for the image filename in the annotations data structure
    try:
        # Check if there's an "object" field with "images" array
        if "object" in annotations_data and "images" in annotations_data["object"]:
            for img_info in annotations_data["object"]["images"]:
                if img_info.get("id") == image_id:
                    filename = img_info.get("file_name")
                    if filename:
                        return os.path.join(images_dir, filename)

        # If not found in object.images, try to find any image with matching ID
        if "images" in annotations_data:
            for img_info in annotations_data["images"]:
                if img_info.get("id") == image_id:
                    filename = img_info.get("file_name")
                    if filename:
                        return os.path.join(images_dir, filename)

        # Fallback: if we can't find the mapping, use the first available image
        print(f"Warning: Could not find filename mapping for image_id {image_id}")
        image_files = [f for f in os.listdir(images_dir) if f.endswith(".png")]
        if image_files:
            return os.path.join(images_dir, image_files[0])

    except Exception as e:
        print(f"Error finding image file: {e}")

    return None


def visualize_annotations(image_path, annotations, output_path=None):
    """Visualize annotations on the image."""
    # Load image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(15, 20))
    ax.imshow(img_array)

    # Define category colors (based on what we saw in the annotations)
    category_colors = {
        1: "#c9c910",  # Form header
        2: "#c4db43",  # Section headers
        3: "#11f37a",  # Field labels
        4: "#3cf3fe",  # Field names
        5: "#6aefe4",  # Values
        6: "#afe34a",  # Table headers
        7: "#68ef3a",  # Table values
    }

    # Draw annotations
    for ann in annotations:
        # Get bounding box
        bbox = ann["bbox"]  # [x, y, width, height]
        x, y, w, h = bbox

        # Get category and color
        category_id = ann["category_id"]
        color = ann.get("color", category_colors.get(category_id, "#ff0000"))

        # Create rectangle patch
        rect = patches.Rectangle(
            (x, y), w, h, linewidth=2, edgecolor=color, facecolor="none", alpha=0.8
        )
        ax.add_patch(rect)

        # Add text label
        text = ann.get("text", f"Cat {category_id}")
        if text and len(text.strip()) > 0:
            # Truncate long text
            display_text = text[:30] + "..." if len(text) > 30 else text
            ax.text(
                x,
                y - 5,
                display_text,
                fontsize=8,
                color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
            )

    # Set title
    ax.set_title(f"Image with {len(annotations)} Annotations", fontsize=16)
    ax.axis("off")

    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"Visualization saved to {output_path}")
    else:
        plt.show()

    plt.close()


def analyze_annotation_scheme(annotations_data):
    """Analyze the annotation scheme structure."""
    print("=== ANNOTATION SCHEME ANALYSIS ===\n")

    if "annotations" in annotations_data:
        annotations = annotations_data["annotations"]
    else:
        annotations = annotations_data

    # Count total annotations
    print(f"Total annotations: {len(annotations)}")

    # Count unique image IDs
    image_ids = set(ann["image_id"] for ann in annotations)
    print(f"Unique image IDs: {len(image_ids)}")

    # Analyze categories
    categories = {}
    for ann in annotations:
        cat_id = ann["category_id"]
        if cat_id not in categories:
            categories[cat_id] = {"count": 0, "examples": []}
        categories[cat_id]["count"] += 1
        if len(categories[cat_id]["examples"]) < 3:  # Keep first 3 examples
            categories[cat_id]["examples"].append(ann.get("text", "No text"))

    print(f"\nCategory breakdown:")
    for cat_id, info in sorted(categories.items()):
        print(f"  Category {cat_id}: {info['count']} annotations")
        print(f"    Examples: {info['examples']}")

    # Analyze annotation structure
    if annotations:
        first_ann = annotations[0]
        print(f"\nAnnotation structure:")
        for key, value in first_ann.items():
            if key == "segmentation":
                print(f"  {key}: {type(value)} (length: {len(value)})")
            elif key == "bbox":
                print(f"  {key}: {value} (format: [x, y, width, height])")
            else:
                print(f"  {key}: {type(value)} = {value}")


def main():
    """Main function."""
    # Paths
    val_file = "annotations/form-nlu/val.json"
    images_dir = "annotations/form-nlu/images"

    # Check if files exist
    if not os.path.exists(val_file):
        print(f"Error: {val_file} not found!")
        return

    if not os.path.exists(images_dir):
        print(f"Error: {images_dir} not found!")
        return

    # Load annotations
    print("Loading annotations...")
    annotations_data = load_annotations(val_file)

    # Analyze the scheme
    analyze_annotation_scheme(annotations_data)

    # Get first image annotations
    print("\n=== FIRST IMAGE ANALYSIS ===")
    first_image_id, first_image_anns = get_first_image_annotations(annotations_data)
    print(f"First image ID: {first_image_id}")
    print(f"Number of annotations: {len(first_image_anns)}")

    # Find corresponding image file
    image_path = find_image_file(first_image_id, annotations_data, images_dir)
    if image_path:
        print(f"Found image: {image_path}")

        # Visualize annotations
        output_path = "first_image_annotations.png"
        visualize_annotations(image_path, first_image_anns, output_path)

        # Show some annotation details
        print(f"\nFirst few annotations for image {first_image_id}:")
        for i, ann in enumerate(first_image_anns[:5]):
            print(
                f"  {i+1}. Category {ann['category_id']}: {ann.get('text', 'No text')}"
            )
            print(f"     BBox: {ann['bbox']}")
            print(f"     Color: {ann.get('color', 'Default')}")
    else:
        print("Could not find corresponding image file.")


if __name__ == "__main__":
    main()
