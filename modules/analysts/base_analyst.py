import yfinance as yf
import pandas as pd
from xgboost import XGBRegressor

class BaseAnalyst:
    def __init__(self, market_name):
        self.market_name = market_name

    def calculate_indicators(self, df):
        df = df.copy()
        # 選股邏輯 1: 報酬率特徵
        df['ret'] = df['Close'].pct_change()
        # 選股邏輯 2: 均線乖離率 (判斷是否過熱)
        df['ma20_gap'] = (df['Close'] - df['Close'].rolling(20).mean()) / df['Close'].rolling(20).mean()
        # 選股邏輯 3: 量能比 (判斷是否有主力介入)
        df['vol_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
        # 預測目標：5日後報酬
        df['target'] = df['Close'].shift(-5) / df['Close'] - 1
        return df.dropna()

    def predict(self, symbol):
        try:
            data = yf.download(symbol, period="2y", progress=False)
            if len(data) < 40: return None
            
            df = self.calculate_indicators(data)
            feats = ['ret', 'ma20_gap', 'vol_ratio']
            
            # 訓練 XGBoost 模型
            train = df.iloc[:-5]
            model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.05)
            model.fit(train[feats], train['target'])
            
            # 獲取最新數據進行預測
            last_feat = df[feats].iloc[-1:]
            pred_ret = float(model.predict(last_feat)[0])
            
            return {
                "symbol": symbol,
                "price": round(float(data['Close'].iloc[-1]), 2),
                "pred": pred_ret
            }
        except:
            return None
