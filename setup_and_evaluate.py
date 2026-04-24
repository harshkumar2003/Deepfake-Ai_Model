import os
import cv2
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms, models
from sklearn.metrics import (
    roc_auc_score, roc_curve,
    f1_score, precision_score,
    recall_score, classification_report
)

# =============================================================
# setup_and_evaluate.py
# -------------------------------------------------------------
# This script does EVERYTHING in one run:
#
# STEP 1 — Reads your videos from:
#               data/test/video/real/   (real videos)
#               data/test/video/fake/   (fake videos)
#
# STEP 2 — Extracts 20 frames from each video into:
#               data/test/real/video_name/frame_000.jpg ...
#               data/test/fake/video_name/frame_000.jpg ...
#
# STEP 3 — Runs ensemble model on all videos
#
# STEP 4 — Computes AUC, EER, F1, Precision, Recall
#
# STEP 5 — Saves ROC curve + metrics report to results/
# =============================================================

# =========================
# SETTINGS — CHECK THESE
# =========================
VIDEO_REAL_DIR = "data/test/video/real"   # your real .mp4 files
VIDEO_FAKE_DIR = "data/test/video/fake"   # your fake .mp4 files
FRAMES_REAL    = "data/test/real"         # frames will be saved here
FRAMES_FAKE    = "data/test/fake"         # frames will be saved here
RESULT_DIR     = "results"
NUM_FRAMES     = 20

MODEL_PATHS = {
    "EfficientNet-B0": "models/efficientnet_b0.pth",
    "MobileNetV3":     "models/mobilenetv3.pth",
    "ShuffleNet-V2":   "models/shufflenet_v2.pth",
}

os.makedirs(FRAMES_REAL, exist_ok=True)
os.makedirs(FRAMES_FAKE, exist_ok=True)
os.makedirs(RESULT_DIR,  exist_ok=True)

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}\n")

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

# =====================================================
# STEP 1 — EXTRACT 20 FRAMES FROM EACH VIDEO
# (uses your exact same logic from extract_20_frames.py)
# =====================================================
def extract_20_frames(video_path, output_dir, num_frames=20):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < num_frames:
        print(f"  WARNING: Video too short ({total_frames} frames), extracting all.")
        num_frames = total_frames

    step = total_frames // num_frames
    frame_indices = [i * step for i in range(num_frames)]

    count = 0
    saved = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count in frame_indices:
            frame_name = f"frame_{saved:03d}.jpg"
            cv2.imwrite(os.path.join(output_dir, frame_name), frame)
            saved += 1
        count += 1

    cap.release()
    return saved


def extract_all_videos(video_dir, frames_dir, label):
    print(f"Extracting frames from {label.upper()} videos...")
    video_files = [
        f for f in sorted(os.listdir(video_dir))
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]

    if len(video_files) == 0:
        print(f"  ERROR: No video files found in {video_dir}")
        return []

    extracted = []
    for video_file in video_files:
        video_name  = os.path.splitext(video_file)[0]   # e.g. "real-v-1"
        video_path  = os.path.join(video_dir, video_file)
        output_dir  = os.path.join(frames_dir, video_name)

        # Skip if already extracted
        if os.path.exists(output_dir) and len(os.listdir(output_dir)) >= NUM_FRAMES:
            print(f"  SKIP (already extracted): {video_name}")
            extracted.append(output_dir)
            continue

        saved = extract_20_frames(video_path, output_dir, NUM_FRAMES)
        print(f"  Extracted {saved} frames → {output_dir}")
        extracted.append(output_dir)

    return extracted


# =====================================================
# STEP 2 — LOAD ALL 3 ENSEMBLE MODELS
# =====================================================
def load_all_models():
    loaded = {}

    m1 = models.efficientnet_b0(pretrained=False)
    m1.classifier[1] = nn.Linear(m1.classifier[1].in_features, 1)
    m1.load_state_dict(torch.load(MODEL_PATHS["EfficientNet-B0"], map_location=device))
    loaded["EfficientNet-B0"] = m1.to(device).eval()

    m2 = models.mobilenet_v3_large(pretrained=False)
    m2.classifier[3] = nn.Linear(m2.classifier[3].in_features, 1)
    m2.load_state_dict(torch.load(MODEL_PATHS["MobileNetV3"], map_location=device))
    loaded["MobileNetV3"] = m2.to(device).eval()

    m3 = models.shufflenet_v2_x1_0(pretrained=False)
    m3.fc = nn.Linear(m3.fc.in_features, 1)
    m3.load_state_dict(torch.load(MODEL_PATHS["ShuffleNet-V2"], map_location=device))
    loaded["ShuffleNet-V2"] = m3.to(device).eval()

    print("All 3 models loaded.\n")
    return loaded


