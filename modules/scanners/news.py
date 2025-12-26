import feedparser

class NewsScanner:
    def scan(self):
        feed = feedparser.parse("https://news.google.com/rss/search?q=股市+崩盤+戰爭&hl=zh-TW")
        level = 1
        news_titles = []
        for entry in feed.entries[:5]:
            if any(kw in entry.title for kw in ["崩盤", "戰爭", "暴跌"]): 
                level = 4
                news_titles.append(entry.title)
        return level, news_titles # 這裡要回傳兩個值
