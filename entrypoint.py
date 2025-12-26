import os
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # --- 1. 黑天鵝消息 (獨立發送 / 紅色) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    current_risk = max(news_lv, vix_lv)

    if current_risk >= 4:
        engine.set_risk(4, pause_hours=24)
        notifier.send(
            "🚨 【緊急：黑天鵝事件警報】", 
            f"**風險來源：** {news_list[0] if news_list else 'VIX 指數異常飆升'}\n**系統動作：** 啟動 L4 防禦機制，未來 24 小時停止交易預測。",
            color=0xff0000 # 紅色
        )
    elif current_risk == 3:
        notifier.send("⚠️ 【市場預警：L3 警戒】", "市場波動加大，請注意部位回撤風險。", color=0xf1c40f) # 橘色

    # 若系統處於暫停狀態，則不執行後續分析
    if engine.is_paused():
        return

    # --- 2. 台股 AI 分析報告 (獨立發送 / 綠色) ---
    tw_analyst = MarketAnalyst("TW")
    tw_targets = ["2330.TW", "2317.TW", "2454.TW", "2382.TW", "2308.TW"]
    
    for s in tw_targets:
        res = tw_analyst.analyze(s)
        if res:
            DataManager.save_history("data/history/tw_history.csv", [res])
            notifier.send(
                f"📈 【台股 AI 選股報告】 - {res['symbol']}", 
                f"**目前價格：** {res['price']}\n**預測 5 日報酬：** {res['pred']:.2%}\n**風險評級：** L{current_risk}",
                color=0x2ecc71 # 綠色
            )

    # --- 3. 美股 AI 分析報告 (獨立發送 / 藍色) ---
    us_analyst = MarketAnalyst("US")
    us_targets = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL"]
    
    for s in us_targets:
        res = us_analyst.analyze(s)
        if res:
            DataManager.save_history("data/history/us_history.csv", [res])
            notifier.send(
                f"🇺🇸 【美股 AI 選股報告】 - {res['symbol']}", 
                f"**目前價格：** {res['price']}\n**預測 5 日報酬：** {res['pred']:.2%}\n**風險評級：** L{current_risk}",
                color=0x3498db # 藍色
            )

if __name__ == "__main__":
    main()
