import os
import sys
from datetime import datetime
from core.engine import GuardianEngine
from core.notifier import Notifier # 需自行建立 notifier.py 或整合
from modules.analysts.base_analyst import BaseAnalyst
from core.data_manager import DataManager

def run_market_task(market, symbols, engine, history_path):
    analyst = BaseAnalyst(market)
    results = []
    for s in symbols:
        res = analyst.predict(s)
        if res:
            res['date'] = datetime.now().strftime("%Y-%m-%d")
            results.append(res)
    
    # 判斷是否寫入歷史 (L3/L4 不寫入)
    if engine.can_attack():
        DataManager.append_history(history_path, results)
        print(f"✅ {market} Analysis saved to history.")
    else:
        print(f"🛡️ {market} Analysis finished (Defense Mode: No save).")

def main():
    engine = GuardianEngine()
    hour = datetime.utcnow().hour # GitHub Actions 為 UTC

    # 1. 執行新聞雷達 (假設你已將 news_radar 改為類別)
    # 這裡可以加入檢查新聞並 update engine.set_risk 的邏輯

    # 2. 判斷時段執行分析
    if hour == 23: # 台灣 07:00
        run_market_task("TW", ["2330.TW", "2317.TW"], engine, "data/history/tw_history.csv")
    
    if hour == 14: # 台灣 22:00 (美股)
        run_market_task("US", ["AAPL", "NVDA", "TSLA"], engine, "data/history/us_history.csv")

if __name__ == "__main__":
    main()
