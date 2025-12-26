import os
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # --- 1. 黑天鵝消息 (獨立發送) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    current_risk = max(news_lv, vix_lv)

    if current_risk >= 4:
        engine.set_risk(4, pause_hours=24)
        notifier.send(
            "🚨 【黑天鵝緊急通報】", 
            f"**關鍵消息：** {news_list[0] if news_list else '市場波動率(VIX)爆表'}\n**系統動作：** 已強制切換至 L4 防禦模式，停止所有進攻分析。",
            color=0xff0000 # 純紅色
        )
    elif current_risk == 3:
        notifier.send("⚠️ 【市場預警】", "偵測到異常波動，目前風險等級 L3，請留意部位。", color=0xf1c40f)

    # 如果目前是暫停狀態，就不執行後續的股票分析
    if engine.is_paused():
        return

    # --- 2. 台股 AI 分析 (獨立發送) ---
    tw_analyst = MarketAnalyst("TW")
    tw_targets = ["2330.TW", "2317.TW", "2454.TW"]
    
    for s in tw_targets:
        res = tw_analyst.analyze(s)
        if res:
            DataManager.save_history("data/history/tw_history.csv", [res])
            notifier.send(
                f"📈 【台股 AI 進攻報告】 - {res['symbol']}", 
                f"**目前價格：** {res['price']}\n**AI 預測報酬：** {res['pred']:.2%}\n**信心等級：** 穩定",
                color=0x2ecc71 # 綠色
            )

    # --- 3. 美股 AI 分析 (獨立發送) ---
    us_analyst = MarketAnalyst("US")
    us_targets = ["NVDA", "TSLA", "AAPL"]
    
    for s in us_targets:
        res = us_analyst.analyze(s)
        if res:
            DataManager.save_history("data/history/us_history.csv", [res])
            notifier.send(
                f"🇺🇸 【美股 AI 進攻報告】 - {res['symbol']}", 
                f"**目前價格：** {res['price']}\n**AI 預測報酬：** {res['pred']:.2%}\n**信心等級：** 穩定",
                color=0x3498db # 藍色
            )

if __name__ == "__main__":
    main()
