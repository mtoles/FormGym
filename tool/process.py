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

# import libcontent_aware_fill as cwf
from resynthesizer import resynthesize, TImageSynthParameters

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


def get_full_question_text(entry: Dict, id_to_entry: Dict) -> str:
    question_texts = []
    seen_ids = set()

    def add_linked_questions(entry_id):
        if entry_id in seen_ids:
            return
        seen_ids.add(entry_id)
        linked_entry = id_to_entry[entry_id]
        question_texts.append(linked_entry["text"])
        for e in linked_entry["linking"]:
            add_linked_questions(e[0])

    for link in entry["linking"]:
        add_linked_questions(link[0])

    return " | ".join(question_texts)


def get_question_and_answer(
    entry: Dict,
    form_id: str,
    width: int,
    height: int,
    id_to_entry: Dict,
    processed_filename: str = None,
    split: str = None,
) -> dict:
    if entry["label"] == "question":
        cbs = [c for c in entry["text"] if c in "☑☐⬛✓✗\u2611\u2610"]
        non_cbs_text = "".join(
            [c for c in entry["text"] if c not in "☑☐⬛✓✗\u2611\u2610"]
        )
        # If question contains a checkbox, use the checkbox as the answer
        if cbs:
            cb = cbs[0]
            for word in entry["words"]:
                if cb in word["text"]:
                    recursive_question_text = get_full_question_text(entry, id_to_entry)
                    if not (recursive_question_text or non_cbs_text):
                        print(f"No question text for {form_id} entry {entry['id']}")
                        return None
                    question_text = (
                        f"{recursive_question_text} | {non_cbs_text}"
                        if recursive_question_text and non_cbs_text
                        else recursive_question_text or non_cbs_text
                    ).strip()
                    question_bbox = BoundingBox.from_list(entry["box"])
                    out_entry = {
                        "form_id": form_id,
                        "question_text": question_text,
                        "answer_text": word["text"],
                        "answer_bbox": BoundingBox.from_list(word["box"]),
                        "question_bbox": question_bbox,
                        "processed_image": f"processed_{form_id}.png",
                        "w": width,
                        "h": height,
                    }
                    if split:
                        out_entry["split"] = split
                    return out_entry
        else:
            return None
    elif entry["label"] == "answer":
        out_entry = {
            "form_id": form_id,
            "question_text": get_full_question_text(entry, id_to_entry),
            "answer_text": entry["text"],
            "answer_bbox": BoundingBox.from_list(entry["box"]),
            "processed_image": f"processed_{form_id}.png",
            "w": width,
            "h": height,
        }
        if split:
            out_entry["split"] = split
        return out_entry
    else:
        return None  # I didn't know there were other options


