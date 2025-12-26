import os
import pandas as pd
import json

class DataManager:
    @staticmethod
    def save_csv(path, data, mode='a'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df = pd.DataFrame(data)
        header = not os.path.exists(path) or mode == 'w'
        df.to_csv(path, index=False, mode=mode, header=header)

    @staticmethod
    def load_json(path, default=None):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default or {}

    @staticmethod
    def save_json(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
