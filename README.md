Quant-Guardian-Ultra/
│
├─ .github/workflows/
│  └─ main_pipeline.yml       # 核心自動化排程
│
├─ core/                      # 核心邏輯庫 (封裝成模組)
│  ├─ __init__.py
│  ├─ engine.py               # 狀態管理與 L1-L4 分級控制器
│  ├─ model.py                # XGBoost 模型封裝 (支援存取)
│  ├─ data_manager.py         # 負責所有 CSV/JSON 的讀寫與備份
│  └─ notifier.py             # 統一的 Discord Webhook 發送器
│
├─ modules/                   # 功能擴充模組
│  ├─ scanners/               # 數據掃描 (新聞、股價、VIX)
│  ├─ analysts/               # AI 預測邏輯 (台股、美股)
│  └─ guardians/              # 風控邏輯 (Counterfactual, Defense)
│
├─ data/                      # 數據存放
│  ├─ history/                # 交易與預測歷史
│  ├─ models/                 # 訓練好的模型檔 (.json)
│  └─ system/                 # 系統狀態 (state.json, .flag)
│
├─ entrypoint.py              # 統一的腳本入口
├─ requirements.txt
└─ README.md
