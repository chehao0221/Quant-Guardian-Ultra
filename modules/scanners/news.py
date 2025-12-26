import feedparser
import time

class NewsScanner:
    def __init__(self):
        self.keywords = {"crash": 4, "war": 4, "inflation": 3, "fed": 2}

    def scan(self):
        # 範例使用 RSS
        feed = feedparser.parse("https://news.google.com/rss/search?q=finance+market&hl=en-US")
        max_level = 1
        found_events = []
        
        for entry in feed.entries[:10]:
            title = entry.title.lower()
            for kw, lv in self.keywords.items():
                if kw in title:
                    max_level = max(max_level, lv)
                    found_events.append(entry.title)
        return max_level, found_events
