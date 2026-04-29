import lightgbm as lgb
import joblib
import numpy as np
from base_predictor import BasePredictor


class LGBMPredictor(BasePredictor):
    def __init__(self):
        self.model = lgb.Booster(model_file="predictor/lightgbm_asl_model.txt")
        self.encoder = joblib.load("predictor/label_encoder.pkl")

    def predict(self, features):
        if features is None:
            return None, 0.0

        X = np.array(features).reshape(1, -1)
        probs = self.model.predict(X)[0]

        idx = probs.argmax()
        return self.encoder.inverse_transform([idx])[0], float(probs[idx])
