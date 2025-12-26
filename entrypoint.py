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

    # 如果有黑天鵝，發送獨立的「紅色」警報
    if current_risk >= 4:
        engine.set_risk(4, pause_hours=24)
        notifier.send(
            "🚨 偵測到黑天鵝風險事件", 
            f"**風險來源：** {news_list[0] if news_list else '市場波動率異常'}\n**系統狀態：** 啟動 L4 防禦，暫停分析 24 小時。",
            color=0xff0000  # 紅色
        )
    elif current_risk == 3:
        notifier.send("⚠️ 市場警戒通知", "VIX 指數進入 L3 等級，請注意回測風險。", color=0xf1c40f)

    # --- 第二部分：股票 AI 分析報告 (分開處理) ---
    # 只有在沒被停火 (L4) 的情況下才發送
    if not engine.is_paused():
        analyst = MarketAnalyst("TW")
        targets = ["2330.TW", "2317.TW", "2454.TW"]
        
        for symbol in targets:
            res = analyst.analyze(symbol)
            if res:
                # 存檔至 CSV
                DataManager.save_history("data/history/tw_history.csv", [res])
                # 發送獨立的「綠色」股票報告
                notifier.send(
                    f"📈 AI 進攻報告 - {res['symbol']}", 
                    f"**目前價格：** {res['price']}\n**預測報酬：** {res['pred_ret']:.2%}\n**風險等級：** L{current_risk}",
                    color=0x2ecc71  # 綠色
                )

if __name__ == "__main__":
    main()