def process_annotation_and_image(
    doc: List[Dict],
    form_id: str,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    dataset_name: str = None,
    split: str = None,
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

    # For XFUND, try both train and test directories due to mismatched organization
    if dataset_name == "xfund":
        train_image_path = os.path.join(
            f"tool/dataset/{dataset_name}_train/images", f"{form_id}.{image_ext}"
        )
        test_image_path = os.path.join(
            f"tool/dataset/{dataset_name}_test/images", f"{form_id}.{image_ext}"
        )

        if os.path.exists(train_image_path):
            input_image_path = train_image_path
        elif os.path.exists(test_image_path):
            input_image_path = test_image_path
        else:
            raise ValueError(
                f"Could not find image {form_id}.{image_ext} in either XFUND train or test directories"
            )
    else:
        input_image_path = os.path.join(input_images_dir, f"{form_id}.{image_ext}")

    # Load input image and get dimensions
    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError(f"Could not load image: {input_image_path}")
    height, width = img.shape[:2]
    output_image_path = os.path.join(output_images_dir, f"processed_{form_id}.png")
    mask_bboxes = []
    # filled_img = img.copy()
    mask = np.zeros((height, width), dtype=np.uint8)
    for entry in doc:
<<<<<<< HEAD
        pair = get_question_and_answer(entry, form_id, width, height, id_to_entry)
=======
        pair = get_question_and_answer(
            entry, form_id, width, height, id_to_entry, processed_filename, split
        )
>>>>>>> @{-1}
        if pair is None:
            continue

        # filled_img = img.copy()
        # Create a single mask for all bounding boxes
        # for mask_bbox in mask_bboxes:
        # Clip bbox to image bounds
        # mask.clip_to_bounds(width, height)
        mask[
            pair["answer_bbox"].y1 : pair["answer_bbox"].y2,
            pair["answer_bbox"].x1 : pair["answer_bbox"].x2,
        ] = 255
        pairs.append(pair)
    if len(pairs) == 0:
        return []
    # Apply content-aware fill once with combined mask
    params = TImageSynthParameters()
    params.isMakeSeamlesslyTileableHorizontally = False
    params.isMakeSeamlesslyTileableVertically = False
    params.matchContextType = 3
    params.mapWeight = 0.5
    params.sensitivityToOutliers = 0.117
    params.patchSize = 50
    params.maxProbeCount = 200

    filled_img = np.array(
        resynthesize(
            Image.fromarray(img),
            Image.fromarray(mask),
            parameters=params,
        )
    )

    # Save processed image
    if filled_img is None:
        print(f"Could not fill image for {form_id} (no answers found?)")
        return []
    # cv2.imwrite("original_tmp.png", img)
    # cv2.imwrite("filled_tmp.png", filled_img)
    cv2.imwrite(output_image_path, filled_img)

    return pairs


def process_document(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
<<<<<<< HEAD
=======
    dataset_name: str = None,
    split: str = None,
>>>>>>> @{-1}
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
<<<<<<< HEAD
        doc, form_id, input_images_dir, output_images_dir, image_ext
=======
        doc,
        form_id,
        input_images_dir,
        output_images_dir,
        image_ext,
        dataset_name,
        split,
>>>>>>> @{-1}
    )


def process_document_with_dirs(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
<<<<<<< HEAD
) -> List[Dict]:
    """Process a single document with directory paths."""
    return process_document(
        data, input_images_dir, output_images_dir, image_ext, json_file
=======
    dataset_name: str = None,
    split: str = None,
) -> List[Dict]:
    """Process a single document with directory paths."""
    return process_document(
        data,
        input_images_dir,
        output_images_dir,
        image_ext,
        json_file,
        dataset_name,
        split,
>>>>>>> @{-1}
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

<<<<<<< HEAD
=======
    # save images of the first 5 images in the short test set.
    # draw the bounding boxes on the images  including text labels.

    # Get the first 5 images from the short test set
    short_test_df = test_df.head(SHORT_DATASET_SIZE)
    first_5_images = short_test_df.head(5)

    # # Create output directory for annotated images
    # annotated_images_dir = os.path.join(output_dir, "annotated_images")
    # os.makedirs(annotated_images_dir, exist_ok=True)

    # Process each of the first 5 images
    for idx, row in first_5_images.iterrows():
        form_id = row["form_id"]
        image_filename = row["processed_image"].split("processed_")[1]
        # Ensure correct source image extension per dataset
        name_no_ext, current_ext = os.path.splitext(image_filename)
        if dataset_name == "xfund":
            image_filename = f"{name_no_ext}.jpg"
        answer_bbox = row["answer_bbox"]
        question_text = row["question_text"]
        answer_text = row["answer_text"]

        # Use the appropriate input_images_dir based on dataset
        if input_images_dir is None:
            if dataset_name == "form-nlu":
                image_dir = "annotations/form-nlu/images"
                image_path = os.path.join(image_dir, image_filename)
            else:
                # Try both train and test directories for FUNSD/XFUND
                train_image_path = os.path.join(
                    f"tool/dataset/{dataset_name}_train/images", image_filename
                )
                test_image_path = os.path.join(
                    f"tool/dataset/{dataset_name}_test/images", image_filename
                )

                if os.path.exists(train_image_path):
                    image_path = train_image_path
                elif os.path.exists(test_image_path):
                    image_path = test_image_path
                else:
                    raise ValueError(
                        f"Image {image_filename} not found in either train or test directories"
                    )
        else:
            image_dir = input_images_dir
            image_path = os.path.join(image_dir, image_filename)
        temp_output_dir = os.path.join("tmp", dataset_name)
        os.makedirs(temp_output_dir, exist_ok=True)

        # Load image using PIL
        img = Image.open(image_path)
        img_array = np.array(img)

        # Convert to OpenCV format if needed
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        elif len(img_array.shape) == 3 and img_array.shape[2] == 3:  # RGB
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Draw bounding box
        if isinstance(answer_bbox, dict):
            # Handle dict format (form-nlu)
            x1, y1, x2, y2 = (
                int(answer_bbox["x1"]),
                int(answer_bbox["y1"]),
                int(answer_bbox["x2"]),
                int(answer_bbox["y2"]),
            )
        else:
            # Handle BoundingBox object format (FUNSD/XFUND)
            x1, y1, x2, y2 = (
                int(answer_bbox.x1),
                int(answer_bbox.y1),
                int(answer_bbox.x2),
                int(answer_bbox.y2),
            )

        # Draw rectangle
        cv2.rectangle(img_array, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Prepare text labels
        question_label = (
            f"Q: {question_text[:50]}{'...' if len(question_text) > 50 else ''}"
        )
        answer_label = f"A: {answer_text[:50]}{'...' if len(answer_text) > 50 else ''}"

        # Draw text labels with background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        # Question text
        (q_width, q_height), _ = cv2.getTextSize(
            question_label, font, font_scale, thickness
        )
        cv2.rectangle(
            img_array,
            (x1, y1 - q_height - 10),
            (x1 + q_width + 10, y1),
            (255, 255, 255),
            -1,
        )
        cv2.putText(
            img_array,
            question_label,
            (x1 + 5, y1 - 5),
            font,
            font_scale,
            (0, 0, 0),
            thickness,
        )

        # Answer text
        (a_width, a_height), _ = cv2.getTextSize(
            answer_label, font, font_scale, thickness
        )
        cv2.rectangle(
            img_array,
            (x1, y2 + 5),
            (x1 + a_width + 10, y2 + a_height + 15),
            (255, 255, 255),
            -1,
        )
        cv2.putText(
            img_array,
            answer_label,
            (x1 + 5, y2 + a_height + 10),
            font,
            font_scale,
            (0, 0, 0),
            thickness,
        )

        # Save annotated image
        output_filename = f"annotated_{form_id}_{image_filename}"
        output_path = os.path.join(temp_output_dir, output_filename)
        cv2.imwrite(output_path, img_array)

        print(f"Saved annotated image: {output_path}")

    # print(f"Saved {len(first_5_images)} annotated images to {temp_output_dir}")

>>>>>>> @{-1}

def main(dataset: str = "funsd") -> None:
    """
    Process either FUNSD or XFUND dataset based on the input parameter.

    Args:
        dataset: Name of the dataset to process ("funsd" or "xfund")
    """
    if dataset not in SUPPORTED_DATASETS:
        raise ValueError(f"Dataset must be one of {SUPPORTED_DATASETS}")

    # Setup directories
<<<<<<< HEAD
    annotations_dir = Path(f"tool/dataset/{dataset}/annotations")
    input_images_dir = f"tool/dataset/{dataset}/images"
    output_images_dir = "tool/dataset/processed/images"
    output_dir = "tool/dataset/processed"
=======
    if dataset == "form-nlu":
        input_images_dir = "annotations/form-nlu/images"
        output_images_dir = "tool/dataset/processed/images"
        output_dir = "tool/dataset/processed"
        train_annotations_file = "annotations/form-nlu/train.json"
        val_annotations_file = "annotations/form-nlu/val.json"
    else:
        # For funsd and xfund, we need to process both train and test splits
        train_annotations_dir = Path(f"tool/dataset/{dataset}_train/annotations")
        test_annotations_dir = Path(f"tool/dataset/{dataset}_test/annotations")
        train_input_images_dir = f"tool/dataset/{dataset}_train/images"
        test_input_images_dir = f"tool/dataset/{dataset}_test/images"
        output_images_dir = "tool/dataset/processed/images"
        output_dir = "tool/dataset/processed"
>>>>>>> @{-1}

    # Create output directories
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Process all JSON files
    all_pairs = []
    for json_file in tqdm(
        list(annotations_dir.glob("*.json")), desc="Processing JSON files"
    ):

        # # debugging
        # if "00836816" not in str(json_file):
        #     continue
        # try:
        with open(json_file, "r") as f:
            data = json.load(f)

<<<<<<< HEAD
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
=======
        # Process train split
        with open(train_annotations_file, "r") as f:
            train_annotations = json.load(f)
        train_pairs = process_form_nlu_annotations(
            train_annotations, input_images_dir, output_images_dir, "train"
        )

        # Process val split
        with open(val_annotations_file, "r") as f:
            val_annotations = json.load(f)
        val_pairs = process_form_nlu_annotations(
            val_annotations, input_images_dir, output_images_dir, "val"
        )

        # Combine all pairs and create proper train/test split
        all_pairs = train_pairs + val_pairs
        assert len(all_pairs) > 0

        print(
            f"Generated {len(train_pairs)} train QA pairs and {len(val_pairs)} test QA pairs"
        )
        print(f"Total QA pairs: {len(all_pairs)}")
    else:
        # Process FUNSD or XFUND datasets from both train and test directories
        all_pairs = []

        # Process both train and test splits
        for split_name, annotations_dir, input_images_dir in [
            ("test", test_annotations_dir, test_input_images_dir),
            ("train", train_annotations_dir, train_input_images_dir),
        ]:
            print(f"Processing {split_name} split from {annotations_dir}")

            for json_file in tqdm(
                list(annotations_dir.glob("*.json")),
                desc=f"Processing {split_name} JSON files",
            ):
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
                                (
                                    d,
                                    input_images_dir,
                                    output_images_dir,
                                    "jpg",
                                    json_file,
                                    dataset,
                                    split_name,
                                )
                                for d in dataset_items
                            ],
                        )
                        for pairs in results:
                            all_pairs.extend(pairs)
                else:
                    # Process FUNSD documents
                    pairs = process_document(
                        data,
                        input_images_dir,
                        output_images_dir,
                        "png",
                        json_file,
                        dataset,
                        split_name,
                    )
                    all_pairs.extend(pairs)
>>>>>>> @{-1}

    # Create and split dataset
    df = pd.DataFrame(all_pairs)
    unique_forms = df["form_id"].unique()
    np.random.shuffle(unique_forms)

<<<<<<< HEAD
    train_size = int(TRAIN_TEST_SPLIT_RATIO * len(unique_forms))
    train_forms = unique_forms[:train_size]
    test_forms = unique_forms[train_size:]
=======
    # drop duplicates where both the form_id and the question_text are the same
    print(
        f"Dropped {len(df) - len(df.drop_duplicates(subset=['form_id', 'question_text']))} duplicates"
    )
    df = df.drop_duplicates(subset=["form_id", "question_text"])
    # print how many duplicates were dropped

    if dataset == "form-nlu":
        # For form-nlu, split based on the split field
        train_forms = df[df["split"] == "train"]["form_id"].unique()
        test_forms = df[df["split"] == "val"]["form_id"].unique()

        print(
            f"Form-nlu split: {len(train_forms)} train forms, {len(test_forms)} test forms"
        )
    else:
        # For FUNSD/XFUND datasets, use the split field from directory structure
        train_forms = df[df["split"] == "train"]["form_id"].unique()
        test_forms = df[df["split"] == "test"]["form_id"].unique()

        print(
            f"{dataset.upper()} split: {len(train_forms)} train forms, {len(test_forms)} test forms"
        )
>>>>>>> @{-1}

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
