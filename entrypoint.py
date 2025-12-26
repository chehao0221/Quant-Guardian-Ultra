import os
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.scanners.vix_scanner import VixScanner
from modules.analysts.market_analyst import MarketAnalyst
from modules.guardians.defense import DefenseManager
from modules.guardians.counterfactual import CounterfactualEngine

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # 1. 環境掃描
    news_lv = NewsScanner().scan()
    vix_lv = VixScanner().check_vix()
    current_risk = max(news_lv, vix_lv)

    # 2. 狀態管理
    if current_risk >= 4 and not engine.state['l4_active']:
        engine.set_risk(4, pause_hours=24)
        notifier.send("🚨 L4 Risk Detected", "Entering defense mode for 24h.", color=0xff0000)

    # 3. 執行邏輯
    if engine.is_paused():
        # L4 防禦邏輯
        notifier.send("🛡️ Defense Mode", "Executing Counterfactual Analysis...", color=0x34495e)
        cf_res = CounterfactualEngine().run_simulation(["2330.TW", "NVDA"])
        DataManager.save_history("data/history/counterfactual.csv", cf_res)
    else:
        # 正常進攻邏輯
        analyst = MarketAnalyst("TW")
        res = analyst.predict("2330.TW")
        if res and engine.can_attack():
            DataManager.save_history("data/history/tw_history.csv", [res])
            notifier.send("📊 AI Report", f"{res['symbol']}: Pred Ret {res['pred_ret']:.2%}")

if __name__ == "__main__":
    main()
