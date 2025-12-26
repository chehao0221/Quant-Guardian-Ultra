import os
from core import Notifier

def main():
    notifier = Notifier()
    print("🚀 開始執行全頻道連線測試...")
    
    # 1. 測試黑天鵝頻道 (紅色)
    notifier.send("swan", "🧪 系統測試：黑天鵝頻道", "連線成功！當未來偵測到重大風險時，會在此發送緊急通報。", color=0xff0000)
    
    # 2. 測試一般消息頻道 (灰色)
    notifier.send("news", "🧪 系統測試：消息頻道", "連線成功！每日早、午、晚的盤前/盤中焦點會在此發送。", color=0x95a5a6)
    
    # 3. 測試台股頻道 (綠色)
    notifier.send("tw", "🧪 系統測試：台股頻道", "連線成功！台股盤後 AI 分析報告會在此發送。", color=0x2ecc71)
    
    # 4. 測試美股頻道 (藍色)
    notifier.send("us", "🧪 系統測試：美股頻道", "連線成功！美股盤後 AI 分析報告會在此發送。", color=0x3498db)

    print("✅ 測試指令已發出，請檢查 Discord！")

if __name__ == "__main__":
    main()
