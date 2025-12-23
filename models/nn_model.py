import os
import csv
import joblib
from sklearn.neural_network import MLPRegressor

# Path Configuration
# We use absolute paths or relative to the main execution script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")

def load_model():
    """
    Loads the trained AI brain.
    """
    try:
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
    except Exception:
        # If model is corrupted/old version, delete it
        try:
            os.remove(MODEL_PATH)
            print("⚠️ Old model was corrupted and removed.")
        except Exception:
            pass
    return None

def train_model():
    """
    Retrains the neural network using the CSV data.
    """
    if not os.path.exists(DATA_PATH):
        print("ℹ️ No training data found yet.")
        return None

    X, y = [], []

    # 1. READ DATA (Robust Mode)
    # We use standard csv.reader to avoid "Missing Header" errors
    with open(DATA_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty lines
            if not row:
                continue
                
            # Skip header line if it exists (check if first item is text)
            if row[0].startswith("norm") or row[0].isalpha():
                continue

            try:
                # We expect 5 Features + 1 Rating = 6 Columns
                # Matches agent/utility.py: extract_features()
                if len(row) < 6:
                    continue
                    
                # Features: Columns 0 to 4
                features = [float(val) for val in row[:5]]
                
                # Target: Column 5 (Rating)
                rating = float(row[5])

                X.append(features)
                y.append(rating)
            except ValueError:
                continue

    # 2. DATA SUFFICIENCY CHECK
    # We need at least 10 samples to train a decent "Baby AI"
    # (lowered from 20 for easier demoing)
    if len(X) < 10:
        print(f"ℹ️ Not enough data to train yet ({len(X)}/10 samples).")
        return None

    # 3. CONFIGURE BRAIN (Neural Network)
    # A simple Multi-Layer Perceptron
    model = MLPRegressor(
        hidden_layer_sizes=(16, 8), # Two thinking layers
        activation="relu",          # Standard AI activation
        solver="adam",              # Good optimizer for small data
        max_iter=1000,              # Allow it time to learn
        random_state=42             # Reproducible results
    )

    # 4. TRAIN
    print(f"🧠 Training AI on {len(X)} experiences...")
    model.fit(X, y)

    # 5. SAVE
    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained and saved.")

    return model