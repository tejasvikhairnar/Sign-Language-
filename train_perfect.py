import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import time

# Load optimized dataset
print("Loading optimized data...")
try:
    X = np.load("X_optimized.npy")
    y = np.load("y_optimized.npy")
except FileNotFoundError:
    print("X_optimized.npy not found. Using X.npy as fallback.")
    X = np.load("X.npy")
    y = np.load("y.npy")

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Dataset size: {len(X)} samples")
print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")

# Models to compare
models = {
    "ExtraTrees": ExtraTreesClassifier(n_estimators=100, random_state=42),
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
}

best_overall_model = None
best_overall_acc = 0

for name, model in models.items():
    print(f"\n=== Evaluating {name} ===")
    start_time = time.time()
    
    # 5-Fold Cross Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Fit on full training set
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Set Accuracy: {acc:.4f}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
    
    if acc > best_overall_acc:
        best_overall_acc = acc
        best_overall_model = (name, model)

print(f"\n🏆 Best Model: {best_overall_model[0]} with {best_overall_acc*100:.2f}% accuracy")

# Final training on best model with slight tuning if it's the winner
name, model = best_overall_model
print(f"Saving {name}_optimized_model.pkl...")
joblib.dump(model, f"{name}_optimized_model.pkl")

# Generate report for the winner
y_pred = model.predict(X_test)
print("\nFinal Classification Report:")
print(classification_report(y_test, y_pred))

# Update final model link (optional, for backend)
# joblib.dump(model, "KNN_model.pkl") # If we want to replace the backend model directly
