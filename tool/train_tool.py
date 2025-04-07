import json
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
from transformers import AutoProcessor, AutoModelForCausalLM
import torch.nn as nn
from tqdm import tqdm

class FormDataset(Dataset):
    def __init__(self, json_path, image_dir, processor):
        self.processor = processor
        self.image_dir = image_dir
        
        with open(json_path, 'r') as f:
            self.data = json.load(f)
            
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        image_path = os.path.join(self.image_dir, f"{item['form_id']}.png")
        image = Image.open(image_path).convert('RGB')
        
        # Format the prompt
        prompt = f"Where is the bounding box for '{item['question_text']}'"
        
        # Process the image and text
        inputs = self.processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        )
        
        # Get the bounding box coordinates
        bbox = torch.tensor(item['question_bbox'], dtype=torch.float32)
        
        return {
            'pixel_values': inputs['pixel_values'].squeeze(0),
            'input_ids': inputs['input_ids'].squeeze(0),
            'attention_mask': inputs['attention_mask'].squeeze(0),
            'bbox': bbox
        }

def train():
    # Initialize model and processor
    model_id = "microsoft/Florence-2-large"
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    
    # Move model to GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    # Initialize dataset and dataloader
    dataset = FormDataset(
        json_path="tool/dataset/processed/qa_pairs.json",
        image_dir="tool/dataset/processed/images",
        processor=processor
    )
    
    dataloader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )
    
    # Initialize optimizer and loss function
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
    criterion = nn.MSELoss()
    
    # Training loop
    num_epochs = 1
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}/{num_epochs}")
        for batch in progress_bar:
            # Move batch to GPU
            pixel_values = batch['pixel_values'].to(device)
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            bbox = batch['bbox'].to(device)
            
            # Forward pass
            outputs = model(
                pixel_values=pixel_values,
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            
            # Extract the predicted bounding box from the model's output
            # Note: This is a placeholder - you'll need to modify this based on how
            # Florence-2 outputs bounding box predictions
            predicted_bbox = outputs.last_hidden_state[:, -1, :4]  # Assuming last 4 tokens are bbox coords
            
            # Calculate loss
            loss = criterion(predicted_bbox, bbox)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            progress_bar.set_postfix({'loss': loss.item()})
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss:.4f}")

if __name__ == "__main__":
    train()
