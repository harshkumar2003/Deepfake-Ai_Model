import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# PATHS
# =========================
CSV_PATH = "results/summary_results.csv"
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)

# Take the last evaluated video
row = df.iloc[-1]

# =========================
# GRAPH 1: MODEL-WISE SCORES
# =========================
models = [
    "Xception (Non-Random)",
    "ResNet-50 (Non-Random)",
    "EfficientNet-B0 (Random)",
    "MobileNetV3 (Random)",
    "ShuffleNet-V2 (Random)"
]

scores = [
    row["Xception (Non-Random)"],
    row["ResNet-50 (Non-Random)"],
    row["EfficientNet-B0 (Random)"],
    row["MobileNetV3 (Random)"],
    row["ShuffleNet-V2 (Random)"]
]

plt.figure(figsize=(10, 5))
plt.bar(models, scores)
plt.axhline(60, linestyle="--", label="Likely Genuine Threshold")
plt.axhline(40, linestyle="--", label="Likely Deepfake Threshold")

plt.ylabel("Authenticity Score")
plt.title("Model-wise Authenticity Score Comparison")
plt.xticks(rotation=20)
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "model_score_comparison.png"), dpi=300)
plt.close()

# =========================
# GRAPH 2: BASELINE vs RANDOM vs ENSEMBLE
# =========================
baseline_avg = (row["Xception (Non-Random)"] + row["ResNet-50 (Non-Random)"]) / 2
random_avg = (
    row["EfficientNet-B0 (Random)"] +
    row["MobileNetV3 (Random)"] +
    row["ShuffleNet-V2 (Random)"]
) / 3
ensemble = row["Ensemble"]

labels = ["Baseline Avg", "Random Avg", "Ensemble"]
values = [baseline_avg, random_avg, ensemble]

plt.figure(figsize=(6, 4))
plt.bar(labels, values)
plt.ylabel("Authenticity Score")
plt.title("Baseline vs Random Models vs Ensemble")
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "baseline_vs_random.png"), dpi=300)
plt.close()

# =========================
# DONE
# =========================
print("✅ Both graphs generated successfully!")
print("📊 Saved files:")
print(" - results/model_score_comparison.png")
print(" - results/baseline_vs_random.png")
