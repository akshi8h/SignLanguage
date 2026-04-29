from collections import Counter
from xgb_predictor import XGBPredictor
from rf_predictor import RFPredictor
from lgbm_predictor import LGBMPredictor
from catboost_predictor import CatBoostPredictor

class PredictorManager:
    def __init__(self):
        # ✅ Bagging setup
        self.models = [
            XGBPredictor(),
            RFPredictor(),
            LGBMPredictor(),
            CatBoostPredictor()
        ]

    def predict(self, features):from collections import Counter
from xgb_predictor import XGBPredictor
from rf_predictor import RFPredictor
from lgbm_predictor import LGBMPredictor
from catboost_predictor import CatBoostPredictor

class PredictorManager:
    def __init__(self):
        self.models = [
            XGBPredictor(),
            RFPredictor(),
            LGBMPredictor(),
            CatBoostPredictor()
        ]

        print("✅ PredictorManager initialized with models:")
        for m in self.models:
            print(" -", m.__class__.__name__)

    def predict(self, features):
        votes = []
        confidences = []

        for model in self.models:
            label, conf = model.predict(features)

            if label:
                votes.append(label)
                confidences.append(conf)

                # 🔍 DEBUG LINE
                print(f"[{model.__class__.__name__}] → {label} ({conf:.2f})")

        if not votes:
            return None, 0.0

        final_label = Counter(votes).most_common(1)[0][0]
        avg_conf = sum(confidences) / len(confidences)

        print(f"✅ FINAL VOTE → {final_label}\n")

        return final_label, avg_conf

        votes = []
        confidences = []

        for model in self.models:
            label, conf = model.predict(features)
            if label:
                votes.append(label)
                confidences.append(conf)

        if not votes:
            return None, 0.0

        # majority voting
        final_label = Counter(votes).most_common(1)[0][0]
        avg_conf = sum(confidences) / len(confidences)

        return final_label, avg_conf
