import os
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image

# =========================
# SETTINGS
# =========================

# frame_dir = "data/test/frames"
FRAME_DIR = None
# FRAME_DIR = "data/test/frames"

MODEL_PATHS = {
    "EfficientNet-B0": "models/efficientnet_b0.pth",
    "MobileNetV3": "models/mobilenetv3.pth",
    "ShuffleNet-V2": "models/shufflenet_v2.pth"
}

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

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
# LOAD MODELS
# =========================
def load_model(model_name, model_path):
    if model_name == "EfficientNet-B0":
        model = models.efficientnet_b0(pretrained=False)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

    elif model_name == "MobileNetV3":
        model = models.mobilenet_v3_large(pretrained=False)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

    elif model_name == "ShuffleNet-V2":
        model = models.shufflenet_v2_x1_0(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 1)

    else:
        raise ValueError("Unknown model")

    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

# =========================
# PREDICT SINGLE MODEL
# =========================
def predict_with_model(model, frame_dir):
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

    avg_fake = np.mean(fake_probs)
    authenticity_score = (1 - avg_fake) * 100
    return round(authenticity_score, 2)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    FRAME_DIR = "data/test/frames"
    scores = {}

    print("\n==== INDIVIDUAL MODEL RESULTS ====")

    for model_name, path in MODEL_PATHS.items():
        model = load_model(model_name, path)
        score = predict_with_model(model)
        scores[model_name] = score
        print(f"{model_name} Authenticity Score: {score}")

    # =========================
    # ENSEMBLE
    # =========================
    final_score = sum(scores.values()) / len(scores)

    print("\n==== FINAL ENSEMBLE RESULT ====")
    print("Final Authenticity Score:", round(final_score, 2))

    if final_score < 40:
        print("Verdict: Likely Deepfake")
    elif final_score < 60:
        print("Verdict: Uncertain")
    else:
        print("Verdict: Likely Genuine")
