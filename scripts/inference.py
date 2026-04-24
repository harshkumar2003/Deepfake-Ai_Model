# import os
# import uuid

# from scripts.extract_20_frames import extract_20_frames
# from scripts.final_ensemble_predict import load_model, predict_with_model, MODEL_PATHS

# def predict_video(video_path: str):
#     # 🔥 output_dir define karo
#     frame_dir = os.path.join("temp_frames", uuid.uuid4().hex)

#     extract_20_frames(video_path, frame_dir)

#     scores = {}
#     for model_name, path in MODEL_PATHS.items():
#         model = load_model(model_name, path)
#         score = predict_with_model(model, frame_dir)
#         scores[model_name] = score

#     final_score = sum(scores.values()) / len(scores)

#     return {
#         "final_score": round(final_score, 2),
#         "model_scores": scores
#     }

# import os
# import cv2
# import torch
# import torch.nn as nn
# import numpy as np
# from torchvision import transforms, models
# from PIL import Image

# # =========================
# # SETTINGS
# # =========================
# IMG_SIZE = 224
# MAX_FRAMES = 60
# SKIP = 5
# THRESHOLD = 0.4164  # 🔥 final threshold (0.4164 = 41.64%)

# MODEL_PATHS = {
#     "EfficientNet": "models/efficientnet_b0.pth",
#     "MobileNet": "models/mobilenetv3.pth",
#     "ShuffleNet": "models/shufflenet_v2.pth"
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # =========================
# # FACE DETECTOR
# # =========================
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # =========================
# # TRANSFORM
# # =========================
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
# ])

# # =========================
# # LOAD MODEL
# # =========================
# def load_model(name, path):
#     if name == "EfficientNet":
#         model = models.efficientnet_b0(weights=None)
#         model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

#     elif name == "MobileNet":
#         model = models.mobilenet_v3_large(weights=None)
#         model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

#     elif name == "ShuffleNet":
#         model = models.shufflenet_v2_x1_0(weights=None)
#         model.fc = nn.Linear(model.fc.in_features, 1)

#     model.load_state_dict(torch.load(path, map_location=device))
#     model.to(device)
#     model.eval()
#     return model

# # =========================
# # LOAD ALL MODELS (ONCE)
# # =========================
# models_loaded = {
#     name: load_model(name, path)
#     for name, path in MODEL_PATHS.items()
# }

# # =========================
# # EXTRACT FRAMES
# # =========================
# def extract_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []

#     frame_id = 0
#     count = 0

#     while cap.isOpened() and count < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#             if len(faces) > 0:
#                 x, y, w, h = faces[0]
#                 crop = frame[y:y+h, x:x+w]
#             else:
#                 crop = frame  # fallback

#             crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
#             crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
#             crop = Image.fromarray(crop)

#             frames.append(crop)
#             count += 1

#         frame_id += 1

#     cap.release()
#     return frames

# # =========================
# # SINGLE MODEL PREDICTION
# # =========================
# def predict_single_model(model, frames):
#     probs = []

#     for frame in frames:
#         img = transform(frame).unsqueeze(0).to(device)

#         with torch.no_grad():
#             out = model(img).view(-1)
#             prob = torch.sigmoid(out).item()
#             probs.append(prob)

#     return np.mean(probs)

# # =========================
# # MAIN ENSEMBLE FUNCTION
# # =========================
# def predict_video_ensemble(video_path):
#     frames = extract_frames(video_path)

#     if len(frames) == 0:
#         return {
#             "error": "No frames extracted from video"
#         }

#     model_scores = {}

#     for model_name, model in models_loaded.items():
#         prob = predict_single_model(model, frames)
#         model_scores[model_name] = round(prob * 100, 2)

#     # 🔥 FINAL ENSEMBLE SCORE
#     final_score = np.mean(list(model_scores.values()))

#     # 🔥 DECISION LOGIC
#     label = "FAKE" if final_score >= (THRESHOLD * 100) else "REAL"

#     return {
#         "final_score": round(final_score, 2),
#         "prediction": label,
#         "model_scores": model_scores
#     }
# import os
# import cv2
# import torch
# import torch.nn as nn
# import numpy as np
# from torchvision import transforms, models
# from PIL import Image

# # =========================
# # SETTINGS
# # =========================
# IMG_SIZE = 224
# MAX_FRAMES = 60
# SKIP = 5

