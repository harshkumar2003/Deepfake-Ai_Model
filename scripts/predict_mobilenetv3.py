import os
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image

# =========================
# SETTINGS
# =========================
MODEL_PATH = "models/mobilenetv3.pth"
FRAME_DIR = "data/test/frames"

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# =========================
# LOAD MODEL
# =========================
model = models.mobilenet_v3_large(pretrained=False)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

# =========================
# TRANSFORMS
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
# PREDICTION FUNCTION
# =========================
def predict_video_authenticity(frame_dir):
    fake_probs = []

    with torch.no_grad():
        for img_name in os.listdir(frame_dir):
            if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            img_path = os.path.join(frame_dir, img_name)
            img = Image.open(img_path).convert("RGB")
            img = transform(img).unsqueeze(0).to(device)

            logit = model(img)
            fake_prob = torch.sigmoid(logit).item()
            fake_probs.append(fake_prob)

    if len(fake_probs) == 0:
        raise ValueError("No frames found for prediction.")

    avg_fake = np.mean(fake_probs)
    authenticity_score = (1 - avg_fake) * 100

    return round(authenticity_score, 2), round(avg_fake, 4)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    score, fake_prob = predict_video_authenticity(FRAME_DIR)

    print("\n==== MOBILENETV3 RESULT ====")
    print("Average Fake Probability:", fake_prob)
    print("Authenticity Score:", score)

    if score < 40:
        print("Verdict: Likely Deepfake")
    elif score < 60:
        print("Verdict: Uncertain")
    else:
        print("Verdict: Likely Genuine")
