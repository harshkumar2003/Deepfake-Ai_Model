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
# TEST_DIR = "data/test"
# IMG_SIZE = 224
# MAX_FRAMES = 30
# SKIP = 5

# MODELS = {
#     "EfficientNet": "models/efficientnet_b0.pth",
#     "MobileNet": "models/mobilenetv3.pth",
#     "ShuffleNet": "models/shufflenet_v2.pth"
# }

# # =========================
# # DEVICE
# # =========================
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)
# print("DEBUG → real=0, fake=1\n")

# # =========================
# # TRANSFORMS
# # =========================
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])

# # =========================
# # LOAD MODEL
# # =========================
# def load_model(name, path):
#     if name == "EfficientNet":
#         model = models.efficientnet_b0(pretrained=False)
#         model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

#     elif name == "MobileNet":
#         model = models.mobilenet_v3_large(pretrained=False)
#         model.classifier[3] = nn.Linear(model.classifier[3].in_features, 1)

#     elif name == "ShuffleNet":
#         model = models.shufflenet_v2_x1_0(pretrained=False)
#         model.fc = nn.Linear(model.fc.in_features, 1)

#     model.load_state_dict(torch.load(path, map_location=device))
#     model.to(device)
#     model.eval()
#     return model

# # =========================
# # FRAME EXTRACTION
# # =========================
# def extract_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []
#     count = 0
#     frame_id = 0

#     while cap.isOpened() and count < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = Image.fromarray(frame)
#             frames.append(frame)
#             count += 1

#         frame_id += 1

#     cap.release()
#     return frames

# # =========================
# # PREDICT VIDEO
# # =========================
# def predict_video(model, video_path):
#     frames = extract_frames(video_path)
#     probs = []

#     for frame in frames:
#         img = transform(frame).unsqueeze(0).to(device)

#         with torch.no_grad():
#             output = model(img).view(-1)
#             prob = torch.sigmoid(output).item()
#             probs.append(prob)

#     if len(probs) == 0:
#         return None

#     return np.mean(probs)  # probability of FAKE

# # =========================
# # TEST LOOP
# # =========================
# for model_name, model_path in MODELS.items():
#     print(f"\n🔍 Testing {model_name}")

#     model = load_model(model_name, model_path)

#     correct = 0
#     total = 0

#     for label_name in ["real", "fake"]:
#         folder = os.path.join(TEST_DIR, label_name)

#         # ✅ CORRECT LABEL MAPPING
#         true_label = 0 if label_name == "real" else 1

#         for video in os.listdir(folder):
#             video_path = os.path.join(folder, video)

#             prob = predict_video(model, video_path)

#             if prob is None:
#                 continue

#             pred = 1 if prob >= 0.5 else 0  # 1 = fake

#             # Debug print (optional but useful)
#             print(f"{video} | Fake Prob: {prob:.3f} | Pred: {pred} | True: {true_label}")

#             if pred == true_label:
#                 correct += 1
#             total += 1

#     accuracy = (correct / total) * 100

#     print(f"\n{model_name} Accuracy: {accuracy:.2f}%")

# print("\n✅ Testing Completed")




# import os
# import cv2
# import torch
# import torch.nn as nn
# import numpy as np
# from torchvision import transforms, models
# from PIL import Image
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# # =========================
# # SETTINGS
# # =========================
# TEST_DIR = "data/test"
# IMG_SIZE = 224
# MAX_FRAMES = 30
# SKIP = 5
# THRESHOLD = 0.6   # 🔥 FIXED

# MODELS = {
#     "EfficientNet": "models/efficientnet_finetuned.pth",
#     "MobileNet": "models/mobilenet_finetuned.pth",
#     "ShuffleNet": "models/shufflenet_finetuned.pth"
# }

# # =========================
# # DEVICE
# # =========================
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)

# # =========================
# # FACE DETECTOR (IMPORTANT FIX)
# # =========================
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # =========================
# # TRANSFORMS
# # =========================
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
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
# # FRAME EXTRACTION + FACE FILTER
# # =========================
# def extract_faces(video_path):
#     cap = cv2.VideoCapture(video_path)
#     faces = []
#     count = 0
#     frame_id = 0