# # 🔥 BEST THRESHOLD STRATEGY
# LOW_THRESHOLD = 0.33
# HIGH_THRESHOLD = 0.48

# # 🔥 WEIGHTED ENSEMBLE
# WEIGHTS = {
#     "EfficientNet": 0.5,
#     "MobileNet": 0.3,
#     "ShuffleNet": 0.2
# }

# MODEL_PATHS = {
#     "EfficientNet": "models/efficientnet_b0.pth",
#     "MobileNet": "models/mobilenetv3.pth",
#     "ShuffleNet": "models/shufflenet_v2.pth"
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # =========================
# # FACE DETECTOR
# # =========================
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # =========================
# # TRANSFORM
# # =========================
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
# ])

# # =========================
# # LOAD MODEL
# # =========================
# def load_model(name, path):
#     if name == "EfficientNet":
#         model = models.efficientnet_b0(weights=None)
#         model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

#     elif name == "MobileNet":
#         model = models.mobilenet_v3_large(weights=None)
#         model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

#     elif name == "ShuffleNet":
#         model = models.shufflenet_v2_x1_0(weights=None)
#         model.fc = nn.Linear(model.fc.in_features, 1)

#     model.load_state_dict(torch.load(path, map_location=device))
#     model.to(device)
#     model.eval()
#     return model

# # =========================
# # LOAD ALL MODELS (ONCE)
# # =========================
# models_loaded = {
#     name: load_model(name, path)
#     for name, path in MODEL_PATHS.items()
# }

# # =========================
# # FRAME EXTRACTION (OPTIMIZED)
# # =========================
# def extract_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []

#     frame_id = 0
#     count = 0

#     while cap.isOpened() and count < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#             if len(faces) > 0:
#                 x, y, w, h = faces[0]
#                 crop = frame[y:y+h, x:x+w]
#             else:
#                 crop = frame  # fallback

#             crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
#             crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
#             crop = Image.fromarray(crop)

#             frames.append(crop)
#             count += 1

#         frame_id += 1

#     cap.release()
#     return frames

# # =========================
# # SINGLE MODEL PREDICTION
# # =========================
# def predict_single_model(model, frames):
#     probs = []

#     for frame in frames:
#         img = transform(frame).unsqueeze(0).to(device)

#         with torch.no_grad():
#             out = model(img).view(-1)
#             prob = torch.sigmoid(out).item()
#             probs.append(prob)

#     return np.mean(probs)

# # =========================
# # FINAL ENSEMBLE FUNCTION
# # =========================
# def predict_video_ensemble(video_path):
#     frames = extract_frames(video_path)

#     if len(frames) == 0:
#         return {"error": "No frames extracted from video"}

#     model_probs = {}

#     for name, model in models_loaded.items():
#         prob = predict_single_model(model, frames)
#         model_probs[name] = prob

#     # 🔥 Weighted Ensemble
#     ensemble_prob = sum(
#         WEIGHTS[name] * model_probs[name]
#         for name in model_probs
#     )

#     # 🔥 Authenticity Score
#     authenticity_score = (1 - ensemble_prob) * 100

#     # 🔥 FINAL DECISION (DUAL THRESHOLD)
#     if ensemble_prob < LOW_THRESHOLD:
#         prediction = "REAL"
#     elif ensemble_prob > HIGH_THRESHOLD:
#         prediction = "FAKE"
#     else:
#         prediction = "UNCERTAIN"

#     return {
#         "final_score": round(authenticity_score, 2),
#         "prediction": prediction,
#         "ensemble_probability": round(ensemble_prob, 4),
#         "model_scores": {
#             name: round(prob * 100, 2)
#             for name, prob in model_probs.items()
#         }
#     }




# import os
# import cv2
# import torch
# import torch.nn as nn
# import numpy as np
# from torchvision import transforms, models
# from PIL import Image
# import csv
# import sys
# import argparse
# from pathlib import Path

# # ══════════════════════════════════════════════
# #  SETTINGS — tuned from your actual results
# # ══════════════════════════════════════════════
# IMG_SIZE    = 224
# MAX_FRAMES  = 60
# SKIP        = 5          # sample every 5th frame

# LOW_THRESHOLD  = 0.36    # below → REAL   (raised from 0.33 based on results)
# HIGH_THRESHOLD = 0.48    # above → FAKE

