import os
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image
from datetime import datetime
from datetime import datetime

# =========================
# SETTINGS
# =========================
FRAME_DIR = "data/test/frames"
RESULT_DIR = "results"
VIDEO_NAME =  "real-v-3"  # Example video name; adjust as needed

MODEL_PATHS = {
    "Xception (Non-Random)": ("xception", "models/xception.pth"),
    "ResNet-50 (Non-Random)": ("resnet50", "models/resnet50.pth"),
    "EfficientNet-B0 (Random)": ("efficientnet", "models/efficientnet_b0.pth"),
    "MobileNetV3 (Random)": ("mobilenet", "models/mobilenetv3.pth"),
    "ShuffleNet-V2 (Random)": ("shufflenet", "models/shufflenet_v2.pth"),
}

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# LOAD MODEL
# =========================
def load_model(name, path):
    if name == "xception":
        import timm
        model = timm.create_model("xception", pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 1)

    elif name == "resnet50":
        model = models.resnet50(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 1)

    elif name == "efficientnet":
        model = models.efficientnet_b0(pretrained=False)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

    elif name == "mobilenet":
        model = models.mobilenet_v3_large(pretrained=False)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

    elif name == "shufflenet":
        model = models.shufflenet_v2_x1_0(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 1)

    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device).eval()
    return model

# =========================
# PREDICT
# =========================
def predict(model):
    probs = []
    with torch.no_grad():
        for img in os.listdir(FRAME_DIR):
            if img.endswith((".jpg", ".png", ".jpeg")):
                im = Image.open(os.path.join(FRAME_DIR, img)).convert("RGB")
                im = transform(im).unsqueeze(0).to(device)
                prob = torch.sigmoid(model(im)).item()
                probs.append(prob)

    avg_fake = np.mean(probs)
    score = (1 - avg_fake) * 100
    return round(score, 2)

# =========================
# MAIN
# =========================
os.makedirs(RESULT_DIR, exist_ok=True)
video_dir = os.path.join(RESULT_DIR, VIDEO_NAME)
os.makedirs(video_dir, exist_ok=True)

summary = {}
random_scores = []

for label, (model_name, path) in MODEL_PATHS.items():
    model = load_model(model_name, path)
    score = predict(model)
    summary[label] = score

    with open(os.path.join(video_dir, f"{label.replace(' ', '_')}.txt"), "w") as f:
        f.write(f"{label}\nAuthenticity Score: {score}\n")

    if "Random" in label:
        random_scores.append(score)

# =========================
# ENSEMBLE
# =========================
ensemble_score = round(sum(random_scores) / len(random_scores), 2)

with open(os.path.join(video_dir, "ensemble.txt"), "w") as f:
    f.write(f"Final Ensemble Score: {ensemble_score}\n")

# =========================
# SUMMARY CSV
# =========================
csv_path = os.path.join(RESULT_DIR, "summary_results.csv")
write_header = not os.path.exists(csv_path)

with open(csv_path, "a") as f:
    if write_header:
        f.write("Video," + ",".join(summary.keys()) + ",Ensemble\n")

    f.write(
        VIDEO_NAME + "," +
        ",".join(str(v) for v in summary.values()) +
        f",{ensemble_score}\n"
    )

print("\n✅ ALL MODELS RUN SUCCESSFULLY")
print("📁 Results saved in:", video_dir)
print("📊 Ensemble Score:", ensemble_score)
