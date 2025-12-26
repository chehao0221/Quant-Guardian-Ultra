import requests
import os

class Notifier:
    def __init__(self):
        # 讀取 4 個不同的 Webhook 網址
        self.webhooks = {
            "tw": os.getenv("DISCORD_TW_STOCK"),
            "us": os.getenv("DISCORD_US_STOCK"),
            "swan": os.getenv("DISCORD_BLACK_SWAN"),
            "news": os.getenv("DISCORD_GENERAL_NEWS")
        }

    def send(self, channel_type, title, msg, color=0x3498db):
        url = self.webhooks.get(channel_type)
        if not url:
            print(f"⚠️ 找不到 {channel_type} 的 Webhook 設定")
            return

        payload = {
            "embeds": [{
                "title": title,
                "description": msg,
                "color": color,
                "footer": {"text": "Quant-Guardian-Ultra"}
            }]
        }
        requests.post(url, json=payload)
