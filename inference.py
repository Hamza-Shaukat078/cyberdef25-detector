import os
import glob
from datetime import datetime

import pandas as pd
import joblib

# Paths inside the container
INPUT_DIR = "/input/logs"
OUTPUT_DIR = "/output"
MODEL_PATH = "model.pkl"
FEATURE_NAMES_FILE = "feature_names.txt"

def log(msg):
    print(msg, flush=True)

def load_feature_names():
    if not os.path.exists(FEATURE_NAMES_FILE):
        raise FileNotFoundError(f"feature_names.txt not found")
    with open(FEATURE_NAMES_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def load_logs():
    if not os.path.isdir(INPUT_DIR):
        raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

    files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV log files found in {INPUT_DIR}")

    frames = []
    for path in files:
        log(f"Reading log file: {path}")
        df = pd.read_csv(path)
        df["__source_file"] = os.path.basename(path)
        frames.append(df)

    all_logs = pd.concat(frames, ignore_index=True)
    log(f"Loaded {len(all_logs)} log entries from {len(files)} file(s).")
    return all_logs

def preprocess(df, feature_names):
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    X = df[feature_names].fillna(0)
    return X

def main():
    log("Starting CYBER-DEF25 malware detection inference...")

    feature_names = load_feature_names()
    log(f"Using feature columns: {feature_names}")

    model = load_model()
    logs_df = load_logs()

    X = preprocess(logs_df, feature_names)

    log("Running model prediction...")
    preds = model.predict(X)

    try:
        probs = model.predict_proba(X)[:, 1]
    except Exception:
        probs = preds.astype(float)

    alerts = logs_df.copy()
    alerts["prediction"] = preds
    alerts["is_malicious"] = (alerts["prediction"] == 1).astype(int)
    alerts["malicious_score"] = probs
    alerts["inference_timestamp"] = datetime.utcnow().isoformat() + "Z"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "alerts.csv")
    alerts.to_csv(output_path, index=False)

    log(f"Inference completed. Results saved to {output_path}")

if __name__ == "__main__":
    main()
