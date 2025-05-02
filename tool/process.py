import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
from PIL import Image
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import cv2
import torch
from dataclasses import dataclass
import libcontent_aware_fill as cwf

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
SUPPORTED_DATASETS = ["funsd", "xfund"]
DEFAULT_IMAGE_EXT = "png"
TRAIN_TEST_SPLIT_RATIO = 0.8
SHORT_DATASET_SIZE = 64


@dataclass
class Args:
    checkpoint: str
    model_type: str
    input: str
    output: Optional[str]
    device: str


class BoundingBox:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @classmethod
    def from_list(cls, box: List[int]) -> "BoundingBox":
        return cls(*map(int, box))

    def to_list(self) -> List[int]:
        return [self.x1, self.y1, self.x2, self.y2]

    def clip_to_bounds(self, width: int, height: int) -> None:
        """Clip bounding box coordinates to image dimensions."""
        self.x1 = max(0, min(self.x1, width))
        self.y1 = max(0, min(self.y1, height))
        self.x2 = max(0, min(self.x2, width))
        self.y2 = max(0, min(self.y2, height))


def process_annotation_and_image(
    doc: List[Dict],
    form_id: str,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
) -> List[Dict]:
    """
    Process a single document and its corresponding image.

    Args:
        doc: List of document entries
        form_id: Unique identifier for the form
        input_images_dir: Directory containing input images
        output_images_dir: Directory to save processed images
        image_ext: Image file extension

    Returns:
        List of processed question-answer pairs with their metadata
    """
    pairs = []
    id_to_entry = {entry["id"]: entry for entry in doc}

    input_image_path = os.path.join(input_images_dir, f"{form_id}.{image_ext}")

    # Load input image and get dimensions
    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError(f"Could not load image: {input_image_path}")
    height, width = img.shape[:2]
    output_image_path = os.path.join(output_images_dir, f"processed_{form_id}.png")
    mask_bboxes = []

    for entry in doc:
        if entry["label"] != "question" or not entry.get("linking"):
            continue

        for question_id, answer_id in entry["linking"]:
            if answer_id not in id_to_entry:
                continue

            answer_entry = id_to_entry[answer_id]
            if answer_entry["label"] == "question":
                continue

            # Process bounding box
            bbox = BoundingBox.from_list(answer_entry["box"])
            mask_bboxes.append(bbox)
            pairs.append(
                {
                    "form_id": form_id,
                    "question_text": entry["text"],
                    "question_bbox": entry["box"],
                    "answer_text": answer_entry["text"],
                    "answer_bbox": answer_entry["box"],
                    "processed_image": f"processed_{form_id}.png",
                    "w": width,
                    "h": height,
                }
            )
        filled_img = img.copy()
        # Create a single mask for all bounding boxes
        mask = np.zeros((height, width), dtype=np.uint8)
        for mask_bbox in mask_bboxes:
            # Clip bbox to image bounds
            # mask.clip_to_bounds(width, height)
            mask[mask_bbox.y1 : mask_bbox.y2, mask_bbox.x1 : mask_bbox.x2] = 255

        # Apply content-aware fill once with combined mask
        filled_img = cwf.content_aware_fill(
            filled_img,
            mask,
            isMakeSeamlesslyTileableHorizontally=False,
            isMakeSeamlesslyTileableVertically=False,
            matchContextType=3,
            mapWeight=0.5,
            sensitivityToOutliers=0.117,
            patchSize=50,
            maxProbeCount=200,
        )

    # Save processed image
    cv2.imwrite(output_image_path, filled_img)

    return pairs


def process_document(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
) -> List[Dict]:
    """
    Process a single document and return its pairs.

    Args:
        data: Document data dictionary
        input_images_dir: Directory containing input images
        output_images_dir: Directory to save processed images
        image_ext: Image file extension
        json_file: Path to the JSON file (used for FUNSD dataset)

    Returns:
        List of processed question-answer pairs
    """
    doc = data.get("document") or data.get("form")
    if not doc:
        raise ValueError("Document data must contain either 'document' or 'form' key")

    form_id = data.get("id") or Path(json_file).stem
    if not form_id:
        raise ValueError("Form ID could not be determined")

    return process_annotation_and_image(
        doc, form_id, input_images_dir, output_images_dir, image_ext
    )


