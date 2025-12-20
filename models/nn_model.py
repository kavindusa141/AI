import os
import csv
import joblib
from sklearn.neural_network import MLPRegressor

MODEL_PATH = "models/model.pkl"
DATA_PATH = "data/training_data.csv"

FEATURES = [
    "norm_cost",
    "norm_days",
    "norm_travel",
    "interest_match",
    "activity_match"
]


def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
    except Exception:
        return None
    return None


def train_model():
    if not os.path.exists(DATA_PATH):
        return None

    X, y = [], []

    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                X.append([float(row[k]) for k in FEATURES])
                y.append(float(row["rating"]))
            except (KeyError, ValueError):
                continue

    # 🔹 Minimum data threshold
    if len(X) < 20:
        return None

    model = MLPRegressor(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42
    )

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

    return model