# WEIGHTS = {
#     "EfficientNet": 0.55,  # bumped up — strongest model
#     "MobileNet":    0.28,
#     "ShuffleNet":   0.17,
# }

# MODEL_PATHS = {
#     "EfficientNet": "models/efficientnet_b0.pth",
#     "MobileNet":    "models/mobilenetv3.pth",
#     "ShuffleNet":   "models/shufflenet_v2.pth",
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # ══════════════════════════════════════════════
# #  FACE DETECTOR  (Haar + fallback to DNN)
# # ══════════════════════════════════════════════
# haar_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # Optional: OpenCV DNN face detector for harder cases
# _dnn_net = None

# def _get_dnn_net():
#     """Load OpenCV DNN face detector once (more robust than Haar)."""
#     global _dnn_net
#     if _dnn_net is not None:
#         return _dnn_net
#     proto = cv2.data.haarcascades + "deploy.prototxt"
#     model = cv2.data.haarcascades + "res10_300x300_ssd_iter_140000.caffemodel"
#     if os.path.exists(proto) and os.path.exists(model):
#         _dnn_net = cv2.dnn.readNetFromCaffe(proto, model)
#     return _dnn_net

# def detect_face(frame_bgr):
#     """
#     Returns cropped face (BGR) or None.
#     Tries Haar first, then DNN, then returns None.
#     """
#     h, w = frame_bgr.shape[:2]
#     gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

#     # — Haar cascade —
#     faces = haar_cascade.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60)
#     )
#     if len(faces) > 0:
#         x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])   # biggest face
#         # add 10% margin so we don't clip the face tightly
#         pad_x = int(fw * 0.10)
#         pad_y = int(fh * 0.10)
#         x1 = max(0, x - pad_x)
#         y1 = max(0, y - pad_y)
#         x2 = min(w, x + fw + pad_x)
#         y2 = min(h, y + fh + pad_y)
#         return frame_bgr[y1:y2, x1:x2]

#     # — DNN fallback —
#     net = _get_dnn_net()
#     if net is not None:
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(frame_bgr, (300, 300)), 1.0,
#             (300, 300), (104, 117, 123)
#         )
#         net.setInput(blob)
#         detections = net.forward()
#         for i in range(detections.shape[2]):
#             conf = detections[0, 0, i, 2]
#             if conf > 0.6:
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 x1, y1, x2, y2 = box.astype(int)
#                 x1, y1 = max(0, x1), max(0, y1)
#                 x2, y2 = min(w, x2), min(h, y2)
#                 if x2 > x1 and y2 > y1:
#                     return frame_bgr[y1:y2, x1:x2]

#     return None   # no face found — caller will use full frame


# # ══════════════════════════════════════════════
# #  TRANSFORM
# # ══════════════════════════════════════════════
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225]),
# ])

# # ══════════════════════════════════════════════
# #  MODEL LOADER
# # ══════════════════════════════════════════════
# def load_model(name, path):
#     if not os.path.exists(path):
#         raise FileNotFoundError(
#             f"Model file not found: {path}\n"
#             f"Make sure '{path}' exists relative to where you run this script."
#         )
#     if name == "EfficientNet":
#         m = models.efficientnet_b0(weights=None)
#         m.classifier[1] = nn.Linear(m.classifier[1].in_features, 1)
#     elif name == "MobileNet":
#         m = models.mobilenet_v3_large(weights=None)
#         m.classifier[3] = nn.Linear(m.classifier[3].in_features, 1)
#     elif name == "ShuffleNet":
#         m = models.shufflenet_v2_x1_0(weights=None)
#         m.fc = nn.Linear(m.fc.in_features, 1)
#     else:
#         raise ValueError(f"Unknown model name: {name}")

#     m.load_state_dict(torch.load(path, map_location=device))
#     m.to(device)
#     m.eval()
#     return m


# def load_all_models():
#     print("Loading models...")
#     loaded = {}
#     for name, path in MODEL_PATHS.items():
#         try:
#             loaded[name] = load_model(name, path)
#             print(f"  ✓ {name}")
#         except FileNotFoundError as e:
#             print(f"  ✗ {e}")
#     if not loaded:
#         raise RuntimeError("No models could be loaded. Aborting.")
#     return loaded


