import hashlib
from datetime import datetime
import pytz

from core import GuardianEngine, Notifier
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()

    tw_tz = pytz.timezone("Asia/Taipei")
    now = datetime.now(tw_tz)
    h = now.hour

    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()

    if news_list:
        content = "".join(news_list)
        news_hash = hashlib.md5(content.encode()).hexdigest()

        if engine.state.get("last_news_hash") != news_hash:
            if max(news_lv, vix_lv) >= 4:
                engine.set_risk(4, pause_hours=8)
                notifier.send(
                    "swan",
                    "🚨 黑天鵝風險警報",
                    news_list[0],
                    color=0xff0000
                )
            elif h in [8, 14, 20]:
                notifier.send(
                    "news",
                    "📰 市場焦點",
                    "\n".join(news_list[:5]),
                    color=0x95a5a6
                )

            engine.state["last_news_hash"] = news_hash
            engine.save_state()

    if not engine.is_paused():
        if h == 14:
            analyst = MarketAnalyst("TW")
            for s in ["2330.TW", "2317.TW", "2454.TW"]:
                res = analyst.analyze(s)
                if res:
                    notifier.send("tw", f"📈 {s}", f"{res['price']} / {res['pred']:.2%}")

        if h == 6:
            analyst = MarketAnalyst("US")
            for s in ["NVDA", "TSLA", "AAPL"]:
                res = analyst.analyze(s)
                if res:
                    notifier.send("us", f"🇺🇸 {s}", f"{res['price']} / {res['pred']:.2%}")

if __name__ == "__main__":
    main()
