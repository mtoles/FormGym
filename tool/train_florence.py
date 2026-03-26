import os
import torch
from datasets import load_dataset, disable_caching
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoProcessor,
    AutoConfig,
    get_scheduler,
)
from torch.optim import AdamW
import random
import json
from PIL import Image, ImageDraw
import numpy as np
import os
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import get_scheduler
import wandb
from datetime import datetime
import argparse
import yaml
from pathlib import Path
import pandas as pd  # Add pandas import
import matplotlib.pyplot as plt
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import sys

# set all random seeds
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True


print(os.environ["CUDA_HOME"])
print(os.environ["LD_LIBRARY_PATH"])
print(torch.cuda.is_available())
# assert torch.cuda.is_available()  # not available in debug mode, dunno why

TASK_NAME_PREFIX = "<OPEN_VOCABULARY_DETECTION>"  # config["task_name_prefix"]
TEXT_INPUT_PROMPT_TEMPLATE = (
    TASK_NAME_PREFIX + "text entry field corresponding to {target}"
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class FormGymDataset(Dataset):
    def __init__(
        self,
        json_path: str,
        max_examples_per_image: int = sys.maxsize,
        max_size: int = None,
    ):
        self.image_dir = "tool/dataset/processed/images"
        # Load data - the .jsonl files are actually JSON arrays, not true JSONL
        with open(json_path, "r") as f:
            raw_data = json.load(f)

        # Shuffle the data
        random.shuffle(raw_data)

        # Group examples by image file
        image_groups = {}
        for example in raw_data:
            image_path = example["processed_image"]
            # image_prefix = "_".join(image_path.split("_")[:-1])
            if image_path not in image_groups:
                image_groups[image_path] = []
            image_groups[image_path].append(example)

        # Keep at most max_examples_per_image examples per image
        self.data = []
        for image_path, examples in image_groups.items():
            if max_examples_per_image is not None:
                examples = examples[:max_examples_per_image]
            self.data.extend(examples)
        print(f"Total examples reduced from {len(raw_data)} to {len(self.data)}")
        # Apply downsampling if max_size is specified
        if max_size is not None and max_size < len(self.data):
            self.data = random.sample(self.data, max_size)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        example = self.data[idx]
        w = example["w"]
        h = example["h"]
        bbox = example["answer_bbox"]
        x1 = str(int(bbox["x1"] / w * 1000))
        y1 = str(int(bbox["y1"] / h * 1000))
        x2 = str(int(bbox["x2"] / w * 1000))
        y2 = str(int(bbox["y2"] / h * 1000))
        question = TEXT_INPUT_PROMPT_TEMPLATE.format(target=example["question_text"])
        image_path = os.path.join(self.image_dir, f"{example['processed_image']}")
        image = Image.open(image_path).convert("RGB")
        image = np.array(image)
        # first_answer = str(example["answer_bbox"])
        label = f"{example['question_text']}<loc_{x1}><loc_{y1}><loc_{x2}><loc_{y2}>"

        return question, label, image, bbox, image_path


def load_config(args, actions):
    """Load configuration from YAML file and override with command line arguments"""
    config_path = args.config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Convert values to proper types based on argument parser types
    # for action in parser._actions:
    for action in actions:
        if action.dest in config and action.type is not None:
            config[action.dest] = action.type(config[action.dest])

    # if override_args:
    # Update config with command line arguments
    for key, value in vars(args).items():
        if value is not None:  # Remove the key in config check to allow new keys
            config[key] = value

    return config


def calculate_iou(bbox1, bbox2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.
    Bounding boxes are expected in format [x1, y1, x2, y2]
    """
    if bbox1 is None or bbox2 is None:
        return 0
    # Calculate intersection area
    x1 = max(bbox1["x1"], bbox2["x1"])
    y1 = max(bbox1["y1"], bbox2["y1"])
    x2 = min(bbox1["x2"], bbox2["x2"])
    y2 = min(bbox1["y2"], bbox2["y2"])

    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)

    # Calculate union area
    bbox1_area = (bbox1["x2"] - bbox1["x1"]) * (bbox1["y2"] - bbox1["y1"])
    bbox2_area = (bbox2["x2"] - bbox2["x1"]) * (bbox2["y2"] - bbox2["y1"])
    union_area = bbox1_area + bbox2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area if union_area > 0 else 0
    return iou


def calculate_inside_accuracy(pred_bbox, gt_bbox):
    """
    Calculate if the predicted bounding box is completely inside the target box.
    Returns 1 if pred_bbox is completely inside gt_bbox, 0 otherwise.
    Bounding boxes are expected in format [x1, y1, x2, y2]
    """
    if pred_bbox is None or gt_bbox is None:
        return 0

    # Check if center of predicted box is completely inside ground truth box
    pred_center_x = (pred_bbox["x1"] + pred_bbox["x2"]) / 2
    pred_center_y = (pred_bbox["y1"] + pred_bbox["y2"]) / 2
    inside = (
        pred_center_x >= gt_bbox["x1"]
        and pred_center_y >= gt_bbox["y1"]
        and pred_center_x <= gt_bbox["x2"]
        and pred_center_y <= gt_bbox["y2"]
    )

    return 1 if inside else 0


def collate_fn(batch, processor):
    questions, answers, images, bboxes, image_paths = zip(*batch)
    inputs = processor(
        text=list(questions),
        images=list(images),
        return_tensors="pt",
        padding=True,
    ).to(device)
    # Get image dimensions (width, height) for each image
    widths = [img.shape[1] for img in images]
    heights = [img.shape[0] for img in images]
    return inputs, answers, widths, heights, bboxes, image_paths


def calculate_loss(model, data_loader, processor):
    """Calculate the loss for the entire dataset"""
    model.eval()
    total_loss = 0
    num_batches = 0
    print(f"Calculating loss for {len(data_loader)} batches")

    with torch.no_grad():
        for batch_idx, (
            inputs,
            answers,
            widths,
            heights,
            gt_bboxes,
            image_paths,
        ) in tqdm(enumerate(data_loader)):
            # Calculate loss for the batch
            labels = processor.tokenizer(
                text=answers,
                return_tensors="pt",
                padding=True,
                padding_side="left",
                return_token_type_ids=False,
            ).input_ids.to(device)
            loss_outputs = model(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                labels=labels,
            )
            total_loss += loss_outputs.loss.item()
            num_batches += 1

    avg_loss = total_loss / num_batches if num_batches > 0 else 0
    return avg_loss


def calculate_iou_accuracy(
    model, data_loader, processor, max_iou_examples=None, dataset_name=None
):
    """Calculate IoU accuracy for the first max_examples examples"""
    # if max_iou_examples is None:
    #     max_iou_examples = MAX_IOU_EXAMPLES
    model.eval()
    total_iou = 0
    total_inside_acc = 0
    num_samples = 0
    predictions_data = []

    # Calculate total number of examples for progress bar
    total_examples = len(data_loader.dataset)
    if max_iou_examples is not None:
        total_examples = min(total_examples, max_iou_examples)

    with torch.no_grad():
        for batch_idx, (
            inputs,
            answers,
            widths,
            heights,
            gt_bboxes,
            image_paths,
        ) in enumerate(
            tqdm(
                data_loader,
                desc=f"Evaluating ({total_examples} examples)",
                total=len(data_loader),
            )
        ):
            if max_iou_examples is not None and num_samples >= max_iou_examples:
                break

            input_text = processor.batch_decode(
                inputs["input_ids"], skip_special_tokens=False
            )
            batch_size = len(input_text)

            # Get decoder start tokens for the entire batch
            decoder_input_ids = torch.tensor(
                [[model.config.text_config.bos_token_id]] * batch_size, device=device
            )
            current_ids = decoder_input_ids
            max_length = 64

            # Generate tokens one by one for the entire batch
            generated_ids_list = [[] for _ in range(batch_size)]
            still_generating = [True for _ in range(batch_size)]
            for _ in range(max_length):
                outputs = model(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    decoder_input_ids=current_ids,
                )

                # Get the next tokens for the entire batch
                next_tokens = outputs.logits[:, -1, :].argmax(dim=-1).unsqueeze(-1)

                # Update generated IDs and check for EOS tokens
                for i in range(batch_size):
                    if (
                        len(generated_ids_list[i]) == 0
                        or generated_ids_list[i][-1]
                        != model.config.text_config.eos_token_id
                    ):
                        generated_ids_list[i].append(next_tokens[i].item())
                    if (
                        generated_ids_list[i][-1]
                        == model.config.text_config.eos_token_id
                    ):
                        still_generating[i] = False

                # Check if all sequences have reached EOS
                if all(
                    len(ids) > 0 and ids[-1] == model.config.text_config.eos_token_id
                    for ids in generated_ids_list
                ):
                    break

                # Update input for next iteration
                print(f"token no: {current_ids.shape[1]}", end="\r")
                current_ids = torch.cat([current_ids, next_tokens], dim=-1)

                if not any(still_generating):
                    break

            # Process each sample in the batch
            generated_texts = processor.batch_decode(
                generated_ids_list, skip_special_tokens=False
            )

            for i, generated_text in enumerate(generated_texts):

                parsed_answer = processor.post_process_generation(
                    generated_text,
                    task=TASK_NAME_PREFIX,
                    image_size=(widths[i], heights[i]),
                )
                parsed_bboxes = parsed_answer[TASK_NAME_PREFIX]["bboxes"]
                pred_bboxes = [
                    {
                        "x1": float(bbox[0]) / 1000,
                        "y1": float(bbox[1]) / 1000,
                        "x2": float(bbox[2]) / 1000,
                        "y2": float(bbox[3]) / 1000,
                    }
                    for bbox in parsed_bboxes
                ]
                gt_bbox = {
                    "x1": float(gt_bboxes[i]["x1"]) / 1000,
                    "y1": float(gt_bboxes[i]["y1"]) / 1000,
                    "x2": float(gt_bboxes[i]["x2"]) / 1000,
                    "y2": float(gt_bboxes[i]["y2"]) / 1000,
                }

                if len(pred_bboxes) == 0:
                    pred_bbox = None  # always wrong
                else:
                    pred_bbox = pred_bboxes[0]

                # Calculate IoU and inside accuracy
                iou = calculate_iou(pred_bbox, gt_bbox)
                inside_acc = calculate_inside_accuracy(pred_bbox, gt_bbox)
                total_iou += iou
                total_inside_acc += inside_acc

                # Store data for DataFrame
                predictions_data.append(
                    {
                        "input_text": input_text[i],
                        "generated_text": generated_text,
                        "ground_truth_bbox": gt_bboxes[i],
                        "predicted_bbox": pred_bbox,
                        "iou": iou,
                        "inside_accuracy": inside_acc,
                        "dataset_name": dataset_name,
                        "image_width": widths[i],
                        "image_height": heights[i],
                        "pixel_values": inputs["pixel_values"][i].cpu().numpy(),
                        "answer": answers[i],
                        "image_path": image_paths[i],
                    }
                )

                num_samples += 1

    avg_iou = total_iou / num_samples if num_samples > 0 else 0
    avg_inside_acc = total_inside_acc / num_samples if num_samples > 0 else 0
    return avg_iou, avg_inside_acc, predictions_data


def evaluate_per_dataset(model, val_datasets, config, processor, max_iou_examples=None):
    """Evaluate model on each dataset separately and log per-dataset metrics to wandb"""
    per_dataset_metrics = {}
    all_predictions_data = []

    for i, dataset in enumerate(val_datasets):
        dataset_name = os.path.basename(config["eval_paths"][i]).replace(
            "_test_qa_pairs.jsonl", ""
        )
        print(f"Evaluating on {dataset_name} dataset...")

        # Create data loader for this dataset
        dataset_loader = DataLoader(
            dataset,
            batch_size=config["val_batch_size"],
            collate_fn=lambda batch: collate_fn(batch, processor),
            num_workers=config["num_workers"],
        )

        # Evaluate on this dataset
        avg_iou, avg_inside_acc, predictions_data = calculate_iou_accuracy(
            model, dataset_loader, processor, max_iou_examples, dataset_name
        )

        # Store metrics
        per_dataset_metrics[dataset_name] = {
            "iou": avg_iou,
            "inside_accuracy": avg_inside_acc,
            "num_samples": len(predictions_data),
        }

        # Add to all predictions data
        all_predictions_data.extend(predictions_data)

        # Log per-dataset metrics to wandb
        wandb.log(
            {
                f"accuracy/{dataset_name}_iou": avg_iou,
                f"accuracy/{dataset_name}_inside_acc": avg_inside_acc,
                f"dataset/{dataset_name}_eval_samples": len(predictions_data),
            }
        )

        print(f"{dataset_name} - IoU: {avg_iou:.4f}, Inside Acc: {avg_inside_acc:.4f}")

    # Calculate overall metrics
    overall_iou = sum(
        [metrics["iou"] for metrics in per_dataset_metrics.values()]
    ) / len(per_dataset_metrics)
    overall_inside_acc = sum(
        [metrics["inside_accuracy"] for metrics in per_dataset_metrics.values()]
    ) / len(per_dataset_metrics)

    # Log overall metrics
    wandb.log(
        {
            "accuracy/overall_iou": overall_iou,
            "accuracy/overall_inside_acc": overall_inside_acc,
        }
    )

    print(f"Overall - IoU: {overall_iou:.4f}, Inside Acc: {overall_inside_acc:.4f}")

    return per_dataset_metrics, all_predictions_data


def manage_checkpoints(checkpoint_dir, max_checkpoints=4):
    """Keep only the max_checkpoints most recent checkpoints in the directory."""
    # Get all checkpoint directories
    checkpoint_dirs = [
        d
        for d in os.listdir(checkpoint_dir)
        if os.path.isdir(os.path.join(checkpoint_dir, d))
    ]

    # Sort by modification time (newest first)
    checkpoint_dirs.sort(
        key=lambda x: os.path.getmtime(os.path.join(checkpoint_dir, x)), reverse=True
    )

    # Delete older checkpoints
    for old_checkpoint in checkpoint_dirs[max_checkpoints:]:
        old_path = os.path.join(checkpoint_dir, old_checkpoint)
        print(f"Deleting old checkpoint: {old_path}")
        import shutil

        shutil.rmtree(old_path)


def load_from_checkpoint(checkpoint_path, device):
    try:
        model_config = AutoConfig.from_pretrained(
            "microsoft/Florence-2-large-ft",
            trust_remote_code=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint_path, trust_remote_code=True, config=model_config
        ).to(device)
        processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-large-ft", trust_remote_code=True
        )
    except Exception as e:
        print(f"Error loading model from checkpoint: {e}")
        return None, None
    return processor, model


# Main execution code starts here
# Load configuration


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Train form filler model")
    parser.add_argument(
        "--config",
        type=str,
        default="tool/config.yaml",
        help="Path to configuration YAML file",
    )
    parser.add_argument(
        "--train_paths",
        type=list,
        help="Path to training data JSON file (overrides config)",
        nargs="+",
    )
    parser.add_argument(
        "--eval_paths",
        type=str,
        help="Path to evaluation data JSON file (overrides config)",
        nargs="+",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs (overrides config)",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        help="Learning rate for training (overrides config)",
    )
    parser.add_argument(
        "--train_batch_size",
        type=int,
        help="Training batch size (overrides config)",
    )
    parser.add_argument(
        "--val_batch_size",
        type=int,
        help="Validation batch size (overrides config)",
    )
    parser.add_argument(
        "--epochs_per_eval",
        type=float,
        help="Number of epochs between evaluations (overrides config)",
    )
    parser.add_argument(
        "--load_checkpoint_from",
        type=str,
        help="Path to checkpoint to load from (overrides config)",
    )
    parser.add_argument(
        "--train_size",
        type=int,
        help="Number of samples to use for training (overrides config)",
    )
    parser.add_argument(
        "--val_size",
        type=int,
        help="Number of samples to use for validation (overrides config)",
    )
    parser.add_argument(
        "--note",
        type=str,
        help="A note to be logged to wandb and included in save paths",
    )
    parser.add_argument(
        "--use_peft",
        type=bool,
        help="Whether to use PEFT (overrides config)",
    )
    parser.add_argument(
        "--max_iou_examples",
        type=int,
        help="Number of examples to use for IoU calculation (overrides config)",
    )
    parser.add_argument(
        "--max_examples_per_image",
        type=int,
        help="Maximum number of examples to use per image (overrides config)",
    )
    args = parser.parse_args()
    config = load_config(args, parser._actions)

    # Configuration
    TRAIN_BATCH_SIZE = config["train_batch_size"]
    VAL_BATCH_SIZE = config["val_batch_size"]
    NUM_WORKERS = config["num_workers"]
    EPOCHS = config["epochs"]
    LEARNING_RATE = config["learning_rate"]
    MODEL_NAME = config["model_name"]
    # MODEL_REVISION = config["model_revision"]
    EPOCHS_PER_EVAL = config["epochs_per_eval"]
    CHECKPOINT_DIR = config["checkpoint_dir"]
    LOAD_CHECKPOINT_FROM = config.get("load_checkpoint_from", None)
    TRAIN_SIZE = config.get("train_size", None)
    VAL_SIZE = config.get("val_size", None)
    NOTE = config.get("note", "")  # Get note from config, default to empty string
    MAX_IOU_EXAMPLES = config.get(
        "max_iou_examples", None
    )  # Get max_iou_examples from config
    MAX_EXAMPLES_PER_IMAGE = config.get(
        "max_examples_per_image"
    )  # Get max_examples_per_image from config
    # Override with command line arguments if provided
    if args.train_size is not None:
        TRAIN_SIZE = args.train_size
    if args.val_size is not None:
        VAL_SIZE = args.val_size
    if args.note is not None:
        NOTE = args.note
    if args.max_iou_examples is not None:
        MAX_IOU_EXAMPLES = args.max_iou_examples
    if args.val_batch_size is not None:
        VAL_BATCH_SIZE = args.val_batch_size

    # Create a unique run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"train_tool_{timestamp}"
    if NOTE:
        run_name = f"{run_name}_{NOTE.replace(' ', '_')}"

    run = wandb.init(project="form-filler", name=run_name, config=config)

    disable_caching()

    # Load model from checkpoint if specified, otherwise load from pretrained
    if LOAD_CHECKPOINT_FROM:
        processor, model = load_from_checkpoint(LOAD_CHECKPOINT_FROM, device=device)
        print(f"Loading model from checkpoint: {LOAD_CHECKPOINT_FROM}")

    else:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True
        ).to(device)
        processor = AutoProcessor.from_pretrained(MODEL_NAME, trust_remote_code=True)

    for param in model.vision_tower.parameters():
        param.is_trainable = False

    train_dataset = ConcatDataset(
        [
            FormGymDataset(
                path, max_size=TRAIN_SIZE, max_examples_per_image=MAX_EXAMPLES_PER_IMAGE
            )
            for path in config["train_paths"]
        ]
    )

    # Load each validation dataset separately with different max_examples_per_image
    val_datasets = []
    for path in config["eval_paths"]:
        if "form-nlu" in path:
            max_examples = None
        elif "funsd" in path:
            max_examples = None
        elif "xfund" in path:
            max_examples = None
        else:
            raise ValueError("No such dataset")

        val_datasets.append(
            FormGymDataset(
                path,
                max_size=VAL_SIZE,
                max_examples_per_image=max_examples,
            )
        )

    val_dataset = ConcatDataset(val_datasets)

    # Log dataset sizes to wandb
    print("Dataset sizes:")
    print(f"Training dataset: {len(train_dataset)} examples")
    wandb.log({"dataset/train_size": len(train_dataset)})

    print(f"Validation dataset: {len(val_dataset)} examples")
    wandb.log({"dataset/val_size": len(val_dataset)})

    # Log per-dataset validation sizes
    for i, path in enumerate(config["eval_paths"]):
        dataset_name = os.path.basename(path).replace("_test_qa_pairs.jsonl", "")
        dataset_size = len(val_datasets[i])
        print(f"  {dataset_name}: {dataset_size} examples")
        wandb.log({f"dataset/val_{dataset_name.lower()}_size": dataset_size})

    # Log per-dataset training sizes
    train_dataset_sizes = []
    for i, path in enumerate(config["train_paths"]):
        dataset_name = os.path.basename(path).replace("_train_qa_pairs.jsonl", "")
        # Get individual dataset size by creating a temporary dataset
        temp_dataset = FormGymDataset(
            path, max_size=TRAIN_SIZE, max_examples_per_image=MAX_EXAMPLES_PER_IMAGE
        )
        dataset_size = len(temp_dataset)
        train_dataset_sizes.append(dataset_size)
        print(f"  {dataset_name}: {dataset_size} examples")
        wandb.log({f"dataset/train_{dataset_name.lower()}_size": dataset_size})

    print()

    train_loader = DataLoader(
        train_dataset,
        batch_size=TRAIN_BATCH_SIZE,
        collate_fn=lambda batch: collate_fn(batch, processor),
        num_workers=NUM_WORKERS,
        shuffle=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=VAL_BATCH_SIZE,
        collate_fn=lambda batch: collate_fn(batch, processor),
        num_workers=NUM_WORKERS,
    )

    # Initialize optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    num_training_steps = EPOCHS * len(train_loader)
    lr_scheduler = get_scheduler(
        name="cosine",
        optimizer=optimizer,
        num_warmup_steps=int(0.05 * num_training_steps),
        num_training_steps=num_training_steps,
    )

    # Load optimizer and scheduler states if they exist
    if LOAD_CHECKPOINT_FROM:
        states_path = os.path.join(LOAD_CHECKPOINT_FROM, "training_states.pt")
        if os.path.exists(states_path):
            print("Loading optimizer and scheduler states...")
            checkpoint = torch.load(states_path)
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            lr_scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
            batch_no = checkpoint["batch_no"]
            total_batches = checkpoint["total_batches"]
            print(f"Resuming from epoch {checkpoint['epoch']}, batch {batch_no}")

    # Apply PEFT if configured
    if config.get("use_peft", False):
        print("Applying PEFT configuration...")
        peft_config = LoraConfig(**config["peft_config"])

        # First prepare the model for k-bit training
        model = prepare_model_for_kbit_training(model)

        # Get PEFT model
        model = get_peft_model(model, peft_config)

        # Freeze all parameters except LoRA parameters
        for name, param in model.named_parameters():
            if "lora" not in name.lower():
                param.requires_grad = False

        # Print trainable parameters
        model.print_trainable_parameters()

        # Verify that only LoRA parameters are trainable
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        print(f"Trainable parameters: {trainable_params}")
        print(f"Total parameters: {total_params}")
        print(
            f"Percentage of trainable parameters: {100 * trainable_params / total_params:.2f}%"
        )

    batch_no = -1
    val_accuracy, val_loss, predictions_df = None, None, None
    total_batches = 0
    batches_per_epoch = len(train_loader)
    for epoch in tqdm(range(EPOCHS), desc="Training Epochs"):
        model.train()
        train_loss = 0
        for inputs, answers, widths, heights, bboxes, image_paths in tqdm(
            train_loader, desc=f"Training Epoch {epoch + 1}/{EPOCHS}"
        ):
            batch_no += 1
            total_batches += 1
            input_ids = inputs["input_ids"]
            pixel_values = inputs["pixel_values"]
            labels = processor.tokenizer(
                text=answers,
                return_tensors="pt",
                padding=True,
                padding_side="left",
                return_token_type_ids=False,
            ).input_ids.to(device)
            outputs = model(
                input_ids=input_ids, pixel_values=pixel_values, labels=labels
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            train_loss += loss.item()

            # Log batch-level metrics
            wandb.log(
                {
                    "loss/train_loss": loss.item(),
                    "config/learning_rate": lr_scheduler.get_last_lr()[0],
                    "config/epoch": epoch,
                    "config/batch": batch_no,
                }
            )

            # Evaluate every N batches
            if (
                batch_no % int(EPOCHS_PER_EVAL * batches_per_epoch) == 0
                and batch_no != 0
            ) or batch_no == EPOCHS * batches_per_epoch - 1:
                val_loss = calculate_loss(model, val_loader, processor)
                per_dataset_metrics, all_predictions_data = evaluate_per_dataset(
                    model, val_datasets, config, processor, MAX_IOU_EXAMPLES
                )
                predictions_df = pd.DataFrame(all_predictions_data)

                # Calculate overall metrics for logging
                overall_iou = sum(
                    [metrics["iou"] for metrics in per_dataset_metrics.values()]
                ) / len(per_dataset_metrics)
                overall_inside_acc = sum(
                    [
                        metrics["inside_accuracy"]
                        for metrics in per_dataset_metrics.values()
                    ]
                ) / len(per_dataset_metrics)

                print(f"Validation IoU: {overall_iou}")
                print(f"Validation Inside Acc: {overall_inside_acc}")
                print(f"Validation Loss: {val_loss}")
                wandb.log(
                    {
                        "accuracy/val_iou": overall_iou,
                        "accuracy/overall_inside_acc": overall_inside_acc,
                        "loss/val_loss": val_loss,
                    }
                )

                # Save model checkpoint after evaluation
                current_epoch_fraction = total_batches / batches_per_epoch
                checkpoint_path = os.path.join(
                    CHECKPOINT_DIR,
                    timestamp,
                    f"model_epoch_{current_epoch_fraction:.2f}",
                )
                if NOTE:
                    checkpoint_path = f"{checkpoint_path}_{NOTE.replace(' ', '_')}"
                os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
                print(f"Saving model checkpoint to {checkpoint_path}")

                # Save optimizer and scheduler states
                model.save_pretrained(checkpoint_path)
                torch.save(
                    {
                        "optimizer_state_dict": optimizer.state_dict(),
                        "scheduler_state_dict": lr_scheduler.state_dict(),
                        "epoch": epoch,
                        "batch_no": batch_no,
                        "total_batches": total_batches,
                    },
                    os.path.join(checkpoint_path, "training_states.pt"),
                )
                print(f"Model checkpoint saved successfully")

                # Manage checkpoints to keep only the 4 most recent ones
                manage_checkpoints(
                    os.path.join(CHECKPOINT_DIR, timestamp), max_checkpoints=4
                )

        avg_train_loss = train_loss / len(train_loader)
        print(f"Average Training Loss: {avg_train_loss}")
        wandb.log(
            {
                "loss/train_loss": avg_train_loss,
                "config/learning_rate": lr_scheduler.get_last_lr()[0],
                "config/epoch": epoch,
            }
        )

    # visualize the model's predictions
    os.makedirs(f"tmp/tool/{timestamp}", exist_ok=True)
    if predictions_df is None:
        val_loss = calculate_loss(model, val_loader, processor)
        per_dataset_metrics, all_predictions_data = evaluate_per_dataset(
            model, val_datasets, config, processor, MAX_IOU_EXAMPLES
        )
        predictions_df = pd.DataFrame(all_predictions_data)

        # Calculate overall metrics for logging
        overall_iou = sum(
            [metrics["iou"] for metrics in per_dataset_metrics.values()]
        ) / len(per_dataset_metrics)
        overall_inside_acc = sum(
            [metrics["inside_accuracy"] for metrics in per_dataset_metrics.values()]
        ) / len(per_dataset_metrics)

        wandb.log(
            {
                "accuracy/val_iou": overall_iou,
                "accuracy/overall_inside_acc": overall_inside_acc,
                "loss/val_loss": val_loss,
            }
        )
    for index, row in predictions_df.iterrows():
        # Load the actual image file
        image = Image.open(row["image_path"]).convert("RGB")
        draw = ImageDraw.Draw(image)

        # Draw ground truth box in green
        gt_bbox = row["ground_truth_bbox"]
        draw.rectangle(
            [gt_bbox["x1"], gt_bbox["y1"], gt_bbox["x2"], gt_bbox["y2"]],
            outline="green",
            width=2,
        )
        label = row.answer.split("<")[0]
        draw.text((gt_bbox["x1"], gt_bbox["y1"]), label, fill="green")

        # Draw predicted box in red
        if row["predicted_bbox"] is not None:
            pred_bbox = row["predicted_bbox"]
            # ensure x_1 < x_2 and y_1 < y_2
            ordered_pred_bbox = [
                min(pred_bbox["x1"], pred_bbox["x2"]),
                min(pred_bbox["y1"], pred_bbox["y2"]),
                max(pred_bbox["x1"], pred_bbox["x2"]),
                max(pred_bbox["y1"], pred_bbox["y2"]),
            ]
            draw.rectangle(ordered_pred_bbox, outline="red", width=2)
        else:
            # Draw text when predicted bbox is None
            draw.text((10, 10), "pred bbox is none", fill="red")

        # Save the image
        output_path = f"tmp/tool/prediction_{index}.png"
        image.save(output_path)


if __name__ == "__main__":
    main()
