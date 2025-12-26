import requests
import os

class Notifier:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send(self, title, message, color=0x3498db, fields=None):
        if not self.webhook_url: return
        payload = {
            "embeds": [{
                "title": title, "description": message,
                "color": color, "fields": fields or [],
                "footer": {"text": "Guardian Ultra System"}
            }]
        }
        requests.post(self.webhook_url, json=payload)
