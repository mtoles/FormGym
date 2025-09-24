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
from dataclasses import dataclass
import shutil
from tqdm import tqdm

# import libcontent_aware_fill as cwf
from resynthesizer import resynthesize, TImageSynthParameters

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
SUPPORTED_DATASETS = ["funsd", "xfund", "form-nlu"]
DEFAULT_IMAGE_EXT = "png"
TRAIN_TEST_SPLIT_RATIO = 0.8
SHORT_DATASET_SIZE = 100


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


def apply_content_aware_fill(
    img: np.ndarray, mask: np.ndarray, output_path: str
) -> bool:
    """
    Apply content-aware fill to an image using a mask.

    Args:
        img: Input image as numpy array
        mask: Mask as numpy array (255 for areas to fill)
        output_path: Path to save the processed image

    Returns:
        True if successful, False otherwise
    """
    # Apply content-aware fill
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

    if filled_img is None:
        return False

    cv2.imwrite(output_path, filled_img)
    return True


def get_question_and_answer(
    entry: Dict,
    form_id: str,
    width: int,
    height: int,
    id_to_entry: Dict,
    processed_filename: str = None,
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
                        "processed_image": processed_filename
                        or f"processed_{form_id}.png",
                        "w": width,
                        "h": height,
                    }
                    return out_entry
        else:
            return None
    elif entry["label"] == "answer":
        out_entry = {
            "form_id": form_id,
            "question_text": get_full_question_text(entry, id_to_entry),
            "answer_text": entry["text"],
            "answer_bbox": BoundingBox.from_list(entry["box"]),
            "processed_image": processed_filename or f"processed_{form_id}.png",
            "w": width,
            "h": height,
        }
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
    # Add dataset prefix to processed image filename
    if dataset_name:
        processed_filename = f"{dataset_name}_processed_{form_id}.png"
    else:
        processed_filename = f"processed_{form_id}.png"
    output_image_path = os.path.join(output_images_dir, processed_filename)
    mask_bboxes = []
    # filled_img = img.copy()
    mask = np.zeros((height, width), dtype=np.uint8)
    for entry in doc:
        pair = get_question_and_answer(
            entry, form_id, width, height, id_to_entry, processed_filename
        )
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
    if not apply_content_aware_fill(img, mask, output_image_path):
        print(f"Could not fill image for {form_id} (no answers found?)")
        return []

    return pairs


def process_document(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
    dataset_name: str = None,
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
        doc, form_id, input_images_dir, output_images_dir, image_ext, dataset_name
    )


