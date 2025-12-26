import pandas as pd
import os

class DataManager:
    @staticmethod
    def append_history(file_path, data_list):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data_list)
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)

    @staticmethod
    def load_csv(file_path):
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        return pd.DataFrame()
