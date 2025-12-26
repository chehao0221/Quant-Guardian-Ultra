from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # --- 1. 黑天鵝 & 一般消息掃描 ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    
    # 分流 A：黑天鵝警報 (獨立頻道 / 紅色)
    if max(news_lv, vix_lv) >= 4:
        engine.set_risk(4, pause_hours=24)
        notifier.send("swan", "🚨 黑天鵝緊急警報", f"偵測到極高風險事件：\n{news_list[0] if news_list else 'VIX 異常'}", color=0xff0000)
    
    # 分流 B：一般消息 (獨立頻道 / 灰色)
    if news_list:
        summary = "\n".join([f"• {t}" for t in news_list[:3]])
        notifier.send("news", "📰 今日市場焦點", f"掃描到以下重要新聞：\n{summary}", color=0x95a5a6)

    if engine.is_paused(): return

    # --- 2. 台股分析 (獨立頻道 / 綠色) ---
    tw_analyst = MarketAnalyst("TW")
    for s in ["2330.TW", "2317.TW"]:
        res = tw_analyst.analyze(s)
        if res:
            notifier.send("tw", f"📈 台股報告 - {res['symbol']}", f"目前價格: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x2ecc71)

    # --- 3. 美股分析 (獨立頻道 / 藍色) ---
    us_analyst = MarketAnalyst("US")
    for s in ["NVDA", "TSLA"]:
        res = us_analyst.analyze(s)
        if res:
            notifier.send("us", f"🇺🇸 美股報告 - {res['symbol']}", f"目前價格: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x3498db)

if __name__ == "__main__":
    main()
