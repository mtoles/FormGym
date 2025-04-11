import os
import torch
from datasets import load_dataset
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoProcessor, AdamW, get_scheduler

data = load_dataset("HuggingFaceM4/DocumentVQA")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Florence-2-base-ft", trust_remote_code=True, revision="refs/pr/6"
).to(device)
processor = AutoProcessor.from_pretrained(
    "microsoft/Florence-2-base-ft", trust_remote_code=True, revision="refs/pr/6"
)

for param in model.vision_tower.parameters():
    param.is_trainable = False


class DocVQADataset(Dataset):

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        example = self.data[idx]
        question = "<DocVQA>" + example["question"]
        first_answer = example["answers"][0]
        image = example["image"].convert("RGB")
        return question, first_answer, image


import os
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AdamW, get_scheduler


def collate_fn(batch):
    questions, answers, images = zip(*batch)
    inputs = processor(
        text=list(questions), images=list(images), return_tensors="pt", padding=True
    ).to(device)
    return inputs, answers


train_dataset = DocVQADataset(data["train"])
val_dataset = DocVQADataset(data["validation"])
batch_size = 6
num_workers = 0

train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    collate_fn=collate_fn,
    num_workers=num_workers,
    shuffle=True,
)
val_loader = DataLoader(
    val_dataset, batch_size=batch_size, collate_fn=collate_fn, num_workers=num_workers
)

epochs = 7
optimizer = AdamW(model.parameters(), lr=1e-6)
num_training_steps = epochs * len(train_loader)

lr_scheduler = get_scheduler(
    name="linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps,
)

for epoch in range(epochs):
    model.train()
    train_loss = 0
    i = -1
    for inputs, answers in tqdm(
        train_loader, desc=f"Training Epoch {epoch + 1}/{epochs}"
    ):
        i += 1
        input_ids = inputs["input_ids"]
        pixel_values = inputs["pixel_values"]
        labels = processor.tokenizer(
            text=answers, return_tensors="pt", padding=True, return_token_type_ids=False
        ).input_ids.to(device)
        outputs = model(input_ids=input_ids, pixel_values=pixel_values, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        train_loss += loss.item()
    avg_train_loss = train_loss / len(train_loader)
    print(f"Average Training Loss: {avg_train_loss}")

    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in tqdm(val_loader, desc=f"Validation Epoch {epoch + 1}/{epochs}"):
            inputs, answers = batch
            input_ids = inputs["input_ids"]
            pixel_values = inputs["pixel_values"]
            labels = processor.tokenizer(
                text=answers,
                return_tensors="pt",
                padding=True,
                return_token_type_ids=False,
            ).input_ids.to(device)
            outputs = model(
                input_ids=input_ids, pixel_values=pixel_values, labels=labels
            )
            loss = outputs.loss
            val_loss += loss.item()

            print(val_loss / len(val_loader))


# import json
# import torch
# from torch.utils.data import Dataset, DataLoader
# from PIL import Image
# import os
# import numpy as np
# from transformers import AutoProcessor, AutoModelForCausalLM
# import torch.nn as nn
# from tqdm import tqdm

# class FormDataset(Dataset):
#     def __init__(self, json_path, image_dir, processor):
#         self.processor = processor
#         self.image_dir = image_dir

#         with open(json_path, 'r') as f:
#             self.data = json.load(f)

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         item = self.data[idx]
#         image_path = os.path.join(self.image_dir, f"{item['processed_image']}")
#         image = Image.open(image_path).convert('RGB')
#         image = np.array(image)

#         # Format the prompt
#         # prompt = f"Where is the bounding box for '{item['question_text']}'"
#         prompt = "<OD>"

#         # Process the image and text with padding
#         inputs = self.processor(
#             images=image,
#             text=prompt,
#             return_tensors="pt",
#             padding="max_length",
#             # max_length=2048,
#             truncation=True,
#         )


#         # Get the bounding box coordinates
#         # bbox = torch.tensor(item['question_bbox'], dtype=torch.bfloat16)
#         bbox = str(item["answer_bbox"])
#         labels = self.processor.tokenizer(
#             bbox,
#             return_tensors="pt",
#             padding="max_length",
#             truncation=True,
#         )['input_ids'].squeeze(0)

#         return {
#             'pixel_values': inputs['pixel_values'].squeeze(0).to(torch.bfloat16),
#             'input_ids': inputs['input_ids'].squeeze(0),
#             'attention_mask': inputs['attention_mask'].squeeze(0),
#             'labels': labels
#         }

# def train():
#     # Initialize model and processor
#     # model_id = "microsoft/Florence-2-large"
#     model_id = "microsoft/Florence-2-base-ft"
#     torch_dtype = torch.bfloat16 #if torch.cuda.is_available() else torch.float32
#     # model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=torch_dtype, device_map="auto")
#     model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=torch_dtype)
#     processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

#     # Move model to GPU
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = model.to(device)

#     # Initialize dataset and dataloader
#     dataset = FormDataset(
#         json_path="tool/dataset/processed/qa_pairs_short.json",
#         image_dir="tool/dataset/processed/images",
#         processor=processor
#     )

#     dataloader = DataLoader(
#         dataset,
#         batch_size=32,
#         # batch_size=1,
#         shuffle=True,
#         num_workers=4,
#         pin_memory=True
#     )


#     # Initialize optimizer and loss function
#     optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
#     criterion = nn.MSELoss()

#     # Save first batch for debugging
#     # first_batch = next(iter(dataloader))

#     # Training loop
#     num_epochs = 1
#     for epoch in range(num_epochs):
#         model.train()
#         total_loss = 0

#         progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}/{num_epochs}")
#         for batch in progress_bar:
#             # Move batch to GPU
#             pixel_values = batch['pixel_values'].to(device)
#             input_ids = batch['input_ids'].to(device)
#             attention_mask = batch['attention_mask'].to(device)
#             labels = batch['labels'].to(device)

#             # Forward pass
#             outputs = model(
#                 input_ids=input_ids,
#                 pixel_values=pixel_values,
#                 # attention_mask=attention_mask,
#                 labels=labels
#             )

#             loss = outputs.loss

#             # Extract the predicted bounding box from the model's output
#             # Note: This is a placeholder - you'll need to modify this based on how
#             # Florence-2 outputs bounding box predictions
#             # predicted_bbox = outputs.last_hidden_state[:, -1, :4]  # Assuming last 4 tokens are bbox coords

#             # Calculate loss
#             # loss = criterion(predicted_bbox, bbox)

#             # Backward pass
#             loss.backward()
#             optimizer.step()
#             # lr_scheduler.step()
#             optimizer.zero_grad()

#             total_loss += loss.item()
#             progress_bar.set_postfix({'loss': loss.item()})

#         avg_loss = total_loss / len(dataloader)
#         print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss:.4f}")

# if __name__ == "__main__":
#     train()
