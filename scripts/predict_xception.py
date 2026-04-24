import os
import torch
import torch.nn as nn
import timm
import numpy as np
from PIL import Image
from torchvision import transforms

# =========================
# SETTINGS
# =========================
MODEL_PATH = "models/xception.pth"
FRAME_DIR = "data/test/frames"

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# =========================
# LOAD MODEL
# =========================
model = timm.create_model("xception", pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 1)
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
    probs = []

    with torch.no_grad():
        for img_name in os.listdir(frame_dir):
            if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            img_path = os.path.join(frame_dir, img_name)
            img = Image.open(img_path).convert("RGB")
            img = transform(img).unsqueeze(0).to(device)

            logit = model(img)
            fake_prob = torch.sigmoid(logit).item()
            probs.append(fake_prob)

    if len(probs) == 0:
        raise ValueError("No frames found for prediction.")

    avg_fake = np.mean(probs)
    authenticity_score = (1 - avg_fake) * 100

    return round(authenticity_score, 2), round(avg_fake, 4)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    score, fake_prob = predict_video_authenticity(FRAME_DIR)

    print("\n==== XCEPTION RESULT ====")
    print("Average Fake Probability:", fake_prob)
    print("Authenticity Score:", score)

    if score >= 80:
        print("Verdict: Likely Genuine")
    elif score >= 50:
        print("Verdict: Suspicious")
    else:
        print("Verdict: Likely Deepfake")