def process_form_nlu_synthetic_file(
    synthetic_file_path: str,
    annotations_data: Dict,
    input_images_dir: str,
    output_images_dir: str,
) -> List[Dict]:
    """
    Process a single form-nlu synthetic jsonl file and return QA pairs.

    Args:
        synthetic_file_path: Path to the synthetic jsonl file
        annotations_data: Dictionary containing annotations data
        input_images_dir: Directory containing input images
        output_images_dir: Directory to save processed images

    Returns:
        List of processed question-answer pairs
    """
    pairs = []

    # Extract form_id from the filename
    form_id = os.path.basename(synthetic_file_path).replace("_synthetic.jsonl", "")

    # print(f"Looking for image: {form_id}.png")

    # Find the image in annotations
    image_info = None
    for img in annotations_data["images"]:
        if img["file_name"] == form_id + ".png":
            image_info = img
            break

    if not image_info:
        print(
            f"Available images: {[img['file_name'] for img in annotations_data['images'][:5]]}"
        )
        print(f"Image {form_id}.png not found in annotations, skipping...")
        return []

    width = image_info["width"]
    height = image_info["height"]

    # Load input image
    input_image_path = os.path.join(input_images_dir, f"{form_id}.png")
    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError(f"Could not load image: {input_image_path}")

    # Create mask for content-aware fill
    mask = np.zeros((height, width), dtype=np.uint8)

    # Read synthetic data
    with open(synthetic_file_path, "r") as f:
        lines = f.readlines()

    # Process all lines (each line is a kv_pair)
    for line in lines:
        data = json.loads(line.strip())

        # # Only process QA type entries
        # if data.get("type") != "QA":
        #     continue

        question_text = data["key"]
        answer_text = data["value"]

        # Find matching annotation by text content
        answer_bbox = None
        for ann in annotations_data["annotations"]:
            if (
                ann["image_id"] == image_info["id"]
                and ann["text"].strip() == answer_text.strip()
            ):
                bbox = ann["bbox"]
                # print(f"Found exact match for '{answer_text}' with bbox: {bbox}")
                # Convert [x, y, width, height] to [x1, y1, x2, y2]
                answer_bbox = BoundingBox(
                    bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
                )
                break

        if answer_bbox is None:
            # If no exact match, try partial match
            for ann in annotations_data["annotations"]:
                if (
                    ann["image_id"] == image_info["id"]
                    and answer_text.strip() in ann["text"].strip()
                ):
                    bbox = ann["bbox"]
                    answer_bbox = BoundingBox(
                        bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
                    )
                    break

        if answer_bbox is None:
            # Skip if no bounding box found
            continue

        # Clip bbox to image bounds
        answer_bbox.clip_to_bounds(width, height)

        # Add to mask for content-aware fill
        # Ensure coordinates are integers
        y1, y2, x1, x2 = (
            int(answer_bbox.y1),
            int(answer_bbox.y2),
            int(answer_bbox.x1),
            int(answer_bbox.x2),
        )
        mask[y1:y2, x1:x2] = 255

        # Create QA pair
        pair = {
            "form_id": form_id,
            "question_text": question_text,
            "answer_text": answer_text,
            "answer_bbox": answer_bbox,
            "question_bbox": None,  # Always null for form-nlu
            "processed_image": f"processed_{form_id}.png",
            "w": width,
            "h": height,
        }
        pairs.append(pair)

    if len(pairs) == 0:
        return []

    # Apply content-aware fill
    output_image_path = os.path.join(output_images_dir, f"processed_{form_id}.png")
    if not apply_content_aware_fill(img, mask, output_image_path):
        print(f"Could not fill image for {form_id}")
        return []

    return pairs


def process_form_nlu_dataset(
    input_images_dir: str,
    output_images_dir: str,
    train_annotations_file: str,
    val_annotations_file: str,
) -> List[Dict]:
    """
    Process the entire form-nlu dataset.

    Args:
        input_images_dir: Directory containing input images
        output_images_dir: Directory to save processed images
        train_annotations_file: Path to train annotations JSON
        val_annotations_file: Path to val annotations JSON

    Returns:
        List of all processed question-answer pairs
    """
    all_pairs = []

    # Process both train and val splits
    for split, annotations_file in [
        ("train", train_annotations_file),
        ("val", val_annotations_file),
    ]:
        print(f"Processing {split} split from {annotations_file}")

        # Load annotation data
        with open(annotations_file, "r") as f:
            annotations = json.load(f)

        # Process annotations directly to create QA pairs
        pairs = process_form_nlu_annotations(
            annotations, input_images_dir, output_images_dir, split
        )
        all_pairs.extend(pairs)
        print(f"Generated {len(pairs)} QA pairs for {split} split")

    return all_pairs


