import os
import xgboost as xgb
import pandas as pd

class QuantModel:
    def __init__(self, model_name, models_dir="data/models"):
        self.model_path = os.path.join(models_dir, f"{model_name}.json")
        os.makedirs(models_dir, exist_ok=True)
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.05)

    def train(self, X, y):
        self.model.fit(X, y)
        self.model.save_model(self.model_path)

    def load(self):
        if os.path.exists(self.model_path):
            self.model.load_model(self.model_path)
            return True
        return False

    def predict(self, X):
        return self.model.predict(X)
