import requests
import os

class Notifier:
    def __init__(self):
        self.webhooks = {
            "tw": os.getenv("DISCORD_TW_STOCK"),
            "us": os.getenv("DISCORD_US_STOCK"),
            "swan": os.getenv("DISCORD_BLACK_SWAN"),
            "news": os.getenv("DISCORD_GENERAL_NEWS")
        }

    def send(self, channel_type, title, msg, color=0x3498db):
        url = self.webhooks.get(channel_type)
        if not url: return
        
        payload = {
            "embeds": [{
                "title": title,
                "description": msg,
                "color": color,
                "footer": {"text": "Quant-Guardian-Ultra | 盤後精準模式"}
            }]
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"發送失敗: {e}")
