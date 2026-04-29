import pickle
from predictor_manager import PredictorManager
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# ================= LOAD DATASET =================
with open("asl_keypoints_dataset.pkl", "rb") as f:
    data = pickle.load(f)

# Safe extraction
if "X" in data:
    X = data["X"]
elif "features" in data:
    X = data["features"]
else:
    raise KeyError("❌ Features not found in dataset")

if "y" in data:
    y = data["y"]
elif "labels" in data:
    y = data["labels"]
else:
    raise KeyError("❌ Labels not found in dataset")

print(f"✅ Dataset loaded: {len(X)} samples")

# ================= SPLIT TEST DATA (20%) =================
_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================= INIT ENSEMBLE =================
predictor = PredictorManager()

y_true = []
y_pred = []

# ================= RUN EVALUATION =================
for i in range(len(X_test)):
    features = X_test[i]
    true_label = y_test[i]

    pred_label, _ = predictor.predict(features)
    if pred_label is None:
        continue

    y_true.append(true_label)
    y_pred.append(pred_label)

print("\n========== METRICS ==========")
print(f"Accuracy  : {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision : {precision_score(y_true, y_pred, average='weighted', zero_division=0):.4f}")
print(f"Recall    : {recall_score(y_true, y_pred, average='weighted', zero_division=0):.4f}")
print(f"F1-score  : {f1_score(y_true, y_pred, average='weighted', zero_division=0):.4f}")

# ================= CONFUSION MATRIX =================
cm = confusion_matrix(y_true, y_pred)
labels = sorted(list(set(y_true)))  # get unique class labels

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()