# # ══════════════════════════════════════════════
# #  FRAME EXTRACTION  (robust version)
# # ══════════════════════════════════════════════
# def extract_frames(video_path):
#     """
#     Extract up to MAX_FRAMES face crops from a video.
#     Falls back to full frame when no face is detected.
#     Returns list of PIL Images.
#     """
#     if not os.path.exists(video_path):
#         print(f"  [WARN] File not found: {video_path}")
#         return []

#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print(f"  [WARN] Cannot open video: {video_path}")
#         return []

#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps          = cap.get(cv2.CAP_PROP_FPS) or 25.0

#     frames        = []
#     face_found    = 0
#     frame_id      = 0
#     sampled       = 0

#     while cap.isOpened() and sampled < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             face_crop = detect_face(frame)

#             if face_crop is not None:
#                 face_found += 1
#                 region = face_crop
#             else:
#                 region = frame   # full-frame fallback

#             # guard against degenerate crops (0-area from bad videos)
#             if region.shape[0] < 10 or region.shape[1] < 10:
#                 frame_id += 1
#                 continue

#             region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
#             pil_img    = Image.fromarray(region_rgb)
#             frames.append(pil_img)
#             sampled += 1

#         frame_id += 1

#     cap.release()

#     face_rate = face_found / max(sampled, 1) * 100
#     if face_rate < 20:
#         print(f"  [WARN] Low face detection rate ({face_rate:.0f}%) — "
#               f"results may be less reliable for {os.path.basename(video_path)}")

#     return frames


# # ══════════════════════════════════════════════
# #  PER-MODEL PREDICTION
# # ══════════════════════════════════════════════
# @torch.no_grad()
# def predict_single_model(model, frames):
#     probs = []
#     for frame in frames:
#         img = transform(frame).unsqueeze(0).to(device)
#         out  = model(img).view(-1)
#         prob = torch.sigmoid(out).item()
#         probs.append(prob)
#     return float(np.mean(probs))


# # ══════════════════════════════════════════════
# #  ENSEMBLE PREDICTION
# # ══════════════════════════════════════════════
# def predict_video(video_path, loaded_models):
#     """
#     Run full ensemble prediction on one video.
#     Returns a result dict.
#     """
#     frames = extract_frames(video_path)

#     if len(frames) == 0:
#         return {
#             "video":            os.path.basename(video_path),
#             "error":            "No frames extracted",
#             "prediction":       "ERROR",
#             "authenticity":     None,
#             "ensemble_prob":    None,
#             "model_scores":     {},
#         }

#     model_probs = {
#         name: predict_single_model(model, frames)
#         for name, model in loaded_models.items()
#     }

#     # weighted ensemble — only use models that were actually loaded
#     total_weight = sum(WEIGHTS[n] for n in model_probs)
#     ensemble_prob = sum(
#         (WEIGHTS[n] / total_weight) * model_probs[n]
#         for n in model_probs
#     )

#     authenticity = (1.0 - ensemble_prob) * 100.0

#     # if ensemble_prob < LOW_THRESHOLD:
#     #     prediction = "REAL"
#     # elif ensemble_prob > HIGH_THRESHOLD:
#     #     prediction = "FAKE"
#     # # else:
#     # #     prediction = "UNCERTAIN"
#     if ensemble_prob < LOW_THRESHOLD:
#         prediction = "REAL"
#     else:
#         prediction = "FAKE"

#     return {
#         "video":         os.path.basename(video_path),
#         "prediction":    prediction,
#         "authenticity":  round(authenticity, 2),
#         "ensemble_prob": round(ensemble_prob, 4),
#         "model_scores":  {n: round(p * 100, 2) for n, p in model_probs.items()},
#         "frames_used":   len(frames),
#     }


# # ══════════════════════════════════════════════
# #  BATCH RUNNER  (folder or list of files)
# # ══════════════════════════════════════════════
# SUPPORTED_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}

# def collect_videos(paths):
#     """Expand directories and filter to supported video extensions."""
#     videos = []
#     for p in paths:
#         p = Path(p)
#         if p.is_dir():
#             for ext in SUPPORTED_EXTS:
#                 videos.extend(sorted(p.rglob(f"*{ext}")))
#         elif p.suffix.lower() in SUPPORTED_EXTS:
#             videos.append(p)
#         else:
#             print(f"[SKIP] Not a supported video file: {p}")
#     return videos


# def run_batch(video_paths, loaded_models, output_csv=None):
#     results = []
#     total   = len(video_paths)

