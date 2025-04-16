import json
import os
from pathlib import Path
import pandas as pd
from PIL import Image
import numpy as np
from collections import defaultdict
from tqdm import tqdm


def process_annotation_and_image(file_path, input_images_dir, output_images_dir):
    """Process a single annotation file and its corresponding image."""
    with open(file_path, "r") as f:
        data = json.load(f)["form"]

    form_id = Path(file_path).stem
    pairs = []

    # Create a mapping of IDs to their corresponding entries
    id_to_entry = {entry["id"]: entry for entry in data}

    # Track how many times this form_id has been processed
    counter = 1

    # Process each entry
    for entry in data:
        if entry["label"] == "question" and entry.get("linking"):
            for link in entry["linking"]:
                question_id, answer_id = link
                if answer_id in id_to_entry:
                    answer_entry = id_to_entry[answer_id]

                    # Process the image
                    input_image_path = os.path.join(input_images_dir, f"{form_id}.png")
                    output_image_path = os.path.join(
                        output_images_dir, f"processed_{form_id}_{counter}.png"
                    )

                    if os.path.exists(input_image_path):
                        # Load and process image
                        img = Image.open(input_image_path)
                        img_array = np.array(img)

                        # Convert bbox coordinates to integers
                        x1, y1, x2, y2 = map(int, answer_entry["box"])

                        # Ensure coordinates are within image bounds
                        height, width = img_array.shape[:2]
                        x1 = max(0, min(x1, width))
                        y1 = max(0, min(y1, height))
                        x2 = max(0, min(x2, width))
                        y2 = max(0, min(y2, height))

                        # Mask the answer region with white
                        img_array[y1:y2, x1:x2] = 255

                        # Save the processed image
                        processed_img = Image.fromarray(img_array)
                        processed_img.save(output_image_path)

                        # Add the pair with image filename
                        pairs.append(
                            {
                                "form_id": form_id,
                                "question_text": entry["text"],
                                "question_bbox": entry["box"],
                                "answer_text": answer_entry["text"],
                                "answer_bbox": answer_entry["box"],  # [x1 y1 x2 y2]
                                "processed_image": f"processed_{form_id}_{counter}.png",
                                "w": width,
                                "h": height,
                            }
                        )

                        counter += 1
                    else:
                        print(f"Warning: Image not found: {input_image_path}")

    return pairs


def main():
    # Directory paths
    annotations_dir = Path("tool/dataset/funsd/annotations")
    input_images_dir = "tool/dataset/funsd/images"
    output_images_dir = "tool/dataset/processed/images"
    output_dir = "tool/dataset/processed"

    # Create output directories
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Process all JSON files
    all_pairs = []
    for json_file in tqdm(
        list(annotations_dir.glob("*.json")), desc="Processing JSON files"
    ):
        pairs = process_annotation_and_image(
            json_file, input_images_dir, output_images_dir
        )
        all_pairs.extend(pairs)

    # Create DataFrame
    df = pd.DataFrame(all_pairs)

    # Get unique form_ids and shuffle them
    unique_forms = df["form_id"].unique()
    np.random.shuffle(unique_forms)

    # Split form_ids into train and test (80/20)
    train_size = int(0.8 * len(unique_forms))
    train_forms = unique_forms[:train_size]
    test_forms = unique_forms[train_size:]

    # Split the dataset based on form_ids
    train_df = df[df["form_id"].isin(train_forms)]
    test_df = df[df["form_id"].isin(test_forms)]

    # Shuffle the train and test sets
    train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)
    test_df = test_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save full train and test sets
    train_df.to_json(
        os.path.join(output_dir, "funsd_train_qa_pairs.json"), orient="records", indent=2
    )
    test_df.to_json(
        os.path.join(output_dir, "funsd_test_qa_pairs.json"), orient="records", indent=2
    )

    # Save short versions (64 samples each)
    train_df.head(64).to_json(
        os.path.join(output_dir, "funsd_train_qa_pairs_short.json"),
        orient="records",
        indent=2,
    )
    test_df.head(64).to_json(
        os.path.join(output_dir, "funsd_test_qa_pairs_short.json"),
        orient="records",
        indent=2,
    )

    print(f"Processed {len(df)} question-answer pairs")
    print(f"Train set size: {len(train_df)}")
    print(f"Test set size: {len(test_df)}")
    print(f"Saved processed images to {output_images_dir}")
    print(f"Saved QA pairs to {output_dir}")


if __name__ == "__main__":
    main()