def process_form_nlu_annotations(
    annotations: Dict, input_images_dir: str, output_images_dir: str, split: str
) -> List[Dict]:
    """
    Process form-nlu annotations using JSONL as primary data source and COCO for bbox validation.

    Args:
        annotations: COCO format annotations dictionary
        input_images_dir: Directory containing input images
        output_images_dir: Directory to save processed images
        split: Split name ("train" or "val")

    Returns:
        List of processed question-answer pairs
    """
    pairs = []

    # Create mapping from image_id to image info
    image_map = {img["id"]: img for img in annotations["images"]}
    print(f"Found {len(image_map)} images in annotations")
    # Group annotations by image_id
    annotations_by_image = {}
    for ann in annotations["annotations"]:
        image_id = ann["image_id"]
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)

    # Process each image
    for image_id, image_anns in tqdm(annotations_by_image.items()):
        if image_id not in image_map:
            continue

        image_info = image_map[image_id]
        image_filename = image_info["file_name"]
        form_id = f"{image_filename.replace('.png', '')}"

        # Process image if it exists
        input_image_path = os.path.join(input_images_dir, image_filename)
        if not os.path.exists(input_image_path):
            print(f"Warning: Image {input_image_path} not found, skipping")
            continue

        # Load input image and get dimensions
        img = cv2.imread(input_image_path)
        if img is None:
            print(f"Warning: Could not load image {input_image_path}, skipping")
            continue
        height, width = img.shape[:2]

        # Create mask for content-aware fill
        mask = np.zeros((height, width), dtype=np.uint8)

        # Load key-value pairs from JSONL (primary data source)
        jsonl_filename = f"{image_filename.replace('.png', '')}_synthetic.jsonl"
        jsonl_path = os.path.join("tool/dataset/form-nlu", jsonl_filename)

        if not os.path.exists(jsonl_path):
            print(
                f"Warning: JSONL file {jsonl_path} not found, skipping image {image_filename}"
            )
            continue

        # Load question-answer pairs from JSONL (new flexible format)
        qa_data = []
        with open(jsonl_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())

                # Determine question text
                question_parts = []
                if "section" in data and str(data["section"]).strip():
                    question_parts.append(str(data["section"]).strip())

                question_text = None
                if "key" in data and str(data["key"]).strip():
                    question_text = str(data["key"]).strip()
                else:
                    rc_parts = []
                    if "row" in data and str(data["row"]).strip():
                        rc_parts.append(str(data["row"]).strip())
                    if "column" in data and str(data["column"]).strip():
                        rc_parts.append(str(data["column"]).strip())
                    if rc_parts:
                        question_text = " | ".join(rc_parts)

                if question_text is None:
                    continue

                if "value" not in data:
                    continue

                answer_text = str(data["value"]).strip()
                if not answer_text:
                    continue

                if question_parts:
                    question_text = " | ".join(
                        [" | ".join(question_parts), question_text]
                    )

                qa_data.append({"question": question_text, "answer": answer_text})

        # Create mapping from answer text to bbox from COCO annotations
        answer_to_bbox = {}
        for ann in image_anns:
            text = ann["text"].strip()
            if text:
                bbox = ann["bbox"]
                # Convert bbox to [x1, y1, x2, y2] format
                x1, y1, w, h = bbox
                x2, y2 = x1 + w, y1 + h
                answer_to_bbox[text] = {
                    "x1": float(x1),
                    "y1": float(y1),
                    "x2": float(x2),
                    "y2": float(y2),
                }

        # Create QA pairs from JSONL data, checking bbox availability
        image_pairs = []
        for qa in qa_data:
            question_text = qa["question"]
            answer_text = qa["answer"]

            # Check if both question and answer have bboxes
            if answer_text not in answer_to_bbox:
                # print(
                #     f"Warning: Answer '{answer_text}' from JSONL not found in COCO annotations for {image_filename}"
                # )
                continue

            answer_bbox = answer_to_bbox[answer_text]

            # Add to mask for content-aware fill
            x1, y1, x2, y2 = (
                int(answer_bbox["x1"]),
                int(answer_bbox["y1"]),
                int(answer_bbox["x2"]),
                int(answer_bbox["y2"]),
            )
            # Ensure coordinates are within image bounds
            x1 = max(0, min(x1, width))
            y1 = max(0, min(y1, height))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            mask[y1:y2, x1:x2] = 255

            # Create QA pair
            qa_pair = {
                "form_id": form_id,
                "split": split,  # Add split information
                "question_text": question_text,
                "answer_text": answer_text,
                "answer_bbox": answer_bbox,
                "question_bbox": None,  # Could be populated if question bboxes exist
                "processed_image": f"form-nlu_processed_{image_filename}",
                "w": image_info["width"],
                "h": image_info["height"],
            }
            image_pairs.append(qa_pair)

        # Apply content-aware fill for this image if we have pairs
        if len(image_pairs) > 0:
            # Add dataset prefix to processed image filename
            output_image_filename = f"form-nlu_processed_{image_filename}"
            output_image_path = os.path.join(output_images_dir, output_image_filename)
            if not apply_content_aware_fill(img, mask, output_image_path):
                print(f"Could not fill image for {form_id}")
                continue
            pairs.extend(image_pairs)

    return pairs


