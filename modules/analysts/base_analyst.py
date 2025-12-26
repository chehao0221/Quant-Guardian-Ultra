import yfinance as yf
import pandas as pd
from xgboost import XGBRegressor

class BaseAnalyst:
    def __init__(self, symbols, name="Base"):
        self.symbols = symbols
        self.name = name

    def get_features(self, df):
        df = df.copy()
        df["returns"] = df["Close"].pct_change()
        df["vol_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()
        df["ma_gap"] = (df["Close"] - df["Close"].rolling(20).mean()) / df["Close"].rolling(20).mean()
        df["target"] = df["Close"].shift(-5) / df["Close"] - 1
        return df.dropna()

    def run_inference(self):
        results = {}
        for s in self.symbols:
            try:
                data = yf.download(s, period="2y", progress=False)
                df = self.get_features(data)
                
                feats = ["returns", "vol_ratio", "ma_gap"]
                train = df.iloc[:-5]
                
                model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.05)
                model.fit(train[feats], train["target"])
                
                pred = float(model.predict(df[feats].iloc[-1:])[0])
                results[s] = {"pred": pred, "price": data["Close"].iloc[-1]}
            except Exception as e:
                print(f"Error analyzing {s}: {e}")
        return results