#     while cap.isOpened() and count < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             detected = face_cascade.detectMultiScale(gray, 1.3, 5)

#             for (x, y, w, h) in detected:
#                 face = frame[y:y+h, x:x+w]
#                 face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#                 faces.append(Image.fromarray(face))
#                 count += 1
#                 break   # only one face per frame

#         frame_id += 1

#     cap.release()
#     return faces

# # =========================
# # PREDICT VIDEO
# # =========================
# def predict_video(model, video_path):
#     faces = extract_faces(video_path)

#     if len(faces) == 0:
#         return None

#     probs = []

#     for face in faces:
#         img = transform(face).unsqueeze(0).to(device)

#         with torch.no_grad():
#             output = model(img).view(-1)
#             prob = torch.sigmoid(output).item()
#             probs.append(prob)

#     # 🔥 MEDIAN (better than mean)
#     return np.median(probs)

# # =========================
# # TEST LOOP
# # =========================
# for model_name, model_path in MODELS.items():
#     print(f"\n🔍 Testing {model_name}")

#     model = load_model(model_name, model_path)

#     y_true = []
#     y_pred = []

#     for label_name in ["real", "fake"]:
#         folder = os.path.join(TEST_DIR, label_name)
#         true_label = 1 if label_name == "fake" else 0

#         for video in os.listdir(folder):
#             video_path = os.path.join(folder, video)

#             prob = predict_video(model, video_path)

#             if prob is None:
#                 continue

#             pred = 1 if prob >= THRESHOLD else 0

#             y_true.append(true_label)
#             y_pred.append(pred)

#             print(f"{video} | Prob: {prob:.3f} | Pred: {pred} | True: {true_label}")

#     # =========================
#     # METRICS (REVIEW FIX)
#     # =========================
#     acc = accuracy_score(y_true, y_pred)
#     prec = precision_score(y_true, y_pred)
#     rec = recall_score(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)

#     print(f"\n📊 {model_name} Results:")
#     print(f"Accuracy : {acc*100:.2f}%")
#     print(f"Precision: {prec:.2f}")
#     print(f"Recall   : {rec:.2f}")
#     print(f"F1 Score : {f1:.2f}")

# print("\n✅ Testing Completed")



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
# TEST_DIR = "data/test"
# IMG_SIZE = 224
# MAX_FRAMES = 30
# SKIP = 5

# MODELS = {
#     "efficientnet": "models/efficientnet_finetuned.pth",
#     "mobilenet": "models/mobilenet_finetuned.pth",
#     "shufflenet": "models/shufflenet_finetuned.pth"
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
#     if name == "efficientnet":
#         model = models.efficientnet_b0(weights=None)
#         model.classifier[1] = nn.Linear(model.classifier[1].in_features,1)

#     elif name == "mobilenet":
#         model = models.mobilenet_v3_large(weights=None)
#         model.classifier[3] = nn.Linear(model.classifier[3].in_features,1)

#     elif name == "shufflenet":
#         model = models.shufflenet_v2_x1_0(weights=None)
#         model.fc = nn.Linear(model.fc.in_features,1)

#     model.load_state_dict(torch.load(path, map_location=device))
#     model.to(device)
#     model.eval()

#     return model

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
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
#             frame = Image.fromarray(frame)
#             frames.append(frame)
#             count += 1

#         frame_id += 1

#     cap.release()
#     return frames

# # =========================
# # PREDICT VIDEO
# # =========================
# def predict_video(models, video_path):
#     frames = extract_frames(video_path)
#     if len(frames) == 0:
#         return None

#     model_probs = []

#     for name, model in models.items():
#         probs = []

#         for frame in frames:
#             img = transform(frame).unsqueeze(0).to(device)

#             with torch.no_grad():
#                 out = model(img).view(-1)
#                 prob = torch.sigmoid(out).item()
#                 probs.append(prob)

#         model_probs.append(np.mean(probs))

#     # Ensemble
#     final_prob = np.mean(model_probs)

#     return final_prob

# # =========================
# # MAIN TEST LOOP
# # =========================
# models_loaded = {name: load_model(name, path) for name, path in MODELS.items()}