# =====================================================
# STEP 3 — PREDICT ONE VIDEO FOLDER
# Returns ensemble fake probability (0.0 to 1.0)
# =====================================================
def predict_video(frame_dir, loaded_models):
    model_probs = []

    for model_name, model in loaded_models.items():
        frame_probs = []

        with torch.no_grad():
            for img_name in sorted(os.listdir(frame_dir)):
                if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
                    continue
                img = Image.open(os.path.join(frame_dir, img_name)).convert("RGB")
                img = transform(img).unsqueeze(0).to(device)
                fake_prob = torch.sigmoid(model(img)).item()
                frame_probs.append(fake_prob)

        if frame_probs:
            model_probs.append(np.mean(frame_probs))

    return float(np.mean(model_probs)) if model_probs else None


# =====================================================
# STEP 4 — COLLECT PREDICTIONS FROM ALL VIDEOS
# =====================================================
def collect_predictions(loaded_models):
    true_labels = []
    fake_probs  = []
    video_names = []

    print("Running ensemble on REAL videos...")
    for video_folder in sorted(os.listdir(FRAMES_REAL)):
        frame_dir = os.path.join(FRAMES_REAL, video_folder)
        if not os.path.isdir(frame_dir):
            continue
        prob = predict_video(frame_dir, loaded_models)
        if prob is None:
            continue
        auth = round((1 - prob) * 100, 2)
        print(f"  {video_folder:20s} | fake_prob={prob:.4f} | authenticity={auth}")
        fake_probs.append(prob)
        true_labels.append(1)        # real = 1
        video_names.append(video_folder)

    print("\nRunning ensemble on FAKE videos...")
    for video_folder in sorted(os.listdir(FRAMES_FAKE)):
        frame_dir = os.path.join(FRAMES_FAKE, video_folder)
        if not os.path.isdir(frame_dir):
            continue
        prob = predict_video(frame_dir, loaded_models)
        if prob is None:
            continue
        auth = round((1 - prob) * 100, 2)
        print(f"  {video_folder:20s} | fake_prob={prob:.4f} | authenticity={auth}")
        fake_probs.append(prob)
        true_labels.append(0)        # fake = 0
        video_names.append(video_folder)

    return np.array(true_labels), np.array(fake_probs), video_names


# =====================================================
# STEP 5 — COMPUTE METRICS
# =====================================================
def compute_metrics(true_labels, fake_probs):
    auth_probs = 1 - fake_probs

    auc             = roc_auc_score(true_labels, auth_probs)
    fpr, tpr, _     = roc_curve(true_labels, auth_probs)
    fnr             = 1 - tpr
    eer_idx         = np.argmin(np.abs(fpr - fnr))
    eer             = float((fpr[eer_idx] + fnr[eer_idx]) / 2)
    binary_preds    = (auth_probs >= 0.5).astype(int)
    f1              = f1_score(true_labels, binary_preds)
    precision       = precision_score(true_labels, binary_preds)
    recall          = recall_score(true_labels, binary_preds)

    return auc, eer, f1, precision, recall, fpr, tpr


