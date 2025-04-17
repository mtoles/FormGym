import os
import torch
from datasets import load_dataset, disable_caching
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoProcessor,
    AdamW,
    get_scheduler,
    AutoConfig,
)
import json
from PIL import Image, ImageDraw
import numpy as np
import os
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AdamW, get_scheduler
import wandb
from datetime import datetime
import argparse
import yaml
from pathlib import Path
import pandas as pd  # Add pandas import
import matplotlib.pyplot as plt
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

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
    "--eval_path",
    type=str,
    help="Path to evaluation data JSON file (overrides config)",
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
args = parser.parse_args()


class FormGymDataset(Dataset):
    def __init__(
        self, json_path: str, drop_duplicates: bool = False, max_size: int = None
    ):
        self.image_dir = "tool/dataset/processed/images"
        with open(json_path, "r") as f:
            raw_data = json.load(f)

        if drop_duplicates:
            # Filter to keep only first example per form_id
            seen_forms = set()
            self.data = []
            for example in raw_data:
                form_id = example["form_id"]
                if form_id not in seen_forms:
                    seen_forms.add(form_id)
                    self.data.append(example)
        else:
            self.data = raw_data

        # Apply downsampling if max_size is specified
        if max_size is not None and max_size < len(self.data):
            import random

            random.seed(42)  # For reproducibility
            self.data = random.sample(self.data, max_size)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        example = self.data[idx]
        w = example["w"]
        h = example["h"]
        bbox = example["answer_bbox"]
        x1 = str(int(bbox[0] / w * 1000))
        y1 = str(int(bbox[1] / h * 1000))
        x2 = str(int(bbox[2] / w * 1000))
        y2 = str(int(bbox[3] / h * 1000))
        question = f"{TASK_NAME_PREFIX}text entry field corresponding to {example['question_text']}"
        image_path = os.path.join(self.image_dir, f"{example['processed_image']}")
        image = Image.open(image_path).convert("RGB")
        image = np.array(image)
        # first_answer = str(example["answer_bbox"])
        label = f"{example['question_text']}<loc_{x1}><loc_{y1}><loc_{x2}><loc_{y2}>"

        return question, label, image, bbox, image_path


def load_config(config_path, override_args=None):
    """Load configuration from YAML file and override with command line arguments"""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Convert values to proper types based on argument parser types
    for action in parser._actions:
        if action.dest in config and action.type is not None:
            config[action.dest] = action.type(config[action.dest])

    if override_args:
        # Update config with command line arguments
        for key, value in vars(override_args).items():
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
    x1 = max(bbox1[0], bbox2[0])
    y1 = max(bbox1[1], bbox2[1])
    x2 = min(bbox1[2], bbox2[2])
    y2 = min(bbox1[3], bbox2[3])

    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)

    # Calculate union area
    bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    bbox2_area = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
    union_area = bbox1_area + bbox2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area if union_area > 0 else 0
    return iou


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


def metrics(model, data_loader, split_name, processor):
    def _failed_output(generated_text):
        print(f"Cannot parse generated text:\n{generated_text}")

    model.eval()
    total_iou = 0
    total_loss = 0
    num_samples = 0

    # Initialize lists to store data for DataFrame
    predictions_data = []

    with torch.no_grad():
        for inputs, answers, widths, heights, gt_bboxes, image_paths in data_loader:
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
                current_ids_text = processor.batch_decode(
                    current_ids, skip_special_tokens=False
                )
                generated_ids_list_text = processor.batch_decode(
                    generated_ids_list, skip_special_tokens=False
                )

                # Check if all sequences have reached EOS
                if all(
                    len(ids) > 0 and ids[-1] == model.config.text_config.eos_token_id
                    for ids in generated_ids_list
                ):
                    break

                # Update input for next iteration
                print(f"token no: {current_ids.shape[1]}", end="\r")
                current_ids = torch.cat([current_ids, next_tokens], dim=-1)
            print()

            # Process each sample in the batch
            generated_texts = processor.batch_decode(
                generated_ids_list, skip_special_tokens=False
            )

            # Calculate loss for the batch
            labels = processor.tokenizer(
                text=answers,
                return_tensors="pt",
                padding=True,
                return_token_type_ids=False,
            ).input_ids.to(device)
            loss_outputs = model(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                labels=labels,
            )
            total_loss += loss_outputs.loss.item()

            for i, generated_text in enumerate(generated_texts):
                parsed_answer = processor.post_process_generation(
                    generated_text,
                    task=TASK_NAME_PREFIX,
                    image_size=(widths[i], heights[i]),
                )
                pred_bboxes = parsed_answer[TASK_NAME_PREFIX]["bboxes"]
                if len(pred_bboxes) == 0:
                    pred_bbox = None  # always wrong
                else:
                    pred_bbox = pred_bboxes[0]

                # Calculate IoU
                iou = calculate_iou(pred_bbox, gt_bboxes[i])
                total_iou += iou

                # Store data for DataFrame
                predictions_data.append(
                    {
                        "input_text": input_text[i],
                        "generated_text": generated_text,
                        "ground_truth_bbox": gt_bboxes[i],
                        "predicted_bbox": pred_bbox,
                        "iou": iou,
                        "image_width": widths[i],
                        "image_height": heights[i],
                        "pixel_values": inputs["pixel_values"][i].cpu().numpy(),
                        "answer": answers[i],
                        "image_path": image_paths[i],
                    }
                )

                num_samples += 1

    avg_iou = total_iou / num_samples if num_samples > 0 else 0
    avg_loss = total_loss / len(data_loader)

    print(f"val outputs (final batch):\n{generated_texts}")
    print(f"Validation Accuracy: {avg_iou}")
    print(f"Validation Loss: {avg_loss}")
    wandb.log(
        {f"accuracy/{split_name}_iou": avg_iou, f"loss/{split_name}_loss": avg_loss}
    )

    # Create and return DataFrame
    predictions_df = pd.DataFrame(predictions_data)
    return avg_iou, avg_loss, predictions_df