# correct = 0
# total = 0

# for label_name in ["real", "fake"]:
#     folder = os.path.join(TEST_DIR, label_name)
#     true_label = 1 if label_name == "real" else 0

#     for video in os.listdir(folder):
#         video_path = os.path.join(folder, video)

#         prob = predict_video(models_loaded, video_path)
#         if prob is None:
#             continue

#         pred = 1 if prob >= 0.5 else 0

#         print(f"{video} | Prob: {prob:.3f} | Pred: {pred} | True: {true_label}")

#         if pred == true_label:
#             correct += 1

#         total += 1

# accuracy = (correct / total) * 100

# print("\n==========================")
# print(f"FINAL ENSEMBLE ACCURACY: {accuracy:.2f}%")
# print("==========================")




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
# TEST_DIR = "data/test"
# IMG_SIZE = 224
# MAX_FRAMES = 30
# SKIP = 5

# THRESHOLD = 0.45   # 🔥 FIXED

# MODELS = {
#     "efficientnet": "models/efficientnet_finetuned.pth",
#     "mobilenet": "models/mobilenet_finetuned.pth",
#     "shufflenet": "models/shufflenet_finetuned.pth"
# }

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # =========================
# # TRANSFORM
# # =========================
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
# ])
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # =========================
# # LOAD MODEL
# # =========================
# def load_model(name, path):
#     if name == "efficientnet":
#         model = models.efficientnet_b0(weights=None)
#         model.classifier[1] = nn.Linear(model.classifier[1].in_features,1)

#     elif name == "mobilenet":
#         model = models.mobilenet_v3_large(weights=None)
#         model.classifier[3] = nn.Linear(model.classifier[3].in_features,1)

#     elif name == "shufflenet":
#         model = models.shufflenet_v2_x1_0(weights=None)
#         model.fc = nn.Linear(model.fc.in_features,1)

#     model.load_state_dict(torch.load(path, map_location=device))
#     model.to(device)
#     model.eval()
#     return model

# # =========================
# # EXTRACT FRAMES
# # =========================
# def extract_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []

#     frame_id = 0
#     count = 0

#     while cap.isOpened() and count < 50:   # 🔥 increased
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % 5 == 0:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#             if len(faces) > 0:   # 🔥 ONLY KEEP FACE FRAMES
#                 x, y, w, h = faces[0]
#                 face = frame[y:y+h, x:x+w]

#                 face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#                 face = cv2.resize(face, (224, 224))
#                 face = Image.fromarray(face)

#                 frames.append(face)
#                 count += 1

#         frame_id += 1

#     cap.release()
#     return frames
# # =========================
# # PREDICT VIDEO
# # =========================
# def predict_video(models, video_path):
#     frames = extract_frames(video_path)
#     if len(frames) == 0:
#         return None

#     model_probs = []

#     for name, model in models.items():
#         probs = []

#         for frame in frames:
#             img = transform(frame).unsqueeze(0).to(device)

#             with torch.no_grad():
#                 out = model(img).view(-1)
#                 prob = torch.sigmoid(out).item()
#                 probs.append(prob)

#         model_probs.append(np.mean(probs))

#     final_prob = np.mean(model_probs)
#     return final_prob

# # =========================
# # VERDICT FUNCTION
# # =========================
# def get_verdict(prob):
#     if prob < 0.40:
#         return 0, "Fake"
#     elif prob < 0.60:
#         return None, "Uncertain"
#     else:
#         return 1, "Real"

# # =========================
# # MAIN TEST LOOP
# # =========================
# models_loaded = {name: load_model(name, path) for name, path in MODELS.items()}

# correct = 0
# total = 0
# uncertain = 0

# for label_name in ["real", "fake"]:
#     folder = os.path.join(TEST_DIR, label_name)
#     true_label = 1 if label_name == "real" else 0

#     for video in os.listdir(folder):
#         video_path = os.path.join(folder, video)

#         prob = predict_video(models_loaded, video_path)
#         if prob is None:
#             continue

#         pred, verdict = get_verdict(prob)

#         # fallback if uncertain → use threshold
#         if pred is None:
#             uncertain += 1
#             pred = 1 if prob >= THRESHOLD else 0