# =====================================================
# PLOT ROC CURVE → results/roc_curve.png
# =====================================================
def plot_roc_curve(fpr, tpr, auc, eer):
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='#2E75B6', lw=2,
             label=f'Ensemble ROC Curve (AUC = {auc:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--',
             lw=1, label='Random Classifier (AUC = 0.50)')

    fnr     = 1 - tpr
    eer_idx = np.argmin(np.abs(fpr - fnr))
    plt.scatter(fpr[eer_idx], tpr[eer_idx], color='red', zorder=5,
                s=80, label=f'EER Point = {eer:.4f}')

    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.title('ROC Curve — Ensemble Deepfake Detection\n'
              '(EfficientNet-B0 + MobileNetV3 + ShuffleNet-V2)',
              fontsize=13, fontweight='bold')
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    save_path = os.path.join(RESULT_DIR, "roc_curve.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"\n  ROC curve saved     → {save_path}")


# =====================================================
# SAVE METRICS REPORT → results/metrics_report.txt
# =====================================================
def save_report(auc, eer, f1, precision, recall, true_labels, fake_probs):
    auth_probs   = 1 - fake_probs
    binary_preds = (auth_probs >= 0.5).astype(int)
    clf_report   = classification_report(
        true_labels, binary_preds,
        target_names=["Fake (0)", "Real (1)"]
    )

    report_path = os.path.join(RESULT_DIR, "metrics_report.txt")
    with open(report_path, "w") as f:
        f.write("=" * 55 + "\n")
        f.write("  ENSEMBLE DEEPFAKE DETECTION — METRICS REPORT\n")
        f.write("  Models: EfficientNet-B0, MobileNetV3, ShuffleNet-V2\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"  AUC Score   : {auc:.4f}\n")
        f.write(f"  EER         : {eer:.4f}\n")
        f.write(f"  F1-Score    : {f1:.4f}\n")
        f.write(f"  Precision   : {precision:.4f}\n")
        f.write(f"  Recall      : {recall:.4f}\n\n")
        f.write("  Classification Report (threshold = 0.5):\n")
        f.write("-" * 55 + "\n")
        f.write(clf_report)
        f.write("\n" + "=" * 55 + "\n")

    # Also save as CSV
    csv_path = os.path.join(RESULT_DIR, "metrics_summary.csv")
    with open(csv_path, "w") as f:
        f.write("Metric,Value\n")
        f.write(f"AUC,{auc:.4f}\n")
        f.write(f"EER,{eer:.4f}\n")
        f.write(f"F1-Score,{f1:.4f}\n")
        f.write(f"Precision,{precision:.4f}\n")
        f.write(f"Recall,{recall:.4f}\n")

    print(f"  Metrics report saved → {report_path}")
    print(f"  Metrics CSV saved    → {csv_path}")


# =====================================================
# MAIN — runs all 5 steps
# =====================================================
if __name__ == "__main__":

    # STEP 1 — Extract frames from all videos
    print("=" * 55)
    print("STEP 1: Extracting frames from videos...")
    print("=" * 55)
    extract_all_videos(VIDEO_REAL_DIR, FRAMES_REAL, "real")
    extract_all_videos(VIDEO_FAKE_DIR, FRAMES_FAKE, "fake")

    # STEP 2 — Load models
    print("\n" + "=" * 55)
    print("STEP 2: Loading ensemble models...")
    print("=" * 55)
    loaded_models = load_all_models()

    # STEP 3 — Run predictions
    print("=" * 55)
    print("STEP 3: Running predictions on all videos...")
    print("=" * 55)
    true_labels, fake_probs, video_names = collect_predictions(loaded_models)

    if len(true_labels) == 0:
        print("\nERROR: No videos processed!")
        print(f"  Check VIDEO_REAL_DIR = {VIDEO_REAL_DIR}")
        print(f"  Check VIDEO_FAKE_DIR = {VIDEO_FAKE_DIR}")
        exit()

    n_real = int(np.sum(true_labels))
    n_fake = int(len(true_labels) - n_real)
    print(f"\nTotal videos evaluated : {len(true_labels)}")
    print(f"  Real                 : {n_real}")
    print(f"  Fake                 : {n_fake}")

    # STEP 4 — Compute metrics
    print("\n" + "=" * 55)
    print("STEP 4: Computing metrics...")
    print("=" * 55)
    auc, eer, f1, precision, recall, fpr, tpr = compute_metrics(true_labels, fake_probs)

    print(f"\n  AUC Score   : {auc:.4f}   (1.0 = perfect, 0.5 = random)")
    print(f"  EER         : {eer:.4f}   (lower is better)")
    print(f"  F1-Score    : {f1:.4f}   (higher is better)")
    print(f"  Precision   : {precision:.4f}")
    print(f"  Recall      : {recall:.4f}")

    # STEP 5 — Save outputs
    print("\n" + "=" * 55)
    print("STEP 5: Saving outputs...")
    print("=" * 55)
    plot_roc_curve(fpr, tpr, auc, eer)
    save_report(auc, eer, f1, precision, recall, true_labels, fake_probs)

    print("\n" + "=" * 55)
    print("DONE! Check your results/ folder:")
    print("  results/roc_curve.png      ← Figure for your paper")
    print("  results/metrics_report.txt ← AUC/EER/F1 numbers for your paper")
    print("  results/metrics_summary.csv")
    print("=" * 55)