#     for i, vp in enumerate(video_paths, 1):
#         vp = str(vp)
#         print(f"\n[{i}/{total}] {os.path.basename(vp)}")
#         result = predict_video(vp, loaded_models)

#         tag = {
#             "REAL":      "✅ REAL",
#             "FAKE":      "🚨 FAKE",
#             # "UNCERTAIN": "⚠️  UNCERTAIN",
#             "ERROR":     "❌ ERROR",
#         }.get(result["prediction"], result["prediction"])

#         if result.get("error"):
#             print(f"  → {tag}  ({result['error']})")
#         else:
#             print(f"  → {tag}")
#             print(f"     Authenticity : {result['authenticity']:.1f}%")
#             print(f"     Ensemble prob: {result['ensemble_prob']:.4f}")
#             for name, score in result["model_scores"].items():
#                 print(f"     {name:<14}: {score:.1f}%")

#         results.append(result)

#     # ── summary ──────────────────────────────
#     print("\n" + "═" * 50)
#     print("SUMMARY")
#     print("═" * 50)
#     # counts = {"REAL": 0, "FAKE": 0, "UNCERTAIN": 0, "ERROR": 0}
#     counts = {"REAL": 0, "FAKE": 0, "ERROR": 0}
#     for r in results:
#         counts[r["prediction"]] = counts.get(r["prediction"], 0) + 1
#     for label, count in counts.items():
#         if count > 0:
#             print(f"  {label:<12}: {count}")
#     print(f"  {'TOTAL':<12}: {total}")

#     # ── CSV export ────────────────────────────
#     if output_csv:
#         fieldnames = [
#             "video", "prediction", "authenticity",
#             "ensemble_prob", "frames_used",
#             "EfficientNet", "MobileNet", "ShuffleNet",
#         ]
#         with open(output_csv, "w", newline="") as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#             for r in results:
#                 writer.writerow({
#                     "video":         r.get("video", ""),
#                     "prediction":    r.get("prediction", "ERROR"),
#                     "authenticity":  r.get("authenticity", ""),
#                     "ensemble_prob": r.get("ensemble_prob", ""),
#                     "frames_used":   r.get("frames_used", ""),
#                     "EfficientNet":  r.get("model_scores", {}).get("EfficientNet", ""),
#                     "MobileNet":     r.get("model_scores", {}).get("MobileNet", ""),
#                     "ShuffleNet":    r.get("model_scores", {}).get("ShuffleNet", ""),
#                 })
#         print(f"\nResults saved → {output_csv}")

#     return results


# # ══════════════════════════════════════════════
# #  ENTRY POINT
# # ══════════════════════════════════════════════
# def main():
#     parser = argparse.ArgumentParser(
#         description="Deepfake detection — ensemble inference"
#     )
#     parser.add_argument(
#         "input", nargs="+",
#         help="Video file(s) or folder(s) containing videos"
#     )
#     parser.add_argument(
#         "--output", "-o", default=None,
#         help="Optional CSV file to save results (e.g. results.csv)"
#     )
#     args = parser.parse_args()

#     video_paths = collect_videos(args.input)
#     if not video_paths:
#         print("No valid video files found. Exiting.")
#         sys.exit(1)

#     print(f"Found {len(video_paths)} video(s). Device: {device}\n")

#     loaded_models = load_all_models()
#     run_batch(video_paths, loaded_models, output_csv=args.output)


# if __name__ == "__main__":
#     main()



import os
import cv2
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image
import csv
import sys
import argparse
from pathlib import Path

# ══════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════
IMG_SIZE   = 224
MAX_FRAMES = 60
SKIP       = 5

# authenticity = (1 - ensemble_prob) * 100
# target decision boundary: authenticity >= 60  →  REAL
# equivalently:             ensemble_prob < 0.40 →  REAL
THRESHOLD = 0.40

WEIGHTS = {
    "EfficientNet": 0.55,
    "MobileNet":    0.28,
    "ShuffleNet":   0.17,
}