def evaluate(model, val_loader, epoch, timestamp, CHECKPOINT_DIR, processor):
    """Evaluate model performance"""
    val_accuracy, val_loss, predictions_df = metrics(
        model, val_loader, "val", processor
    )
    return val_accuracy, val_loss, predictions_df


# Main execution code starts here
# Load configuration
config = load_config(args.config, args)

# Configuration
TASK_NAME_PREFIX = config["task_name_prefix"]
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

# Override with command line arguments if provided
if args.train_size is not None:
    TRAIN_SIZE = args.train_size
if args.val_size is not None:
    VAL_SIZE = args.val_size
if args.note is not None:
    NOTE = args.note

# Initialize wandb with config
wandb_config = {
    "task_name_prefix": TASK_NAME_PREFIX,
    "train_batch_size": TRAIN_BATCH_SIZE,
    "epochs": EPOCHS,
    "learning_rate": LEARNING_RATE,
    "model": MODEL_NAME,
    # "model_revision": MODEL_REVISION,
    "train_paths": config["train_paths"],
    "eval_path": config["eval_path"],
    "load_checkpoint_from": LOAD_CHECKPOINT_FROM,
    "train_size": TRAIN_SIZE,
    "val_size": VAL_SIZE,
    "note": NOTE,  # Add note to wandb config
}

# Create a unique run name with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
run_name = f"train_tool_{timestamp}"
if NOTE:
    run_name = f"{run_name}_{NOTE.replace(' ', '_')}"

run = wandb.init(project="form-filler", name=run_name, config=wandb_config)

disable_caching()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model from checkpoint if specified, otherwise load from pretrained
if LOAD_CHECKPOINT_FROM:
    print(f"Loading model from checkpoint: {LOAD_CHECKPOINT_FROM}")
    model_config = AutoConfig.from_pretrained(
        "microsoft/Florence-2-large-ft",
        trust_remote_code=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        LOAD_CHECKPOINT_FROM, trust_remote_code=True, config=model_config
    ).to(device)
else:
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True).to(
        device
    )

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

processor = AutoProcessor.from_pretrained(MODEL_NAME, trust_remote_code=True)

for param in model.vision_tower.parameters():
    param.is_trainable = False

train_dataset = ConcatDataset(
    [FormGymDataset(path, max_size=TRAIN_SIZE) for path in config["train_paths"]]
)
val_dataset = FormGymDataset(config["eval_path"], max_size=VAL_SIZE)

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

optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
num_training_steps = EPOCHS * len(train_loader)

lr_scheduler = get_scheduler(
    name="linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps,
)

batch_no = -1
val_accuracy, val_loss, predictions_df = None, None, None
total_batches = 0
batches_per_epoch = len(train_loader)
for epoch in range(EPOCHS):
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
            return_token_type_ids=False,
        ).input_ids.to(device)
        outputs = model(input_ids=input_ids, pixel_values=pixel_values, labels=labels)
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

        # Check if we should evaluate based on fractional epochs
        current_epoch_fraction = total_batches / batches_per_epoch
        if current_epoch_fraction % EPOCHS_PER_EVAL < 1.0 / batches_per_epoch:
            val_accuracy, val_loss, predictions_df = evaluate(
                model,
                val_loader,
                current_epoch_fraction,
                timestamp,
                CHECKPOINT_DIR,
                processor,
            )
            # Save model checkpoint after evaluation
            checkpoint_path = os.path.join(
                CHECKPOINT_DIR, timestamp, f"model_epoch_{current_epoch_fraction:.2f}"
            )
            if NOTE:
                checkpoint_path = f"{checkpoint_path}_{NOTE.replace(' ', '_')}"
            os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
            print(f"Saving model checkpoint to {checkpoint_path}")
            model.save_pretrained(checkpoint_path)
            print(f"Model checkpoint saved successfully")

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
os.makedirs("tmp/tool", exist_ok=True)
if predictions_df is None:
    val_accuracy, val_loss, predictions_df = evaluate(
        model, val_loader, 0, timestamp, CHECKPOINT_DIR, processor
    )
for index, row in predictions_df.iterrows():
    # Load the actual image file
    image = Image.open(row["image_path"]).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Draw ground truth box in green
    gt_bbox = row["ground_truth_bbox"]
    draw.rectangle(gt_bbox, outline="green", width=2)
    label = row.answer.split("<")[0]
    draw.text(gt_bbox[:2], label, fill="green")

    # Draw predicted box in red
    if row["predicted_bbox"] is not None:
        pred_bbox = row["predicted_bbox"]
        draw.rectangle(pred_bbox, outline="red", width=2)
    else:
        # Draw text when predicted bbox is None
        draw.text((10, 10), "pred bbox is none", fill="red")

    # Save the image
    output_path = f"tmp/tool/prediction_{index}.png"
    image.save(output_path)

    # Log to wandb
    wandb.log(
        {
            "visualization": wandb.Image(
                image, caption=f"Prediction {index} (Green: GT, Red: Pred)"
            )
        }
    )
