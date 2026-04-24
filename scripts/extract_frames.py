# import cv2
# import os

# # -------- SETTINGS --------
# SOURCE_DIR = "ffpp_videos"      # raw videos
# TARGET_DIR = "data/train"      # training images
# MAX_FRAMES = 30                # per video
# SKIP = 5                       # take 1 frame every 5 frames
# # --------------------------

# def extract_from_video(video_path, save_dir, prefix):
#     cap = cv2.VideoCapture(video_path)
#     count = 0
#     frame_id = 0

#     while cap.isOpened() and count < MAX_FRAMES:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_id % SKIP == 0:
#             frame_name = f"{prefix}_f{count:03d}.jpg"
#             cv2.imwrite(os.path.join(save_dir, frame_name), frame)
#             count += 1

#         frame_id += 1

#     cap.release()


# def process_category(category):
#     src_path = os.path.join(SOURCE_DIR, category)
#     tgt_path = os.path.join(TARGET_DIR, category)
#     os.makedirs(tgt_path, exist_ok=True)

#     for video in os.listdir(src_path):
#         if not video.endswith(".mp4"):
#             continue

#         video_path = os.path.join(src_path, video)
#         video_name = os.path.splitext(video)[0]

#         print(f"[INFO] Processing {category}/{video}")
#         extract_from_video(video_path, tgt_path, video_name)


# if __name__ == "__main__":
#     process_category("real")
#     process_category("fake")
#     print("✅ Frame extraction completed")




# import cv2
# import os
# import random

# # -------- SETTINGS --------
# SOURCE_DIR = "ffpp_videos"      # input videos
# TARGET_DIR = "data/train"       # output frames
# MAX_FRAMES_PER_VIDEO = 30       # frames per video
# SKIP = 5                        # take 1 frame every N frames
# IMG_SIZE = 224                  # resize (model compatible)
# # --------------------------

# def extract_from_video(video_path, save_dir, prefix):
#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         print(f"[ERROR] Cannot open {video_path}")
#         return

#     count = 0
#     frame_id = 0

#     while cap.isOpened() and count < MAX_FRAMES_PER_VIDEO:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Frame sampling (uniform)
#         if frame_id % SKIP == 0:
#             # Resize for model compatibility
#             frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

#             # Unique filename (VERY IMPORTANT)
#             frame_name = f"{prefix}_frame{frame_id}_img{count}.jpg"

#             cv2.imwrite(os.path.join(save_dir, frame_name), frame)
#             count += 1

#         frame_id += 1

#     cap.release()
#     print(f"[INFO] Extracted {count} frames from {prefix}")


# def process_category(category):
#     src_path = os.path.join(SOURCE_DIR, category)
#     tgt_path = os.path.join(TARGET_DIR, category)

#     os.makedirs(tgt_path, exist_ok=True)

#     videos = [v for v in os.listdir(src_path) if v.endswith(".mp4")]
#     random.shuffle(videos)  # shuffle for randomness

#     for video in videos:
#         video_path = os.path.join(src_path, video)
#         video_name = os.path.splitext(video)[0]

#         print(f"[INFO] Processing {category}/{video}")
#         extract_from_video(video_path, tgt_path, video_name)


# if __name__ == "__main__":
#     process_category("real")
#     process_category("fake")
#     print("✅ Frame extraction completed successfully")







import cv2
import os
import random

# =========================
# SETTINGS
# =========================
SOURCE_DIR = "dfd"   # your main DFD folder
TARGET_DIR = "data/finetune_mix"

MAX_FRAMES_TOTAL = 2000      # per class (IMPORTANT)
MAX_FRAMES_PER_VIDEO = 30
SKIP = 5
IMG_SIZE = 224

# =========================
# CREATE OUTPUT FOLDERS
# =========================
os.makedirs(os.path.join(TARGET_DIR, "real"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "fake"), exist_ok=True)

# =========================
# FRAME EXTRACTION
# =========================
def extract_from_video(video_path, save_dir, prefix, current_count):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open {video_path}")
        return current_count

    frame_id = 0
    saved = 0

    while cap.isOpened() and saved < MAX_FRAMES_PER_VIDEO and current_count < MAX_FRAMES_TOTAL:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % SKIP == 0:
            frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

            filename = f"{prefix}_f{frame_id}_{current_count}.jpg"
            cv2.imwrite(os.path.join(save_dir, filename), frame)

            current_count += 1
            saved += 1

        frame_id += 1

    cap.release()
    return current_count

# =========================
# PROCESS CATEGORY (WORKS FOR BOTH FLAT + NESTED)
# =========================
def process_category(src_folder, target_label):
    src_path = os.path.join(SOURCE_DIR, src_folder)
    tgt_path = os.path.join(TARGET_DIR, target_label)

    videos = []

    # Works for both flat and nested folders
    for root, _, files in os.walk(src_path):
        for f in files:
            if f.endswith(".mp4"):
                videos.append(os.path.join(root, f))

    if len(videos) == 0:
        print(f"❌ No videos found in {src_path}")
        return

    print(f"📂 Found {len(videos)} videos in {src_folder}")

    random.shuffle(videos)

    count = 0

    for video_path in videos:
        if count >= MAX_FRAMES_TOTAL:
            break

        name = os.path.splitext(os.path.basename(video_path))[0]

        print(f"[INFO] Processing {name}")

        count = extract_from_video(video_path, tgt_path, name, count)

    print(f"✅ {target_label.upper()} DONE: {count} frames")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🔥 Extracting DFD REAL...")
    process_category("DFD_original_sequences", "real")

    print("\n🔥 Extracting DFD FAKE...")
    process_category("DFD_manipulated_sequences", "fake")

    print("\n🎉 DFD extraction completed successfully!")