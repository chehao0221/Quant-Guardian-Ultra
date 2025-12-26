import hashlib
import os
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    state = DataManager.load_json("data/system/state.json")
    
    # --- 1. 風險監控與消息去重 (保證不重複發送) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    
    if news_list:
        # 建立新聞指紋 (Hash)，若內容相同則不發送
        current_news_content = "".join(news_list)
        current_hash = hashlib.md5(current_news_content.encode()).hexdigest()
        
        if state.get("last_news_hash") != current_hash:
            # A. 黑天鵝頻道 (紅色)
            if max(news_lv, vix_lv) >= 4:
                engine.set_risk(4, pause_hours=24)
                notifier.send("swan", "🚨 黑天鵝緊急警報", f"新風險偵測：\n{news_list[0]}", color=0xff0000)
            
            # B. 一般消息頻道 (灰色)
            else:
                summary = "\n".join([f"• {t}" for t in news_list[:3]])
                notifier.send("news", "📰 市場焦點摘要", f"今日關鍵動態：\n{summary}", color=0x95a5a6)
            
            # 更新狀態並存檔
            state["last_news_hash"] = current_hash
            DataManager.save_json("data/system/state.json", state)

    # --- 2. 盤後個股 AI 分析 (分流發送) ---
    if not engine.is_paused():
        # C. 台股頻道 (綠色)
        tw_analyst = MarketAnalyst("TW")
        tw_targets = ["2330.TW", "2317.TW", "2454.TW"]
        for s in tw_targets:
            res = tw_analyst.analyze(s)
            if res:
                DataManager.save_history("data/history/tw_history.csv", [res])
                notifier.send("tw", f"📈 台股盤後報告 - {res['symbol']}", f"結算價格: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x2ecc71)

        # D. 美股頻道 (藍色)
        us_analyst = MarketAnalyst("US")
        us_targets = ["NVDA", "TSLA", "AAPL", "MSFT"]
        for s in us_targets:
            res = us_analyst.analyze(s)
            if res:
                DataManager.save_history("data/history/us_history.csv", [res])
                notifier.send("us", f"🇺🇸 美股盤後報告 - {res['symbol']}", f"結算價格: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x3498db)

if __name__ == "__main__":
    main()
