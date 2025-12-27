import feedparser
import hashlib
from core.data_manager import DataManager

class NewsScanner:
    def __init__(self):
        self.data_manager = DataManager()

    def scan(self):
        feed = feedparser.parse(
            "https://news.google.com/rss/search?q=股市+崩盤+戰爭+黑天鵝&hl=zh-TW&gl=TW"
        )

        state = self.data_manager.load_state()

        # 相容舊結構
        news_seen = state.get("news_seen", [])
        if not isinstance(news_seen, list):
            news_seen = []

        level = 1
        news_titles = []

        keywords = ["崩盤", "戰爭", "暴跌", "黑天鵝", "斷頭", "大跌"]

        for entry in feed.entries[:8]:
            if not any(kw in entry.title for kw in keywords):
                continue

            # === 新聞 hash（標題即可）===
            news_hash = hashlib.md5(entry.title.encode("utf-8")).hexdigest()

            # 已播過 → 跳過
            if news_hash in news_seen:
                continue

            # 新聞是新的
            level = 4
            news_titles.append(entry.title)

            news_seen.append(news_hash)

        # 限制 cache 長度（防無限成長）
        news_seen = news_seen[-50:]

        state["news_seen"] = news_seen
        self.data_manager.save_state(state)

        return level, news_titles
