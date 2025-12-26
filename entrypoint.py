import sys
from datetime import datetime
from core.engine import GuardianEngine
from core.notifier import Notifier
from core.data_manager import DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst
from modules.guardians.defense import DefenseManager

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # 1. 多維度風險掃描 (新聞 + VIX)
    news_level, events = NewsScanner().scan()
    vix_level = VixScanner().check_vix()
    final_risk = max(news_level, vix_level)
    
    # 2. 更新系統狀態
    if final_risk != engine.state['risk_level']:
        engine.set_risk(final_risk, pause_hours=24 if final_risk >= 4 else 0)
        notifier.send(f"🛡️ 系統分級更新: L{final_risk}", f"原因: 偵測到關鍵事件或 VIX 波動", color=0xe67e22)

    # 3. 根據狀態執行任務
    if engine.is_paused():
        # L4: 執行防禦性回報
        DefenseManager().run_defense_report()
    else:
        # L1-L3: 執行 AI 分析
        hour = datetime.utcnow().hour
        market = "TW" if hour == 23 else "US" # 依照時間決定市場
        symbols = ["2330.TW", "TSLA", "NVDA"] # 範例清單
        
        analyst = MarketAnalyst(market)
        for s in symbols:
            res = analyst.analyze(s)
            if res and engine.can_attack():
                DataManager.save_csv(f"data/history/{market.lower()}_history.csv", [res])
                notifier.send(f"📈 {market} AI 預測點擊", f"{s} 現價: {res['price']}, 預期: {res['pred']:.2%}")

if __name__ == "__main__":
    main()
