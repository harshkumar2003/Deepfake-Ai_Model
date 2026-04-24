# import os
# import random
# import torch
# import torch.nn as nn
# from torch.utils.data import Dataset, DataLoader
# from torchvision import transforms, models
# from PIL import Image

# # =========================
# # SETTINGS
# # =========================
# DATA_DIR        = "data/train"
# MODEL_DIR       = "models"
# MODEL_SAVE_PATH = os.path.join(MODEL_DIR, "mobilenetv3.pth")

# MAX_IMAGES_PER_CLASS = 2500
# BATCH_SIZE           = 16      # increased for GTX 1650
# EPOCHS               = 25      # was 2, now 25
# LR                   = 1e-4
# NUM_WORKERS          = 0       # Windows safe

# # =========================
# # DEVICE
# # =========================
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)
# if torch.cuda.is_available():
#     print("GPU:", torch.cuda.get_device_name(0))

# # =========================
# # DATASET
# # =========================
# class DeepfakeDataset(Dataset):
#     def __init__(self, root_dir, max_per_class):
#         self.samples = []
#         self.class_map = {"real": 0, "fake": 1}

#         for cls in ["real", "fake"]:
#             cls_path = os.path.join(root_dir, cls)
#             images = [
#                 img for img in os.listdir(cls_path)
#                 if img.lower().endswith((".jpg", ".png", ".jpeg"))
#             ]
#             random.shuffle(images)
#             images = images[:max_per_class]
#             for img in images:
#                 self.samples.append(
#                     (os.path.join(cls_path, img), self.class_map[cls])
#                 )

#         self.transform = transforms.Compose([
#             transforms.Resize((224, 224)),
#             transforms.RandomHorizontalFlip(),       # data augmentation
#             transforms.ColorJitter(0.2, 0.2),        # data augmentation
#             transforms.ToTensor(),
#             transforms.Normalize(
#                 mean=[0.485, 0.456, 0.406],
#                 std=[0.229, 0.224, 0.225]
#             )
#         ])
#         print("Total training images:", len(self.samples))

#     def __len__(self):
#         return len(self.samples)

#     def __getitem__(self, idx):
#         img_path, label = self.samples[idx]
#         image = Image.open(img_path).convert("RGB")
#         image = self.transform(image)
#         return image, label

# # =========================
# # DATA LOADER
# # =========================
# train_dataset = DeepfakeDataset(DATA_DIR, MAX_IMAGES_PER_CLASS)
# train_loader  = DataLoader(
#     train_dataset,
#     batch_size=BATCH_SIZE,
#     shuffle=True,
#     num_workers=NUM_WORKERS
# )

# # =========================
# # MODEL
# # =========================
# model = models.mobilenet_v3_large(pretrained=True)
# model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)
# model = model.to(device)

# # =========================
# # LOSS, OPTIMIZER & SCHEDULER
# # =========================
# criterion = nn.BCEWithLogitsLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=LR)
# scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.5)
# # ↑ reduces LR by half every 7 epochs → better learning

# # =========================
# # TRAINING LOOP
# # =========================
# os.makedirs(MODEL_DIR, exist_ok=True)
# best_loss = float("inf")

# print("\n Starting training — MobileNetV3")
# print("=" * 45)

# for epoch in range(EPOCHS):
#     model.train()
#     running_loss = 0.0
#     correct      = 0
#     total        = 0

#     for images, labels in train_loader:
#         images = images.to(device)
#         labels = labels.float().to(device)

#         optimizer.zero_grad()
#         outputs = model(images).view(-1)
#         loss    = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()

#         running_loss += loss.item()

#         # accuracy
#         preds    = (torch.sigmoid(outputs) >= 0.5).float()
#         correct += (preds == labels).sum().item()
#         total   += labels.size(0)

#     scheduler.step()

#     avg_loss = running_loss / len(train_loader)
#     accuracy = 100 * correct / total
#     print(f"Epoch [{epoch+1:02d}/{EPOCHS}] | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.2f}%")

#     # Save best model
#     if avg_loss < best_loss:
#         best_loss = avg_loss
#         torch.save(model.state_dict(), MODEL_SAVE_PATH)
#         print(f"  ✅ Best model saved (loss: {best_loss:.4f})")

# print("\n Training complete!")
# print(f" Model saved at: {MODEL_SAVE_PATH}")



import os
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, models
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# =========================
# SETTINGS
# =========================
DATA_DIR        = "data/train"
MODEL_DIR       = "models"
RESULTS_DIR     = "results"
MODEL_SAVE_PATH = os.path.join(MODEL_DIR, "mobilenetv3.pth")
METRICS_PATH    = os.path.join(RESULTS_DIR, "mobilenetv3_metrics.txt")

MAX_IMAGES_PER_CLASS = 5000
BATCH_SIZE           = 16      # GTX 1650
EPOCHS               = 25
LR                   = 1e-4
VAL_SPLIT            = 0.2     # 80% train, 20% validation
NUM_WORKERS          = 0       # Windows safe

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

