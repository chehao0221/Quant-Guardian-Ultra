from .base_analyst import BaseAnalyst

class MarketAnalyst(BaseAnalyst):
    def __init__(self, market):
        # 初始化父類別 (TW)
        super().__init__(market)

    def analyze(self, symbol):
        # 呼叫 BaseAnalyst 裡的 predict 邏輯
        return self.predict(symbol)
