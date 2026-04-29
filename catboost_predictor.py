import numpy as np
from catboost import CatBoostClassifier
from base_predictor import BasePredictor

class CatBoostPredictor(BasePredictor):
    # ✅ Labels in the same order as used in training
    LABELS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["nothing", "space", "delete"]

    def __init__(self):
        self.model = CatBoostClassifier()
        self.model.load_model("predictor/catboost_asl_model.cbm")

    def predict(self, features):
        if features is None:
            return None, 0.0

        # Ensure features are in correct shape
        X = np.array(features).reshape(1, -1)

        # Get predicted probabilities
        probs = self.model.predict_proba(X)[0]

        # Pick the label with highest probability
        idx = probs.argmax()
        return self.LABELS[idx], float(probs[idx])
