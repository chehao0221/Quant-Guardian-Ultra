import feedparser

class NewsScanner:
    def scan(self):
        # 抓取 Google RSS
        feed = feedparser.parse("https://news.google.com/rss/search?q=股市+崩盤+戰爭+黑天鵝&hl=zh-TW&gl=TW")
        level = 1
        news_titles = []
        
        # 關鍵字清單
        keywords = ["崩盤", "戰爭", "暴跌", "黑天鵝", "斷頭", "大跌"]
        
        for entry in feed.entries[:8]:
            if any(kw in entry.title for kw in keywords):
                level = 4
                news_titles.append(entry.title)
        
        return level, news_titles
