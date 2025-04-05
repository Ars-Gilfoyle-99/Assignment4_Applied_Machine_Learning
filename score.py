
import joblib
import os
import logging
from sklearn.base import BaseEstimator

logging.basicConfig(level=logging.INFO)

MODEL_PATH = "best_model.pkl"

def load_model(path=MODEL_PATH) -> BaseEstimator:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}")
    return joblib.load(path)

def score(text: str, model: BaseEstimator, threshold: float) -> tuple:
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1")
    if text.strip() == "":
        return (0, 0.0)
    prob = model.predict_proba([text])[0][1]
    pred = int(prob >= threshold)
    return (pred, float(prob))
