import yfinance as yf

class DefenseManager:
    def get_safe_assets(self):
        assets = ["GLD", "BIL", "VIXY"]
        data = yf.download(assets, period="1d", progress=False)['Close']
        return data.iloc[-1].to_dict()
