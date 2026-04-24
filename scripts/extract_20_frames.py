import cv2
import os

def extract_20_frames(video_path, output_dir, num_frames=20):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < num_frames:
        raise ValueError("Video too short to extract required frames")

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
    print(f"✅ Extracted {saved} frames from video.")

# =========================
# USAGE
# =========================
if __name__ == "__main__":
    VIDEO_PATH = "data/test/video/real/real-v-3.mp4"
    OUTPUT_DIR = "data/test/frames"

    extract_20_frames(VIDEO_PATH, OUTPUT_DIR)
