import yfinance as yf

class VixScanner:
    def check_vix(self):
        vix = yf.download("^VIX", period="1d", progress=False)
        if vix.empty: return 1
        current_vix = vix['Close'].iloc[-1]
        
        if current_vix > 35: return 4  # 極端恐慌
        if current_vix > 25: return 3  # 高度警戒
        if current_vix > 20: return 2  # 中度波動
        return 1
