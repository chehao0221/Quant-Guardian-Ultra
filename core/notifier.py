import requests
import os

class Notifier:
    def __init__(self, url=None):
        self.url = url or os.getenv("DISCORD_WEBHOOK_URL")

    def send_embed(self, title, description, color=0x2ECC71, fields=None):
        if not self.url: return
        payload = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "fields": fields or [],
                "footer": {"text": "Quant-Guardian-Ultra System"}
            }]
        }
        requests.post(self.url, json=payload, timeout=10)

    def send_text(self, content):
        if not self.url: return
        requests.post(self.url, json={"content": content}, timeout=10)
