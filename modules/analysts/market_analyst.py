import yfinance as yf
from core.model import QuantModel

class MarketAnalyst:
    def __init__(self, market_type): # 'TW' or 'US'
        self.market = market_type
        self.model = QuantModel(f"{market_type}_main")

    def analyze(self, symbol):
        df = yf.download(symbol, period="2y", progress=False)
        if df.empty: return None
        
        # 特徵工程 (簡化版)
        df['ret'] = df['Close'].pct_change()
        X = df[['ret']].tail(1) 
        
        if not self.model.load():
            # 若無模型則現場訓練 (Demo 用)
            train_df = df.dropna()
            self.model.train(train_df[['ret']].shift(1).dropna(), train_df['ret'].dropna())
        
        pred = self.model.predict(X)[0]
        return {"symbol": symbol, "price": df['Close'].iloc[-1], "pred": pred}
