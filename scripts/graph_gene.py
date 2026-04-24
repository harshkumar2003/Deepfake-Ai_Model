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

# =========================
# GRAPH 1: MODEL-WISE SCORE COMPARISON (LAST VIDEO)
# =========================
row = df.iloc[-1]

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

plt.figure(figsize=(10,5))
plt.bar(models, scores)
plt.axhline(60, linestyle="--", label="Likely Genuine")
plt.axhline(40, linestyle="--", label="Likely Deepfake")
plt.ylabel("Authenticity Score")
plt.title("Model-wise Authenticity Score Comparison")
plt.xticks(rotation=20)
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/model_score_comparison.png", dpi=300)
plt.close()

# =========================
# GRAPH 2: BASELINE vs RANDOM vs ENSEMBLE
# =========================
baseline_avg = (
    row["Xception (Non-Random)"] +
    row["ResNet-50 (Non-Random)"]
) / 2

random_avg = (
    row["EfficientNet-B0 (Random)"] +
    row["MobileNetV3 (Random)"] +
    row["ShuffleNet-V2 (Random)"]
) / 3

ensemble = row["Ensemble"]

plt.figure(figsize=(6,4))
plt.bar(
    ["Baseline Avg", "Random Avg", "Ensemble"],
    [baseline_avg, random_avg, ensemble]
)
plt.ylabel("Authenticity Score")
plt.title("Baseline vs Random Models vs Ensemble")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/baseline_vs_random.png", dpi=300)
plt.close()

# =========================
# GRAPH 3: ENSEMBLE SCORE DISTRIBUTION (REAL vs FAKE)
# =========================
real_scores = df[df["Video"].str.contains("real")]["Ensemble"]
fake_scores = df[df["Video"].str.contains("fake")]["Ensemble"]

plt.figure(figsize=(7,5))
plt.boxplot([real_scores, fake_scores], labels=["Real Videos", "Fake Videos"])
plt.axhline(60, linestyle="--", label="Likely Genuine")
plt.axhline(40, linestyle="--", label="Likely Deepfake")
plt.ylabel("Authenticity Score")
plt.title("Distribution of Ensemble Authenticity Scores")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/ensemble_distribution.png", dpi=300)
plt.close()

# =========================
# GRAPH 4: MODEL STABILITY (VARIANCE)
# =========================
variances = [df[m].var() for m in models]

plt.figure(figsize=(8,4))
plt.bar(models, variances)
plt.ylabel("Score Variance (Lower is Better)")
plt.title("Model Stability Comparison")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/model_variance.png", dpi=300)
plt.close()

# =========================
# GRAPH 5: BASELINE OVERCONFIDENCE vs ENSEMBLE
# =========================
baseline_all = (
    df["Xception (Non-Random)"] +
    df["ResNet-50 (Non-Random)"]
) / 2

plt.figure(figsize=(7,5))
plt.scatter(baseline_all, df["Ensemble"])
plt.plot([0,100], [0,100], linestyle="--", label="Ideal Alignment")
plt.xlabel("Baseline Average Score")
plt.ylabel("Ensemble Authenticity Score")
plt.title("Baseline Overconfidence vs Ensemble Moderation")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/baseline_vs_ensemble_scatter.png", dpi=300)
plt.close()

# =========================
# DONE
# =========================
print("✅ All research-grade graphs generated successfully!")
print("📊 Saved files:")
print(" - model_score_comparison.png")
print(" - baseline_vs_random.png")
print(" - ensemble_distribution.png")
print(" - model_variance.png")
print(" - baseline_vs_ensemble_scatter.png")
