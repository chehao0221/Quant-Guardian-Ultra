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
    current_hour = now_tw.hour
    current_minute = now_tw.minute

    # --- 1. 消息與黑天鵝監控 (保證不重複) ---
    news_lv, news_list = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    
    if news_list:
        current_news_content = "".join(news_list)
        current_hash = hashlib.md5(current_news_content.encode()).hexdigest()
        
        # A. 黑天鵝：隨時偵測，只要有新危險就發 (紅色)
        if max(news_lv, vix_lv) >= 4 and state.get("last_swan_hash") != current_hash:
            engine.set_risk(4, pause_hours=24)
            notifier.send("swan", "🚨 黑天鵝緊急警報", f"新風險偵測：\n{news_list[0]}", color=0xff0000)
            state["last_swan_hash"] = current_hash
            
        # B. 一般消息：盤前 (08:00 / 20:00) 且內容更新時才發 (灰色)
        elif (current_hour in [8, 20]) and state.get("last_news_hash") != current_hash:
            summary = "\n".join([f"• {t}" for t in news_list[:5]])
            time_tag = "台股" if current_hour == 8 else "美股"
            notifier.send("news", f"📰 {time_tag}盤前焦點掃描", f"開盤前關鍵動態：\n{summary}", color=0x95a5a6)
            state["last_news_hash"] = current_hash
            
        DataManager.save_json("data/system/state.json", state)

    # --- 2. 盤後個股 AI 分析 (僅在特定盤後時間發送) ---
    if not engine.is_paused():
        # C. 台股盤後 (14:30)
        if current_hour == 14:
            tw_analyst = MarketAnalyst("TW")
            for s in ["2330.TW", "2317.TW", "2454.TW"]:
                res = tw_analyst.analyze(s)
                if res:
                    notifier.send("tw", f"📈 台股盤後 AI 報告", f"股票: {res['symbol']}\n結算價: {res['price']}\n預測下週: {res['pred']:.2%}", color=0x2ecc71)

        # D. 美股盤後 (06:00)
        if current_hour == 6:
            us_analyst = MarketAnalyst("US")
            for s in ["NVDA", "TSLA", "AAPL"]:
                res = us_analyst.analyze(s)
                if res:
                    notifier.send("us", f"🇺🇸 美股盤後 AI 報告", f"股票: {res['symbol']}\n結算價: {res['price']}\n預測下週: {res['pred']:.2%}", color=0x3498db)

if __name__ == "__main__":
    main()
