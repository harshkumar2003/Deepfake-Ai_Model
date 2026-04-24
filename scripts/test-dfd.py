import os
import cv2
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image

from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import pandas as pd

# =========================
# SETTINGS
# =========================
TEST_DIR = "data/test-dfd"
IMG_SIZE = 224
MAX_FRAMES = 60
SKIP = 5

THRESHOLD = 0.40   # 🔥 LOWERED for better fake detection

# 🔥 Weighted Ensemble
WEIGHTS = {
    "EfficientNet": 0.5,
    "MobileNet": 0.3,
    "ShuffleNet": 0.2
}

MODELS = {
    "EfficientNet": "models/efficientnet_b0.pth",
    "MobileNet": "models/mobilenetv3.pth",
    "ShuffleNet": "models/shufflenet_v2.pth"
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# FACE DETECTOR
# =========================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# =========================
# LOAD MODEL
# =========================
def load_model(name, path):
    if name == "EfficientNet":
        model = models.efficientnet_b0(weights=None)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

    elif name == "MobileNet":
        model = models.mobilenet_v3_large(weights=None)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

    elif name == "ShuffleNet":
        model = models.shufflenet_v2_x1_0(weights=None)
        model.fc = nn.Linear(model.fc.in_features, 1)

    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    model.eval()
    return model

# =========================
# FRAME EXTRACTION
# =========================
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    frame_id = 0
    count = 0

    while cap.isOpened() and count < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % SKIP == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                crop = frame[y:y+h, x:x+w]
            else:
                crop = frame

            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
            crop = Image.fromarray(crop)

            frames.append(crop)
            count += 1

        frame_id += 1

    cap.release()
    return frames

# =========================
# PREDICT VIDEO
# =========================
def predict_video(model, video_path):
    frames = extract_frames(video_path)
    if len(frames) == 0:
        return None

    probs = []
    for frame in frames:
        img = transform(frame).unsqueeze(0).to(device)

        with torch.no_grad():
            out = model(img).view(-1)
            prob = torch.sigmoid(out).item()
            probs.append(prob)

    return np.mean(probs)

# =========================
# LOAD MODELS
# =========================
models_loaded = {}
for name, path in MODELS.items():
    models_loaded[name] = load_model(name, path)

# =========================
# TEST LOOP
# =========================
all_labels = []
all_preds = []
all_probs = []
results = []

uncertain_count = 0

for label_name in ["real", "fake"]:
    folder = os.path.join(TEST_DIR, label_name)
    true_label = 0 if label_name == "real" else 1

    for video in os.listdir(folder):
        video_path = os.path.join(folder, video)

        model_probs = {}

        for name, model in models_loaded.items():
            prob = predict_video(model, video_path)
            if prob is None:
                continue
            model_probs[name] = prob

        if len(model_probs) != 3:
            continue

        # 🔥 Weighted Ensemble
        ensemble_prob = sum(
            WEIGHTS[name] * model_probs[name]
            for name in model_probs
        )

        auth_score = (1 - ensemble_prob) * 100

        # 🔥 FINAL DECISION LOGIC
        if 0.45 <= ensemble_prob <= 0.55:
            pred = -1   # uncertain
            uncertain_count += 1
        else:
            if ensemble_prob >= THRESHOLD:
                pred = 1   # fake
            else:
                pred = 0   # real

        # Store confident predictions only
        if pred != -1:
            all_labels.append(true_label)
            all_preds.append(pred)
            all_probs.append(ensemble_prob)

        results.append([
            video,
            model_probs["EfficientNet"],
            model_probs["MobileNet"],
            model_probs["ShuffleNet"],
            ensemble_prob,
            auth_score,
            true_label,
            pred
        ])

        print(f"{video} | Score: {auth_score:.2f} | Pred: {pred}")

# =========================
# METRICS
# =========================
print("\n📊 FINAL RESULTS")

if len(all_preds) > 0:
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    precision = precision_score(all_labels, all_preds)
    recall = recall_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
else:
    print("No confident predictions!")

print(f"Uncertain Samples: {uncertain_count}")

# =========================
# CONFUSION MATRIX
# =========================
if len(all_preds) > 0:
    cm = confusion_matrix(all_labels, all_preds)

    plt.figure()
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i][j], ha="center", va="center")

    plt.savefig("confusion_matrix.png")
    plt.close()

# =========================
# ROC CURVE
# =========================
if len(all_probs) > 0:
    fpr, tpr, _ = roc_curve(all_labels, all_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0,1],[0,1],'--')
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig("roc_curve.png")
    plt.close()

    print(f"AUC: {roc_auc:.4f}")

# =========================
# SAVE RESULTS
# =========================
df = pd.DataFrame(results, columns=[
    "Video",
    "EfficientNet",
    "MobileNet",
    "ShuffleNet",
    "Ensemble_Prob",
    "Authenticity_Score",
    "True_Label",
    "Pred"
])

df.to_csv("dfdc_results.csv", index=False)

print("\n✅ Saved:")
print("→ dfdc_results.csv")
print("→ confusion_matrix.png")
print("→ roc_curve.png")