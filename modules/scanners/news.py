import feedparser

class NewsScanner:
    def scan(self):
        feed = feedparser.parse("https://news.google.com/rss/search?q=股市+崩盤+戰爭&hl=zh-TW")
        level = 1
        triggered_news = []
        for entry in feed.entries[:5]:
            if any(kw in entry.title for kw in ["崩盤", "戰爭", "暴跌", "黑天鵝"]): 
                level = 4
                triggered_news.append(entry.title)
        return level, triggered_news # 必須回傳兩個值
