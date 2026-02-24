import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    cohen_kappa_score,
    top_k_accuracy_score
)

# =========================
# Load dataset
# =========================
X = np.load("X_raw.npy")
y = np.load("y_raw.npy")

# =========================
# Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================
# Train KNN
# =========================
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# =========================
# Predictions
# =========================
y_pred = knn.predict(X_test)

# =========================
# Accuracy Metrics
# =========================
overall_acc = accuracy_score(y_test, y_pred)
balanced_acc = balanced_accuracy_score(y_test, y_pred)
kappa = cohen_kappa_score(y_test, y_pred)
top3_acc = top_k_accuracy_score(y_test, knn.predict_proba(X_test), k=3)

print(f"Overall Accuracy: {overall_acc*100:.2f}%")
print(f"Balanced Accuracy: {balanced_acc*100:.2f}%")
print(f"Cohen's Kappa: {kappa:.4f}")
print(f"Top-3 Accuracy: {top3_acc*100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# =========================
# Optional: Cross-validation Accuracy
# =========================
cv_scores = cross_val_score(knn, X, y, cv=5)
print(f"\n5-Fold Cross-Validation Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
