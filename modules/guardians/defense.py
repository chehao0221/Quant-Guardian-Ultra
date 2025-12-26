import yfinance as yf
from core.notifier import Notifier

class DefenseManager:
    def __init__(self):
        self.notifier = Notifier()
        self.hedge_assets = {
            "BIL": "短債 (Cash)",
            "GLD": "黃金 (Gold)",
            "VIXY": "波動率 (VIX)"
        }

    def run_defense_report(self):
        data = yf.download(list(self.hedge_assets.keys()), period="5d", progress=False)["Close"]
        returns = (data.iloc[-1] / data.iloc[0] - 1)
        
        fields = []
        for ticker, name in self.hedge_assets.items():
            ret = returns[ticker]
            fields.append({
                "name": f"{name} ({ticker})",
                "value": f"週漲跌: `{ret:+.2%}`",
                "inline": True
            })
        
        self.notifier.send("🛡️ 防禦模式資產監控", "當前市場風險較高，建議關注避險資產走勢。", color=0xf1c40f, fields=fields)
