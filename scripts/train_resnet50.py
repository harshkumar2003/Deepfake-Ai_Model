import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image

# =========================
# SETTINGS (FINAL)
# =========================
DATA_DIR = "data/train"              # data/train/real , data/train/fake
MODEL_DIR = "models"
MODEL_SAVE_PATH = os.path.join(MODEL_DIR, "resnet50.pth")

MAX_IMAGES_PER_CLASS = 2500          # same as Xception (fair comparison)
BATCH_SIZE = 4
EPOCHS = 2
LR = 1e-4
NUM_WORKERS = 0                      # Windows + 8GB RAM safe

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# =========================
# DATASET (LIMITED)
# =========================
class DeepfakeDataset(Dataset):
    def __init__(self, root_dir, max_per_class):
        self.samples = []
        self.class_map = {"real": 0, "fake": 1}

        for cls in ["real", "fake"]:
            cls_path = os.path.join(root_dir, cls)
            images = [
                img for img in os.listdir(cls_path)
                if img.lower().endswith((".jpg", ".png", ".jpeg"))
            ]
            images = images[:max_per_class]   # LIMIT

            for img in images:
                self.samples.append(
                    (os.path.join(cls_path, img), self.class_map[cls])
                )

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        print("Using total images:", len(self.samples))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)
        return image, label

# =========================
# DATA LOADER
# =========================
train_dataset = DeepfakeDataset(DATA_DIR, MAX_IMAGES_PER_CLASS)
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS
)

# =========================
# MODEL (RESNET-50)
# =========================
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 1)
model = model.to(device)

# =========================
# LOSS & OPTIMIZER
# =========================
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# =========================
# TRAINING LOOP
# =========================
os.makedirs(MODEL_DIR, exist_ok=True)

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.float().to(device)

        optimizer.zero_grad()
        outputs = model(images).view(-1)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {avg_loss:.4f}")

# =========================
# SAVE MODEL
# =========================
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print("✅ ResNet-50 model trained and saved at:", MODEL_SAVE_PATH)
