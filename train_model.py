import os
import joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

FEATURES_FILE = "feature_names.txt"
MODEL_PATH = "model.pkl"

def load_feature_names():
    with open(FEATURES_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def train_and_save_model():
    feature_names = load_feature_names()
    n_features = len(feature_names)

    # Create synthetic training data
    X, y = make_classification(
        n_samples=500,
        n_features=n_features,
        n_informative=n_features,
        n_redundant=0,
        random_state=42,
    )

    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
