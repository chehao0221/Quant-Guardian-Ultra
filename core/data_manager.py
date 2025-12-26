import os, pandas as pd

class DataManager:
    @staticmethod
    def save_history(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(path, index=False, mode='a', header=not os.path.exists(path))
