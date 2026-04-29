import joblib
import numpy as np
from base_predictor import BasePredictor


class RFPredictor(BasePredictor):
    def __init__(self):
        self.model = joblib.load("predictor/random_forest_asl_model.pkl")
        self.encoder = joblib.load("predictor/label_encoder.pkl")

    def predict(self, features):
        if features is None:
            return None, 0.0

        X = np.array(features).reshape(1, -1)
        probs = self.model.predict_proba(X)[0]

        idx = probs.argmax()
        return self.encoder.inverse_transform([idx])[0], float(probs[idx])