MODEL_PATHS = {
    "EfficientNet": "models/efficientnet_b0.pth",
    "MobileNet":    "models/mobilenetv3.pth",
    "ShuffleNet":   "models/shufflenet_v2.pth",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ══════════════════════════════════════════════
#  FACE DETECTOR  (Haar + DNN fallback)
# ══════════════════════════════════════════════
haar_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

_dnn_net = None

def _get_dnn_net():
    global _dnn_net
    if _dnn_net is not None:
        return _dnn_net
    proto   = cv2.data.haarcascades + "deploy.prototxt"
    weights = cv2.data.haarcascades + "res10_300x300_ssd_iter_140000.caffemodel"
    if os.path.exists(proto) and os.path.exists(weights):
        _dnn_net = cv2.dnn.readNetFromCaffe(proto, weights)
    return _dnn_net

def detect_face(frame_bgr):
    h, w = frame_bgr.shape[:2]
    gray  = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

    faces = haar_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60)
    )
    if len(faces) > 0:
        x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        pad_x = int(fw * 0.10)
        pad_y = int(fh * 0.10)
        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(w, x + fw + pad_x)
        y2 = min(h, y + fh + pad_y)
        return frame_bgr[y1:y2, x1:x2]

    net = _get_dnn_net()
    if net is not None:
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame_bgr, (300, 300)), 1.0,
            (300, 300), (104, 117, 123)
        )
        net.setInput(blob)
        detections = net.forward()
        for i in range(detections.shape[2]):
            conf = detections[0, 0, i, 2]
            if conf > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                if x2 > x1 and y2 > y1:
                    return frame_bgr[y1:y2, x1:x2]

    return None

# ══════════════════════════════════════════════
#  TRANSFORM
# ══════════════════════════════════════════════
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# ══════════════════════════════════════════════
#  MODEL LOADER
# ══════════════════════════════════════════════
def load_model(name, path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found: {path}\n"
            f"Make sure '{path}' exists relative to where you run this script."
        )
    if name == "EfficientNet":
        m = models.efficientnet_b0(weights=None)
        m.classifier[1] = nn.Linear(m.classifier[1].in_features, 1)
    elif name == "MobileNet":
        m = models.mobilenet_v3_large(weights=None)
        m.classifier[3] = nn.Linear(m.classifier[3].in_features, 1)
    elif name == "ShuffleNet":
        m = models.shufflenet_v2_x1_0(weights=None)
        m.fc = nn.Linear(m.fc.in_features, 1)
    else:
        raise ValueError(f"Unknown model name: {name}")

    m.load_state_dict(torch.load(path, map_location=device))
    m.to(device)
    m.eval()
    return m


def load_all_models():
    print("Loading models...")
    loaded = {}
    for name, path in MODEL_PATHS.items():
        try:
            loaded[name] = load_model(name, path)
            print(f"  ✓ {name}")
        except FileNotFoundError as e:
            print(f"  ✗ {e}")
    if not loaded:
        raise RuntimeError("No models could be loaded. Aborting.")
    return loaded

# ══════════════════════════════════════════════
#  FRAME EXTRACTION
# ══════════════════════════════════════════════
def extract_frames(video_path):
    if not os.path.exists(video_path):
        print(f"  [WARN] File not found: {video_path}")
        return []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  [WARN] Cannot open video: {video_path}")
        return []

    frames     = []
    face_found = 0
    frame_id   = 0
    sampled    = 0

    while cap.isOpened() and sampled < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % SKIP == 0:
            face_crop = detect_face(frame)

            if face_crop is not None:
                face_found += 1
                region = face_crop
            else:
                region = frame

            if region.shape[0] < 10 or region.shape[1] < 10:
                frame_id += 1
                continue

            region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(region_rgb))
            sampled += 1

        frame_id += 1

    cap.release()

    face_rate = face_found / max(sampled, 1) * 100
    if face_rate < 20:
        print(f"  [WARN] Low face detection rate ({face_rate:.0f}%) — "
              f"results may be less reliable for {os.path.basename(video_path)}")

    return frames

# ══════════════════════════════════════════════
#  PER-MODEL PREDICTION
# ══════════════════════════════════════════════
@torch.no_grad()
def predict_single_model(model, frames):
    probs = []
    for frame in frames:
        img  = transform(frame).unsqueeze(0).to(device)
        out  = model(img).view(-1)
        prob = torch.sigmoid(out).item()
        probs.append(prob)
    return float(np.mean(probs))

