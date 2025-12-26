import json
import os
import csv

class DataManager:
    @staticmethod
    def load_json(path):
        """讀取 JSON 檔案，如果檔案不存在則返回空字典"""
        if not os.path.exists(path):
            # 如果目錄不存在，順便建立
            os.makedirs(os.path.dirname(path), exist_ok=True)
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    @staticmethod
    def save_json(path, data):
        """將字典儲存為 JSON 檔案"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def save_history(path, data_list):
        """將分析結果寫入 CSV 歷史紀錄"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_exists = os.path.exists(path)
        
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 如果是新檔案，寫入標頭
            if not file_exists:
                writer.writerow(['symbol', 'price', 'pred'])
            
            for item in data_list:
                writer.writerow([item['symbol'], item['price'], item['pred']])
