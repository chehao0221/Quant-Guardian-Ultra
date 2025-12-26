import os
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # --- 第一部分：風險監控 (黑天鵝消息) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    current_risk = max(news_lv, vix_lv)

    # 如果偵測到高風險，立刻發送一則獨立的「黑天鵝警告」
    if current_risk >= 4:
        engine.set_risk(4, pause_hours=24)
        notifier.send(
            "🚨 偵測到黑天鵝風險事件", 
            f"**風險來源：** {news_list[0] if news_list else 'VIX 指數異常'}\n**系統狀態：** 進入 L4 防禦模式，暫停進攻 24 小時。",
            color=0xff0000  # 紅色
        )
    elif current_risk == 3:
        notifier.send("⚠️ 市場警戒通知", "市場波動率 (VIX) 提升至 L3 等級，請注意倉位。", color=0xf1c40f)

    # --- 第二部分：股票 AI 分析報告 (分開處理) ---
    # 只有在沒有 L4 暫停的情況下，才執行並發送股票報告
    if not engine.is_paused():
        analyst = MarketAnalyst("TW")
        targets = ["2330.TW", "2317.TW", "2454.TW"]
        
        for symbol in targets:
            res = analyst.analyze(symbol) # 這裡是呼叫你的分析邏輯
            if res:
                DataManager.save_history("data/history/tw_history.csv", [res])
                # 每支股票發送一個獨立的 Embed，或者一個匯總 Embed
                notifier.send(
                    f"📈 AI 進攻報告 - {res['symbol']}", 
                    f"**目前價格：** {res['price']}\n**預測報酬：** {res['pred']:.2%}\n**風險等級：** L{current_risk}",
                    color=0x2ecc71  # 綠色
                )

if __name__ == "__main__":
    main()
