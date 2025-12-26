import requests, os

class Notifier:
    def __init__(self):
        self.url = os.getenv("DISCORD_WEBHOOK_URL")

    def send(self, title, msg, color=0x3498db, fields=None):
        if not self.url: return
        payload = {"embeds": [{"title": title, "description": msg, "color": color, "fields": fields or []}]}
        requests.post(self.url, json=payload)
