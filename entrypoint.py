from core.engine import GuardianEngine
from core.notifier import Notifier
from modules.scanners.news import NewsScanner
from modules.analysts.market_analyst import MarketAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    scanner = NewsScanner()

    # 1. 掃描風險
    risk_level, events = scanner.scan()
    if risk_level > engine.state['risk_level']:
        engine.set_risk(risk_level, pause_hours=24 if risk_level==4 else 0)
        notifier.send("⚠️ 風險等級提升", f"偵測到關鍵事件，系統升級至 L{risk_level}", color=0xe74c3c)

    # 2. 執行進攻 (判斷是否處於 L4 暫停)
    if not engine.is_paused():
        tw_analyst = MarketAnalyst("TW")
        res = tw_analyst.analyze("2330.TW")
        notifier.send("📊 AI 預測報告", f"TSMC 預期回報: {res['pred']:.2%}", color=0x2ecc71)
    else:
        notifier.send("🛡️ 防禦模式", "L4 狀態中，暫停 AI 預測寫入", color=0x95a5a6)

if __name__ == "__main__":
    main()
