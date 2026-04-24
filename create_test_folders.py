import os
import random
import shutil

# =============================================================
# create_test_folders.py
# -------------------------------------------------------------
# Takes frames from data/train/real and data/train/fake
# and creates test video folders:
#
#   data/test/real/
#       video_real_01/  → 20 frames
#       video_real_02/  → 20 frames
#       ...up to 25 folders
#
#   data/test/fake/
#       video_fake_01/  → 20 frames
#       video_fake_02/  → 20 frames
#       ...up to 25 folders
#
# Frames are COPIED not moved — training data stays intact
# =============================================================

# =========================
# SETTINGS
# =========================
TRAIN_REAL       = "data/train/real"
TRAIN_FAKE       = "data/train/fake"
TEST_REAL        = "data/test/real"
TEST_FAKE        = "data/test/fake"

FRAMES_PER_VIDEO = 20    # 20 frames per test video
NUM_TEST_VIDEOS  = 25    # 25 real + 25 fake = 50 test videos total

# =========================
# FUNCTION
# =========================
def create_test_videos(train_dir, test_dir, label, num_videos, frames_per_video):
    os.makedirs(test_dir, exist_ok=True)

    # Get all available frames
    all_frames = [
        f for f in os.listdir(train_dir)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    total_needed = num_videos * frames_per_video
    if len(all_frames) < total_needed:
        print(f"  WARNING: Only {len(all_frames)} frames available.")
        num_videos = len(all_frames) // frames_per_video
        print(f"  Reducing to {num_videos} test videos.")

    # Shuffle randomly
    random.shuffle(all_frames)
    selected_frames = all_frames[:num_videos * frames_per_video]

    print(f"\nCreating {num_videos} {label} test video folders...")

    created = 0
    for i in range(num_videos):
        video_frames = selected_frames[i * frames_per_video : (i + 1) * frames_per_video]
        video_folder = os.path.join(test_dir, f"video_{label}_{i+1:02d}")

        # Skip if already exists
        if os.path.exists(video_folder):
            print(f"  SKIP (already exists): video_{label}_{i+1:02d}")
            continue

        os.makedirs(video_folder, exist_ok=True)

        for j, frame_name in enumerate(video_frames):
            src = os.path.join(train_dir, frame_name)
            dst = os.path.join(video_folder, f"frame_{j:03d}.jpg")
            shutil.copy2(src, dst)

        print(f"  Created: video_{label}_{i+1:02d}/ ({frames_per_video} frames)")
        created += 1

    print(f"\n{created} new {label} folders created in {test_dir}")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("=" * 50)
    print("  Creating test video folders")
    print(f"  {NUM_TEST_VIDEOS} real + {NUM_TEST_VIDEOS} fake = {NUM_TEST_VIDEOS*2} total")
    print("=" * 50)

    create_test_videos(TRAIN_REAL, TEST_REAL, "real", NUM_TEST_VIDEOS, FRAMES_PER_VIDEO)
    create_test_videos(TRAIN_FAKE, TEST_FAKE, "fake", NUM_TEST_VIDEOS, FRAMES_PER_VIDEO)

    # Final count
    real_count = len([d for d in os.listdir(TEST_REAL) if os.path.isdir(os.path.join(TEST_REAL, d))])
    fake_count = len([d for d in os.listdir(TEST_FAKE) if os.path.isdir(os.path.join(TEST_FAKE, d))])

    print("\n" + "=" * 50)
    print("  DONE!")
    print(f"  Real test videos : {real_count}")
    print(f"  Fake test videos : {fake_count}")
    print(f"  Total            : {real_count + fake_count}")
    print("\n  Now run:")
    print("  python setup_and_evaluate.py")
    print("=" * 50)