import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve

df = pd.read_csv("dfdc_results.csv")

y_true = df["True_Label"].values
y_prob = df["Ensemble_Prob"].values

fpr, tpr, thresholds = roc_curve(y_true, y_prob)

# Youden’s J = TPR - FPR
j = tpr - fpr
best_idx = np.argmax(j)
best_th = thresholds[best_idx]

print("Best threshold:", best_th)