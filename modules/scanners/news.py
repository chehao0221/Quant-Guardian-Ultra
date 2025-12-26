import feedparser

class NewsScanner:
    def scan(self):
        # 抓取 Google 新聞
        feed = feedparser.parse("https://news.google.com/rss/search?q=股市+崩盤+戰爭+黑天鵝&hl=zh-TW&gl=TW")
        level = 1
        news_titles = []
        
        # 檢查前 5 則新聞
        for entry in feed.entries[:5]:
            if any(kw in entry.title for kw in ["崩盤", "戰爭", "暴跌", "黑天鵝", "斷頭"]): 
                level = 4
                news_titles.append(entry.title)
        
        # 必須回傳兩個值，對接 entrypoint.py
        return level, news_titles
