import yfinance as yf
from core.model import QuantModel

class MarketAnalyst:
    def __init__(self, market):
        self.market = market
        self.model = QuantModel(f"{market}_model")

    def analyze(self, symbol):
        df = yf.download(symbol, period="1y", progress=False)
        if df.empty: return None
        df['ret'] = df['Close'].pct_change()
        # 這裡簡化邏輯，實際可加入你原本的 XGBoost 訓練
        return {"symbol": symbol, "price": df['Close'].iloc[-1], "pred": 0.02}