#         print(f"{video} | Prob: {prob:.3f} | Pred: {pred} | True: {true_label} | {verdict}")

#         if pred == true_label:
#             correct += 1

#         total += 1

# accuracy = (correct / total) * 100

# print("\n==========================")
# print(f"Accuracy: {accuracy:.2f}%")
# print(f"Uncertain cases: {uncertain}")
# print("==========================")

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
# TEST_DIR = "data/test-dfd"
# IMG_SIZE = 224
# MAX_FRAMES = 50
# SKIP = 5
# THRESHOLD = 0.45

# MODELS = {
#     "ShuffleNet": "models/shufflenet_v2.pth"
#     "EfficientNet": "models/efficientnet_b0.pth",
#     "MobileNet": "models/mobilenetv3.pth",
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
# # EXTRACT FRAMES (FACE ONLY)
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
#                 face = frame[y:y+h, x:x+w]

#                 face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#                 face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
#                 face = Image.fromarray(face)

#                 frames.append(face)
#                 count += 1

#         frame_id += 1

#     cap.release()
#     return frames

# # =========================
# # PREDICT VIDEO
# # =========================
# def predict_video(model, video_path):
#     frames = extract_frames(video_path)
#     if len(frames) == 0:
#         return None

#     probs = []

#     for frame in frames:
#         img = transform(frame).unsqueeze(0).to(device)

#         with torch.no_grad():
#             out = model(img).view(-1)
#             prob = torch.sigmoid(out).item()
#             probs.append(prob)

#     return np.mean(probs)

# # =========================
# # TEST LOOP
# # =========================
# for model_name, model_path in MODELS.items():

#     print(f"\n🔥 Testing {model_name}")
#     model = load_model(model_name, model_path)

#     correct = 0
#     total = 0

#     for label_name in ["real", "fake"]:

#         folder = os.path.join(TEST_DIR, label_name)

#         # ✅ CORRECT LABEL
#         true_label = 0 if label_name == "real" else 1

#         for video in os.listdir(folder):
#             video_path = os.path.join(folder, video)

#             prob = predict_video(model, video_path)
#             if prob is None:
#                 continue

#             # ✅ FINAL FIX (IMPORTANT)
#             pred = 1 if prob >= THRESHOLD else 0

#             print(f"{video} | Prob: {prob:.3f} | Pred: {pred} | True: {true_label}")

#             if pred == true_label:
#                 correct += 1
#             total += 1

#     accuracy = (correct / total) * 100

#     print(f"\n✅ {model_name} Accuracy: {accuracy:.2f}%")

# print("\n🎯 ALL MODELS TESTED")




import os
import cv2
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms, models
from PIL import Image

# =========================
# SETTINGS
# =========================
TEST_DIR = "data/test-dfd"
IMG_SIZE = 224
MAX_FRAMES = 60   # 🔥 increased
SKIP = 5
THRESHOLD = 0.45

# ✅ FIXED (comma + order clean)
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
# EXTRACT FRAMES (FIXED 🔥)
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

            # 🔥 IMPORTANT FIX
            if len(faces) > 0:
                x, y, w, h = faces[0]
                crop = frame[y:y+h, x:x+w]
            else:
                crop = frame   # 🔥 fallback (VERY IMPORTANT)

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
# TEST LOOP
# =========================
for model_name, model_path in MODELS.items():

    print(f"\n🔥 Testing {model_name}")
    model = load_model(model_name, model_path)

    correct = 0
    total = 0

    for label_name in ["real", "fake"]:

        folder = os.path.join(TEST_DIR, label_name)
        true_label = 0 if label_name == "real" else 1

        for video in os.listdir(folder):
            video_path = os.path.join(folder, video)

            prob = predict_video(model, video_path)
            if prob is None:
                continue

            pred = 1 if prob >= THRESHOLD else 0

            print(f"{video} | Prob: {prob:.3f} | Pred: {pred} | True: {true_label}")

            if pred == true_label:
                correct += 1
            total += 1

    accuracy = (correct / total) * 100

    print(f"\n✅ {model_name} Accuracy: {accuracy:.2f}%")

print("\n🎯 ALL MODELS TESTED")