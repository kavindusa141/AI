import os, csv, joblib
from sklearn.neural_network import MLPRegressor

MODEL_PATH='models/model.pkl'
DATA_PATH='data/training_data.csv'

def load_model():
    return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def train_model():
    X=[]; y=[]
    with open(DATA_PATH) as f:
        r=csv.DictReader(f)
        for row in r:
            X.append([float(row[k]) for k in ['cost','days','travel','interest_match','activity_match']])
            y.append(float(row['rating']))
    if len(X)<2: return None
    m=MLPRegressor(hidden_layer_sizes=(8,4),max_iter=400)
    m.fit(X,y); joblib.dump(m,MODEL_PATH); return m