# =========================
# DATASET
# =========================
class DeepfakeDataset(Dataset):
    def __init__(self, root_dir, max_per_class, augment=True):
        self.samples = []
        self.class_map = {"real": 0, "fake": 1}

        for cls in ["real", "fake"]:
            cls_path = os.path.join(root_dir, cls)
            images = [
                img for img in os.listdir(cls_path)
                if img.lower().endswith((".jpg", ".png", ".jpeg"))
            ]
            random.shuffle(images)
            images = images[:max_per_class]
            for img in images:
                self.samples.append(
                    (os.path.join(cls_path, img), self.class_map[cls])
                )

        if augment:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(),
                transforms.ColorJitter(0.2, 0.2),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])
        else:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)
        return image, label

# =========================
# DATA LOADERS (80/20 split)
# =========================
full_dataset = DeepfakeDataset(DATA_DIR, MAX_IMAGES_PER_CLASS, augment=False)
total_size   = len(full_dataset)
val_size     = int(total_size * VAL_SPLIT)
train_size   = total_size - val_size

train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

train_dataset.dataset.transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.2, 0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE,
                          shuffle=True, num_workers=NUM_WORKERS)
val_loader   = DataLoader(val_dataset, batch_size=BATCH_SIZE,
                          shuffle=False, num_workers=NUM_WORKERS)

print(f"Train samples: {train_size} | Val samples: {val_size}")

# =========================
# MODEL
# =========================
model = models.mobilenet_v3_large(pretrained=True)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)
model = model.to(device)

# =========================
# LOSS, OPTIMIZER & SCHEDULER
# =========================
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.5)

# =========================
# TRAINING LOOP
# =========================
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
best_val_loss = float("inf")

print("\n Starting training — MobileNetV3")
print("=" * 55)

epoch_logs = []

for epoch in range(EPOCHS):
    # --- TRAIN ---
    model.train()
    running_loss = 0.0
    correct = 0
    total   = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.float().to(device)

        optimizer.zero_grad()
        outputs = model(images).view(-1)
        loss    = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        preds    = (torch.sigmoid(outputs) >= 0.5).float()
        correct += (preds == labels).sum().item()
        total   += labels.size(0)

    scheduler.step()
    train_loss = running_loss / len(train_loader)
    train_acc  = 100 * correct / total

    # --- VALIDATE ---
    model.eval()
    val_loss    = 0.0
    all_labels  = []
    all_probs   = []
    all_preds   = []

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.float().to(device)

            outputs = model(images).view(-1)
            loss    = criterion(outputs, labels)
            val_loss += loss.item()

            probs = torch.sigmoid(outputs).cpu().numpy()
            preds = (probs >= 0.5).astype(int)

            all_probs.extend(probs.tolist())
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.cpu().numpy().astype(int).tolist())

    val_loss /= len(val_loader)

    acc       = accuracy_score(all_labels, all_preds) * 100
    precision = precision_score(all_labels, all_preds, zero_division=0) * 100
    recall    = recall_score(all_labels, all_preds, zero_division=0) * 100
    f1        = f1_score(all_labels, all_preds, zero_division=0) * 100
    auc       = roc_auc_score(all_labels, all_probs) * 100

    log = (f"Epoch [{epoch+1:02d}/{EPOCHS}] "
           f"| Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% "
           f"| Val Loss: {val_loss:.4f} | Val Acc: {acc:.2f}% "
           f"| Precision: {precision:.2f}% | Recall: {recall:.2f}% "
           f"| F1: {f1:.2f}% | AUC: {auc:.2f}%")
    print(log)
    epoch_logs.append(log)

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print(f"  ✅ Best model saved (val loss: {best_val_loss:.4f})")

# =========================
# SAVE FINAL METRICS
# =========================
with open(METRICS_PATH, "w") as f:
    f.write("MobileNetV3 — Training & Validation Metrics\n")
    f.write("=" * 55 + "\n")
    f.write(f"Dataset      : FaceForensics++ frames\n")
    f.write(f"Train/Val    : {train_size} / {val_size} samples\n")
    f.write(f"Epochs       : {EPOCHS}\n")
    f.write(f"Batch Size   : {BATCH_SIZE}\n")
    f.write(f"Optimizer    : Adam (LR={LR})\n")
    f.write(f"Scheduler    : StepLR (step=7, gamma=0.5)\n")
    f.write(f"Augmentation : RandomHorizontalFlip, ColorJitter\n")
    f.write("=" * 55 + "\n\n")
    for log in epoch_logs:
        f.write(log + "\n")
    f.write(f"\nBest Val Loss: {best_val_loss:.4f}\n")

print("\n Training complete!")
print(f" Model  saved at : {MODEL_SAVE_PATH}")
print(f" Metrics saved at: {METRICS_PATH}")