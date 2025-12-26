import hashlib
import os
from datetime import datetime
import pytz
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    state = DataManager.load_json("data/system/state.json")
    
    # 設定台灣時區
    tw_tz = pytz.timezone('Asia/Taipei')
    now_tw = datetime.now(tw_tz)
    h = now_tw.hour

    # --- 1. 消息與黑天鵝處理 (08, 14, 20, 06 四個時段均監控) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    
    if news_list:
        current_news_content = "".join(news_list)
        current_hash = hashlib.md5(current_news_content.encode()).hexdigest()
        
        # 內容有變動才執行發送邏輯
        if state.get("last_news_hash") != current_hash:
            # A. 黑天鵝警報 (任何時段偵測到 L4 均發送)
            if max(news_lv, vix_lv) >= 4:
                engine.set_risk(4, pause_hours=8)
                notifier.send("swan", "🚨 黑天鵝風險通報", f"新風險偵測：\n{news_list[0]}", color=0xff0000)
            
            # B. 一般消息 (限定 08, 14, 20 三個時段發送，滿足一天三次)
            elif h in [8, 14, 20]:
                time_labels = {8: "台股盤前", 14: "午後焦點", 20: "美股盤前"}
                label = time_labels.get(h, "即時")
                summary = "\n".join([f"• {t}" for t in news_list[:5]])
                notifier.send("news", f"📰 {label}市場掃描", f"關鍵動態摘要：\n{summary}", color=0x95a5a6)
            
            # 更新 Hash 避免重複
            state["last_news_hash"] = current_hash
            DataManager.save_json("data/system/state.json", state)

    # --- 2. 盤後 AI 分析報告 ---
    if not engine.is_paused():
        # C. 台股盤後報告 (14:00 執行時段，對應 14:30 數據)
        if h == 14:
            tw_analyst = MarketAnalyst("TW")
            for s in ["2330.TW", "2317.TW"]:
                res = tw_analyst.analyze(s)
                if res:
                    notifier.send("tw", f"📈 台股盤後報告: {res['symbol']}", f"結算價: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x2ecc71)

        # D. 美股盤後報告 (06:00 執行時段)
        if h == 6:
            us_analyst = MarketAnalyst("US")
            for s in ["NVDA", "TSLA"]:
                res = us_analyst.analyze(s)
                if res:
                    notifier.send("us", f"🇺🇸 美股盤後報告: {res['symbol']}", f"結算價: {res['price']}\n預測報酬: {res['pred']:.2%}", color=0x3498db)

if __name__ == "__main__":
    main()
