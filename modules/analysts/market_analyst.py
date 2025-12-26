from .base_analyst import BaseAnalyst

class MarketAnalyst(BaseAnalyst):
    def __init__(self, market):
        super().__init__(market)

    def analyze(self, symbol):
        # 調用父類別 BaseAnalyst 的 predict 方法
        return self.predict(symbol)