def process_document_with_dirs(
    data: Dict,
    input_images_dir: str,
    output_images_dir: str,
    image_ext: str = DEFAULT_IMAGE_EXT,
    json_file: Optional[str] = None,
    dataset_name: str = None,
) -> List[Dict]:
    """Process a single document with directory paths."""
    return process_document(
        data, input_images_dir, output_images_dir, image_ext, json_file, dataset_name
    )


def save_dataset(
    df: pd.DataFrame,
    output_dir: str,
    dataset_name: str,
    train_forms: np.ndarray,
    test_forms: np.ndarray,
    save_short: bool = True,
    input_images_dir: str = None,
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
        os.path.join(output_dir, f"{dataset_name}_train_qa_pairs.jsonl"),
        orient="records",
        indent=2,
    )
    test_df.to_json(
        os.path.join(output_dir, f"{dataset_name}_test_qa_pairs.jsonl"),
        orient="records",
        indent=2,
    )

    if save_short:
        # Save short versions - select 100 unique documents, not 100 examples
        # Get unique form_ids from train set
        train_unique_forms = train_df["form_id"].unique()
        train_short_forms = train_unique_forms[:SHORT_DATASET_SIZE]
        train_short_df = train_df[train_df["form_id"].isin(train_short_forms)]

        # Get unique form_ids from test set
        test_unique_forms = test_df["form_id"].unique()
        test_short_forms = test_unique_forms[:SHORT_DATASET_SIZE]
        test_short_df = test_df[test_df["form_id"].isin(test_short_forms)]

        train_short_df.to_json(
            os.path.join(output_dir, f"{dataset_name}_train_qa_pairs_short.jsonl"),
            orient="records",
            indent=2,
        )
        test_short_df.to_json(
            os.path.join(output_dir, f"{dataset_name}_test_qa_pairs_short.jsonl"),
            orient="records",
            indent=2,
        )

    # save images of the first 5 images in the short test set.
    # draw the bounding boxes on the images  including text labels.

    # Get the first 5 images from the short test set
    if save_short:
        short_test_df = test_short_df
    else:
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
            elif dataset_name == "funsd":
                # For FUNSD, we need to find the image in either train or test split
                # Try train first, then test
                train_image_path = f"tool/dataset/funsd_train/images/{image_filename}"
                test_image_path = f"tool/dataset/funsd_test/images/{image_filename}"
                if os.path.exists(train_image_path):
                    image_dir = "tool/dataset/funsd_train/images"
                elif os.path.exists(test_image_path):
                    image_dir = "tool/dataset/funsd_test/images"
                else:
                    print(
                        f"Warning: Image {image_filename} not found in either train or test directories"
                    )
                    continue
            else:
                image_dir = f"tool/dataset/{dataset_name}/images"
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