# ══════════════════════════════════════════════
#  ENSEMBLE PREDICTION
# ══════════════════════════════════════════════
def predict_video(video_path, loaded_models):
    frames = extract_frames(video_path)

    if len(frames) == 0:
        return {
            "video":         os.path.basename(video_path),
            "error":         "No frames extracted",
            "prediction":    "ERROR",
            "authenticity":  None,
            "ensemble_prob": None,
            "model_scores":  {},
            "frames_used":   0,
        }

    model_probs = {
        name: predict_single_model(model, frames)
        for name, model in loaded_models.items()
    }

    total_weight  = sum(WEIGHTS[n] for n in model_probs)
    ensemble_prob = sum(
        (WEIGHTS[n] / total_weight) * model_probs[n]
        for n in model_probs
    )

    # authenticity >= 60% → REAL  ≡  ensemble_prob < 0.40 → REAL
    authenticity = (1.0 - ensemble_prob) * 100.0
    prediction   = "REAL" if ensemble_prob < THRESHOLD else "FAKE"

    return {
        "video":         os.path.basename(video_path),
        "prediction":    prediction,
        "authenticity":  round(authenticity, 2),
        "ensemble_prob": round(ensemble_prob, 4),
        "model_scores":  {n: round(p * 100, 2) for n, p in model_probs.items()},
        "frames_used":   len(frames),
    }

# ══════════════════════════════════════════════
#  BATCH RUNNER
# ══════════════════════════════════════════════
SUPPORTED_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}

def collect_videos(paths):
    videos = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            for ext in SUPPORTED_EXTS:
                videos.extend(sorted(p.rglob(f"*{ext}")))
        elif p.suffix.lower() in SUPPORTED_EXTS:
            videos.append(p)
        else:
            print(f"[SKIP] Not a supported video file: {p}")
    return videos


def run_batch(video_paths, loaded_models, output_csv=None):
    results = []
    total   = len(video_paths)

    for i, vp in enumerate(video_paths, 1):
        vp = str(vp)
        print(f"\n[{i}/{total}] {os.path.basename(vp)}")
        result = predict_video(vp, loaded_models)

        tag = {
            "REAL":  "✅ REAL",
            "FAKE":  "🚨 FAKE",
            "ERROR": "❌ ERROR",
        }.get(result["prediction"], result["prediction"])

        if result.get("error"):
            print(f"  → {tag}  ({result['error']})")
        else:
            print(f"  → {tag}")
            print(f"     Authenticity : {result['authenticity']:.1f}%")
            print(f"     Ensemble prob: {result['ensemble_prob']:.4f}")
            for name, score in result["model_scores"].items():
                print(f"     {name:<14}: {score:.1f}%")

        results.append(result)

    print("\n" + "═" * 50)
    print("SUMMARY")
    print("═" * 50)
    counts = {"REAL": 0, "FAKE": 0, "ERROR": 0}
    for r in results:
        counts[r["prediction"]] = counts.get(r["prediction"], 0) + 1
    for label, count in counts.items():
        if count > 0:
            print(f"  {label:<12}: {count}")
    print(f"  {'TOTAL':<12}: {total}")

    if output_csv:
        fieldnames = [
            "video", "prediction", "authenticity",
            "ensemble_prob", "frames_used",
            "EfficientNet", "MobileNet", "ShuffleNet",
        ]
        with open(output_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "video":         r.get("video", ""),
                    "prediction":    r.get("prediction", "ERROR"),
                    "authenticity":  r.get("authenticity", ""),
                    "ensemble_prob": r.get("ensemble_prob", ""),
                    "frames_used":   r.get("frames_used", ""),
                    "EfficientNet":  r.get("model_scores", {}).get("EfficientNet", ""),
                    "MobileNet":     r.get("model_scores", {}).get("MobileNet", ""),
                    "ShuffleNet":    r.get("model_scores", {}).get("ShuffleNet", ""),
                })
        print(f"\nResults saved → {output_csv}")

    return results

# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Deepfake detection — ensemble inference"
    )
    parser.add_argument(
        "input", nargs="+",
        help="Video file(s) or folder(s) containing videos"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Optional CSV file to save results (e.g. results.csv)"
    )
    args = parser.parse_args()

    video_paths = collect_videos(args.input)
    if not video_paths:
        print("No valid video files found. Exiting.")
        sys.exit(1)

    print(f"Found {len(video_paths)} video(s). Device: {device}\n")

    loaded_models = load_all_models()
    run_batch(video_paths, loaded_models, output_csv=args.output)


if __name__ == "__main__":
    main()