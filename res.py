import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("dfdc_results.csv")

THRESHOLD = 0.4164

y_true = df["True_Label"]
y_pred = df["Ensemble_Prob"].apply(lambda x: 1 if x >= THRESHOLD else 0)

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Accuracy:", acc)
print("Precision:", prec)
print("Recall:", rec)
print("F1:", f1)