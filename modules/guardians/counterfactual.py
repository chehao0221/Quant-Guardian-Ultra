import yfinance as yf
from datetime import datetime, timedelta

class CounterfactualEngine:
    def __init__(self):
        pass

    def run_simulation(self, symbols):
        """模擬 L4 期間若繼續執行的績效"""
        results = []
        for s in symbols:
            data = yf.download(s, period="5d", progress=False)
            if not data.empty:
                perf = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1
                results.append({"symbol": s, "sim_ret": perf})
        return results
