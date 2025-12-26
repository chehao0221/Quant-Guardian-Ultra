# 🛡️ Quant-Guardian-Ultra | 量化守護者
> **基於 XGBoost AI 預測與 Discord 多頻道自動化分流的智能交易監控系統**

---

## 🚀 系統核心功能
本系統部署於 GitHub Actions 雲端環境，結合 **yfinance** 與 **Google News** 數據，實現全天候四個關鍵時段的自動化監控與預測。

### 📡 Discord 四路訊息分流
系統透過 Webhooks 將不同性質的資訊發送到獨立頻道，避免資訊過載：

* **🚨 黑天鵝頻道**：針對市場極端恐慌 (VIX > 35) 與災難性新聞提供紅色警戒。
* **📰 焦點消息頻道**：提供台/美股盤前焦點，具備內容 Hash 去重功能，保證不重複推播。
* **📈 台股分析頻道**：每日 14:30 推送台股重點個股 (2330, 2317...) 的 AI 盤後預測報告。
* **🇺🇸 美股分析頻道**：每日 06:00 推送美股重點個股 (NVDA, TSLA...) 的 AI 盤後收盤報告。

---

## ⏰ 自動化任務時間表 (台灣時間 UTC+8)
| 時間 | 任務內容 | 目標頻道 |
| :--- | :--- | :--- |
| **06:00** | 美股盤後 AI 分析報告 | 🇺🇸 US Stock |
| **08:00** | 台股盤前焦點掃描 + 風險監控 | 📰 News / 🚨 Swan |
| **14:30** | 台股盤後 AI 分析報告 + 午後焦點 | 📈 TW Stock / 📰 News |
| **20:00** | 美股盤前焦點掃描 + 風險監控 | 📰 News / 🚨 Swan |

---

## 🛠️ 技術棧與架構
- **開發語言**: Python 3.10
- **AI 模型**: XGBoost Classifier/Regressor
- **數據來源**: Yahoo Finance API, Google News RSS
- **自動化運算**: GitHub Actions (Ubuntu-latest)
- **通知中樞**: Discord Webhooks SDK

## 📁 資料夾結構說明
- `core/`: 系統核心邏輯 (Notifier, DataManager)
- `modules/`: 掃描器與分析模型模組
- `data/`: 存儲歷史紀錄 (CSV) 與系統狀態 (JSON)
- `entrypoint.py`: 系統排程執行主程式

---
**免責聲明：** 本系統之 AI 預測結果僅供參考，不構成投資建議。金融市場有風險，投資需謹慎。



DISCORD_TW_STOCK (台股報告)

DISCORD_US_STOCK (美股報告)

DISCORD_BLACK_SWAN (黑天鵝緊急警報)

DISCORD_GENERAL_NEWS (一般市場消息)


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
│  │    ├─news.py
│  │    └─vix_scanner.py
│  ├─ analysts/               # AI 預測邏輯 (台股、美股)
│  │    ├─base_analyst.py
│  │    └─market_analyst.py
│  └─ guardians/              # 風控邏輯 (Counterfactual, Defense)
│  │    ├─counterfactual.py
│  │    └─defense.py
│
├─ data/                      # 數據存放
│  ├─ history/                # 交易與預測歷史
│  │    └─tw_history.csv
│  ├─ models/                 # 訓練好的模型檔 (.json)
│  └─ system/                 # 系統狀態 (state.json, .flag)
│
├─ entrypoint.py              # 統一的腳本入口
├─ requirements.txt
└─ README.md