def main(dataset: str = "funsd") -> None:
    """
    Process either FUNSD, XFUND, or form-nlu dataset based on the input parameter.

    Args:
        dataset: Name of the dataset to process ("funsd", "xfund", or "form-nlu")
    """
    if dataset not in SUPPORTED_DATASETS:
        raise ValueError(f"Dataset must be one of {SUPPORTED_DATASETS}")

    # Setup directories
    if dataset == "form-nlu":
        input_images_dir = "annotations/form-nlu/images"
        output_images_dir = "tool/dataset/processed/images"
        output_dir = "tool/dataset/processed"
        train_annotations_file = "annotations/form-nlu/train.json"
        val_annotations_file = "annotations/form-nlu/val.json"
    elif dataset == "funsd":
        # FUNSD has split directories, so we don't set a single input_images_dir
        input_images_dir = None
        output_images_dir = "tool/dataset/processed/images"
        output_dir = "tool/dataset/processed"
    else:
        annotations_dir = Path(f"tool/dataset/{dataset}/annotations")
        input_images_dir = f"tool/dataset/{dataset}/images"
        output_images_dir = "tool/dataset/processed/images"
        output_dir = "tool/dataset/processed"

    # Create output directories
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Process dataset
    if dataset == "form-nlu":
        # Process form-nlu dataset
        print(f"Processing form-nlu dataset...")
        print(f"Input images dir: {input_images_dir}")
        print(f"Train annotations: {train_annotations_file}")
        print(f"Val annotations: {val_annotations_file}")

        # Process train and val separately to create proper split files
        train_pairs = []
        val_pairs = []

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
    elif dataset == "funsd":
        # Process FUNSD dataset with train/test splits
        print(f"Processing FUNSD dataset...")
        all_pairs = []

        # Process both train and test splits
        for split in ["train", "test"]:
            split_annotations_dir = Path(f"tool/dataset/funsd_{split}/annotations")
            split_images_dir = f"tool/dataset/funsd_{split}/images"

            print(f"Processing {split} split from {split_annotations_dir}")

            if not split_annotations_dir.exists():
                print(f"Warning: {split_annotations_dir} does not exist, skipping")
                continue

            for json_file in tqdm(
                list(split_annotations_dir.glob("*.json")),
                desc=f"Processing {split} JSON files",
            ):
                with open(json_file, "r") as f:
                    data = json.load(f)

                # Process FUNSD documents
                pairs = process_document(
                    data, split_images_dir, output_images_dir, "png", json_file, dataset
                )
                all_pairs.extend(pairs)

            print(
                f"Generated {len([p for p in all_pairs if p.get('split') == split])} QA pairs for {split} split"
            )
    else:
        # Process XFUND datasets
        all_pairs = []
        for json_file in tqdm(
            list(annotations_dir.glob("*.json")),
            desc="Processing JSON files",
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
                            )
                            for d in dataset_items
                        ],
                    )
                    for pairs in results:
                        all_pairs.extend(pairs)
            else:
                # Process other datasets
                pairs = process_document(
                    data, input_images_dir, output_images_dir, "png", json_file, dataset
                )
                all_pairs.extend(pairs)

    # Create and split dataset
    df = pd.DataFrame(all_pairs)

    # Debug: Print DataFrame info
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns.tolist()}")
    if len(df) > 0:
        print(f"First few rows:")
        print(df.head())
    else:
        print("Warning: No data was processed! Check your dataset paths and structure.")
        return

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
        # For other datasets, use the standard split
        unique_forms = df["form_id"].unique()
        np.random.shuffle(unique_forms)
        train_size = int(TRAIN_TEST_SPLIT_RATIO * len(unique_forms))
        train_forms = unique_forms[:train_size]
        test_forms = unique_forms[train_size:]

    # Save datasets
    save_dataset(
        df,
        output_dir,
        dataset,
        train_forms,
        test_forms,
        input_images_dir=input_images_dir,
    )

    # Log statistics
    logger.info(f"Processed {len(df)} question-answer pairs")
    logger.info(f"Train set size: {len(df[df['form_id'].isin(train_forms)])}")
    logger.info(f"Test set size: {len(df[df['form_id'].isin(test_forms)])}")
    logger.info(f"Saved processed images to {output_images_dir}")
    logger.info(f"Saved QA pairs to {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process FUNSD, XFUND, or form-nlu dataset"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        choices=SUPPORTED_DATASETS,
        default="funsd",
        help="Dataset to process (funsd, xfund, or form-nlu)",
    )
    args = parser.parse_args()
    main(args.dataset)
