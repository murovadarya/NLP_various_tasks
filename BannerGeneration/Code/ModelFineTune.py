import pandas as pd
import numpy as np
import torch
from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

import torch.nn as nn
import torch.optim as optim

DDATA_PATH_TRAIN = './Data/train_cleaned.csv'
DATA_PATH_TEST = './Data/test.csv'

MODEL_NAME = 'UrukHan/t5-russian-summarization'
MAX_INPUT = 256

tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

train_enc_x = torch.load('./train_enc_x.pt')
test_enc_x = torch.load('./train_enc_y.pt')
train_enc_y = torch.load('./test_enc_x.pt')
test_enc_y = torch.load('./test_enc_y.pt')

# Step 2: Define a Custom Loss Function (Cosine Similarity Loss)
class CosineSimilarityLoss(nn.Module):
    def forward(self, predicted, target):
        # Calculate Cosine Similarity
        similarity = nn.functional.cosine_similarity(predicted, target.unsqueeze(2), dim=2)
        # Calculate the loss (e.g., maximize similarity)
        loss = 1 - similarity.mean()
        return loss

# Step 1: Define a Custom Dataset
class CustomDataset(Dataset):
    def __init__(self, enc_x, enc_y):
        self.enc_x = enc_x
        self.enc_y = enc_y

    def __len__(self):
        return len(self.enc_x['input_ids'])

    def __getitem__(self, idx):
        return {
            'input_ids': self.enc_x['input_ids'][idx],
            'attention_mask': self.enc_x['attention_mask'][idx],
            'labels': self.enc_y['input_ids'][idx],
        }

# Step 3: Create a Custom Training Loop
def train(model, dataloader, optimizer, loss_fn, device):
    model.train()
    total_loss = 0.0
    for batch in dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = loss_fn(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

        print(f'batch loss: {loss}')

    return total_loss / len(dataloader)

# Set up DataLoader and optimizer
train_dataset = CustomDataset(train_enc_x, train_enc_y)
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

optimizer = optim.AdamW(model.parameters(), lr=1e-4)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the loss function
loss_fn = CosineSimilarityLoss()

print('training_started....')
# Training loop
for epoch in range(20):  # You can adjust the number of epochs
    print(f'Epoch {epoch}')
    avg_loss = train(model, train_dataloader, optimizer, loss_fn, device)
    print(f"Epoch {epoch + 1}, Average Loss: {avg_loss:.4f}")
    model.save_pretrained(f"./Model/trained_t5_model_{epoch}")

# Save the trained model
model.save_pretrained("./Model/trained_t5_model")

