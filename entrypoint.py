import os, sys
from core import GuardianEngine, Notifier, DataManager
from modules.scanners.news import NewsScanner
from modules.analysts.market_analyst import MarketAnalyst
from modules.guardians.defense import DefenseManager

def main():
    engine = GuardianEngine()
    notifier = Notifier()

    # 1. 檢查風險
    risk = NewsScanner().scan()
    if risk >= 4: engine.set_risk(4, pause_hours=24)

    # 2. 決定行動
    if engine.is_paused():
        notifier.send("🛡️ 防禦模式", "暫停個股分析", color=0xff0000)
        safe_data = DefenseManager().get_safe_assets()
        DataManager.save_history("data/history/defense.csv", [safe_data])
    else:
        # 執行分析
        analyst = MarketAnalyst("TW")
        res = analyst.analyze("2330.TW")
        if res:
            DataManager.save_history("data/history/tw_history.csv", [res])
            notifier.send("📈 AI 分析完成", f"標的: {res['symbol']} 預測: {res['pred']:.2%}")

if __name__ == "__main__":
    main()
