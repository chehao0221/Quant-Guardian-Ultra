import os
import sys
from datetime import datetime
from core.engine import GuardianEngine
from core.notifier import Notifier
from modules.analysts.base_analyst import BaseAnalyst

def main():
    engine = GuardianEngine()
    notifier = Notifier()
    
    # 獲取當前小時 (UTC)
    hour = datetime.utcnow().hour
    
    # 1. 檢查 L4 狀態
    if engine.is_paused():
        notifier.send_embed("🛡️ 系統防禦中", "目前處於 L4 黑天鵝冷卻期，跳過進攻分析。", color=0xE74C3C)
        sys.exit(0)

    # 2. 執行分析 (範例：台股)
    if hour == 23: # 對應台灣時間早上 07:00
        notifier.send_text("🚀 開始台股盤前掃描...")
        analyst = BaseAnalyst(["2330.TW", "2317.TW", "2454.TW"], name="TW")
        results = analyst.run_inference()
        
        fields = []
        for s, r in results.items():
            fields.append({"name": s, "value": f"預測回報: `{r['pred']:+.2%}`\n現價: `{r['price']:.2f}`", "inline": True})
        
        notifier.send_embed("📊 台股 AI 分析報告", "根據近期數據之預測結果", fields=fields)

if __name__ == "__main__":
    main()
