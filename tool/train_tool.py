import os
import torch
from datasets import load_dataset, disable_caching
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoProcessor, AdamW, get_scheduler
import json
from PIL import Image
import numpy as np
import os
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AdamW, get_scheduler
import wandb

# Configuration
TASK_NAME_PREFIX = "<OPEN_VOCABULARY_DETECTION>"
TRAIN_BATCH_SIZE = 16
VAL_BATCH_SIZE = 64
NUM_WORKERS = 0
EPOCHS = 10
LEARNING_RATE = 1e-6
MODEL_NAME = "microsoft/Florence-2-base-ft"
MODEL_REVISION = "refs/pr/6"
EPOCHS_PER_EVAL = 2

# Initialize wandb with config
config = {
    "task_name_prefix": TASK_NAME_PREFIX,
    "train_batch_size": TRAIN_BATCH_SIZE,
    # "val_batch_size": VAL_BATCH_SIZE,
    # "num_workers": NUM_WORKERS,
    "epochs": EPOCHS,
    "learning_rate": LEARNING_RATE,
    "model": MODEL_NAME,
    "model_revision": MODEL_REVISION,
}

run = wandb.init(project="form-filler", name="train_tool", config=config)

disable_caching()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, trust_remote_code=True, revision=MODEL_REVISION
).to(device)
processor = AutoProcessor.from_pretrained(
    MODEL_NAME, trust_remote_code=True, revision=MODEL_REVISION
)

for param in model.vision_tower.parameters():
    param.is_trainable = False


class FormGymDataset(Dataset):

    def __init__(self, json_path: str, drop_duplicates: bool = False):
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

        return question, label, image, bbox


# def parse_model_output(generated_text):
#     return generated_text.split("<loc_")[1].split(">")[0].split("<")


def calculate_iou(bbox1, bbox2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.
    Bounding boxes are expected in format [x1, y1, x2, y2]
    """
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


def metrics(model, data_loader, split_name):
    def _failed_output(generated_text):
        print(f"Cannot parse generated text:\n{generated_text}")

    model.eval()
    total_iou = 0
    total_loss = 0
    num_samples = 0

    with torch.no_grad():
        for inputs, answers, widths, heights, gt_bboxes in data_loader:
            # TESTING
            test_gen = processor.post_process_generation(
                answers[0],
                task=TASK_NAME_PREFIX,
                image_size=(widths[0], heights[0]),
            )
            print(test_gen)

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
                    pred_bbox = [-2, -2, -1, -1]  # always wrong
                else:
                    pred_bbox = pred_bboxes[0]

                # Calculate IoU
                iou = calculate_iou(pred_bbox, gt_bboxes[i])
                total_iou += iou

                num_samples += 1

    avg_iou = total_iou / num_samples if num_samples > 0 else 0
    avg_loss = total_loss / len(data_loader)

    print(f"val outputs (final batch):\n{generated_texts}")
    print(f"Validation Accuracy: {avg_iou}")
    print(f"Validation Loss: {avg_loss}")
    wandb.log(
        {f"accuracy/{split_name}_iou": avg_iou, f"loss/{split_name}_loss": avg_loss}
    )
    return avg_iou, avg_loss


def collate_fn(batch):
    questions, answers, images, bboxes = zip(*batch)
    inputs = processor(
        text=list(questions),
        images=list(images),
        return_tensors="pt",
        padding=True,
    ).to(device)
    # Get image dimensions (width, height) for each image
    widths = [img.shape[1] for img in images]
    heights = [img.shape[0] for img in images]
    return inputs, answers, widths, heights, bboxes


train_dataset = FormGymDataset("tool/dataset/processed/train_qa_pairs.json")
val_dataset = FormGymDataset("tool/dataset/processed/test_qa_pairs.json")


train_loader = DataLoader(
    train_dataset,
    batch_size=TRAIN_BATCH_SIZE,
    collate_fn=collate_fn,
    num_workers=NUM_WORKERS,
    shuffle=True,
)
val_loader = DataLoader(
    val_dataset,
    batch_size=VAL_BATCH_SIZE,
    collate_fn=collate_fn,
    num_workers=NUM_WORKERS,
)

# Debug: Run a single forward pass for debugging...
# print("\nRunning single forward pass for debugging...")
# metrics(model, val_loader, "val")


optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
num_training_steps = EPOCHS * len(train_loader)

lr_scheduler = get_scheduler(
    name="linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps,
)


batch_no = -1
for epoch in range(EPOCHS):
    model.train()
    train_loss = 0
    for inputs, answers, widths, heights, bboxes in tqdm(
        train_loader, desc=f"Training Epoch {epoch + 1}/{EPOCHS}"
    ):
        batch_no += 1
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

    avg_train_loss = train_loss / len(train_loader)
    print(f"Average Training Loss: {avg_train_loss}")
    wandb.log(
        {
            "loss/train_loss": avg_train_loss,
            "config/learning_rate": lr_scheduler.get_last_lr()[0],
            "config/epoch": epoch,
        }
    )

    if epoch % EPOCHS_PER_EVAL == 0:
        val_accuracy, val_loss = metrics(model, val_loader, "train")
        # wandb.log({"epoch": epoch, "val_accuracy": val_accuracy, "val_loss": val_loss})
