# 🦞 龍蝦系統 (Lobster System)

嵌入式系統工程師的個人技術工具，包含新聞爬蟲、Telegram Bot、Kanban/Scrum Board。

## 架構

```
lobster_system/
├── crawler/          # RSS 爬蟲 + LLM 摘要
│   └── crawler.py
├── telegrambot/      # Telegram Bot
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
├── board/            # Kanban + Scrum Board
│   ├── server.py     # Flask API (port 3333)
│   └── static/
│       └── index.html  # 前端 UI（單一 HTML，無需 build）
├── scripts/
│   └── daily_run.sh  # 每日排程腳本
├── data/             # 資料存放（articles.json, board.json 等）
├── logs/             # 每日執行 log
└── requirements.txt
```

## 爬蟲 Topics

1. **☁️ Cloud Server 市場動態** — ServeTheHome、The Register、AnandTech 等
2. **🔧 OpenBMC / Redfish** — OpenBMC GitHub、Phoronix、LWN.net 等
3. **🤖 AI 最新消息** — HuggingFace、Anthropic、VentureBeat、Papers With Code 等

## 快速啟動

### 1. 安裝依賴

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Telegram Bot

```bash
cp telegrambot/.env.example telegrambot/.env
# 編輯 .env，填入 TELEGRAM_BOT_TOKEN
# 編輯 telegrambot/app.py，填入你的 Telegram user IDs 到 ALLOWED_USERS

source telegrambot/.env
python3 telegrambot/app.py
```

### 3. Board UI

```bash
# 啟動 API server
python3 board/server.py
# 瀏覽器開啟 http://localhost:3333
```

### 4. 手動跑爬蟲

```bash
python3 crawler/crawler.py
```

需要本地 Ollama 運行 `qwen2.5:14b` 才能生成摘要。

### 5. 設定每日排程（每天 8:00）

```bash
crontab -e
# 加入：
0 8 * * * /Users/sean/projects/lobster_system/scripts/daily_run.sh
```

## Telegram Bot 指令

| 指令 | 功能 |
|------|------|
| 今日新聞 | 今天完整文章列表 |
| 摘要 | AI 生成的今日摘要 |
| 清除記憶 | 重置 LLM 對話 |
| 幫助 | 顯示所有指令 |
| 其他文字 | 問本地 LLM |

## Board 功能

- **Kanban**：5 欄（Backlog → Done），卡片可左右移動
- **Scrum**：Sprint 管理、Burndown Chart、Backlog 拖入 Sprint
- Labels：Cloud/BMC、AI、Infra、Bug、Feature、Chore
- 暗色主題，純 HTML 無需 build 工具