def process_document_with_dirs(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
) -> List[Dict]:
    """Process a single document with directory paths."""
    return process_document(
        data, input_images_dir, output_images_dir, image_ext, json_file
    )


def save_dataset(
    df: pd.DataFrame,
    output_dir: str,
    dataset_name: str,
    train_forms: np.ndarray,
    test_forms: np.ndarray,
    save_short: bool = True,
) -> None:
    """
    Save the processed dataset to JSON files.

    Args:
        df: DataFrame containing the dataset
        output_dir: Directory to save the files
        dataset_name: Name of the dataset
        train_forms: Array of form IDs for training set
        test_forms: Array of form IDs for test set
        save_short: Whether to save a short version of the dataset
    """
    # Save full train and test sets
    train_df = df[df["form_id"].isin(train_forms)]
    test_df = df[df["form_id"].isin(test_forms)]

    # Shuffle datasets
    train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)
    test_df = test_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save full datasets
    train_df.to_json(
        os.path.join(output_dir, f"{dataset_name}_train_qa_pairs.json"),
        orient="records",
        indent=2,
    )
    test_df.to_json(
        os.path.join(output_dir, f"{dataset_name}_test_qa_pairs.json"),
        orient="records",
        indent=2,
    )

    if save_short:
        # Save short versions
        train_df.head(SHORT_DATASET_SIZE).to_json(
            os.path.join(output_dir, f"{dataset_name}_train_qa_pairs_short.json"),
            orient="records",
            indent=2,
        )
        test_df.head(SHORT_DATASET_SIZE).to_json(
            os.path.join(output_dir, f"{dataset_name}_test_qa_pairs_short.json"),
            orient="records",
            indent=2,
        )


def main(dataset: str = "funsd") -> None:
    """
    Process either FUNSD or XFUND dataset based on the input parameter.

    Args:
        dataset: Name of the dataset to process ("funsd" or "xfund")
    """
    if dataset not in SUPPORTED_DATASETS:
        raise ValueError(f"Dataset must be one of {SUPPORTED_DATASETS}")

    # Setup directories
    annotations_dir = Path(f"tool/dataset/{dataset}/annotations")
    input_images_dir = f"tool/dataset/{dataset}/images"
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
        # try:
        with open(json_file, "r") as f:
            data = json.load(f)

        if dataset == "xfund":
            # Process XFUND documents in parallel
            dataset_items = data["documents"]
            num_processes = min(cpu_count() // 2 + 1, len(dataset_items))
            with Pool(processes=num_processes) as pool:
                results = pool.starmap(
                    process_document_with_dirs,
                    [
                        (d, input_images_dir, output_images_dir, "jpg", json_file)
                        for d in dataset_items
                    ],
                )
                for pairs in results:
                    all_pairs.extend(pairs)
        else:
            # Process FUNSD documents
            pairs = process_document(
                data, input_images_dir, output_images_dir, "png", json_file
            )
            all_pairs.extend(pairs)

        # except Exception as e:
        #     logger.error(f"Error processing {json_file}: {str(e)}")
        #     continue

    # Create and split dataset
    df = pd.DataFrame(all_pairs)
    unique_forms = df["form_id"].unique()
    np.random.shuffle(unique_forms)

    train_size = int(TRAIN_TEST_SPLIT_RATIO * len(unique_forms))
    train_forms = unique_forms[:train_size]
    test_forms = unique_forms[train_size:]

    # Save datasets
    save_dataset(df, output_dir, dataset, train_forms, test_forms)

    # Log statistics
    logger.info(f"Processed {len(df)} question-answer pairs")
    logger.info(f"Train set size: {len(df[df['form_id'].isin(train_forms)])}")
    logger.info(f"Test set size: {len(df[df['form_id'].isin(test_forms)])}")
    logger.info(f"Saved processed images to {output_images_dir}")
    logger.info(f"Saved QA pairs to {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process FUNSD or XFUND dataset")
    parser.add_argument(
        "--dataset",
        type=str,
        choices=SUPPORTED_DATASETS,
        default="funsd",
        help="Dataset to process (funsd or xfund)",
    )
    args = parser.parse_args()
    main(args.dataset)
