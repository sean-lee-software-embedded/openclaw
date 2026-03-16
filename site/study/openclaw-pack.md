# OpenClaw 能力包（實戰版）

> 給已經有工程背景、想把 OpenClaw 用得更順、更聰明的人。
> 核心觀念只有一句：**不是換更強模型就會變強，而是把「模型 + 工具 + 技能 + 執行環境」配對對了。**

---

## 1. 先用一句話理解 OpenClaw

OpenClaw 不是單純聊天機器人，而是你自己設備上的 **AI 控制平面**：

- **Gateway**：中樞，負責 session、工具、通道、裝置、Web UI、cron、webhook
- **Model**：負責理解、推理、規劃、寫文字
- **Tools**：真正做事的手，例如 read/write/edit/exec/browser/nodes/cron/sessions
- **Skills**：把某一類工作流程封裝成可重用的 SOP
- **Runtime**：任務實際在哪裡跑、怎麼跑，例如主代理、subagent、ACP harness、裝置節點

所以「讓助手更聰明」的正確做法通常不是只升級模型，而是：

1. 給它正確上下文
2. 給它正確工具
3. 給它正確 skill
4. 讓任務在正確 runtime 上執行
5. 把常做工作變成穩定流程

---

## 2. 現在的 OpenClaw，強在哪裡

從目前 README / changelog / skill 設計看，OpenClaw 的主流用法已經很明確：

### A. 把聊天介面變成控制面板
不是只在 Telegram/Discord/Slack 回答問題，而是：

- 收訊息後查 GitHub、跑 shell、讀寫檔案
- 呼叫 browser / node / cron / webhook
- 把結果回送到原聊天介面

這種模式最適合你這種偏技術、偏 workflow 的使用者：**直接在對話裡下達操作級任務**。

### B. 用 subagent 分流複雜工作
OpenClaw 的 `sessions_spawn` 可把任務丟給隔離的子代理執行，完成後再回報主對話。很適合：

- 寫 code / refactor / PR review
- 大量 issue triage
- 長時間背景任務
- 需要獨立上下文的工作

### C. 用 skills 讓常見任務穩定化
技能本質上是「可重複的操作說明 + 工作慣例 + 安全邊界」。
不是讓模型變聰明，而是讓它**少走歪路、少亂猜、少發明流程**。

### D. 把遠端/多裝置接進來
OpenClaw 現在很適合做：

- 本機 Mac 控制
- Linux gateway 常駐
- iOS / Android / macOS node 配對
- Tailscale / SSH tunnel 安全遠端接入
- Dashboard / WebChat / Control UI 操作

### E. 把自動化做成「會持續運作的助手」
比起一次性問答，實務上更有價值的是：

- heartbeat 定時檢查
- cron 週期性任務
- webhook / PubSub 事件觸發
- GitHub issue / review 自動追蹤

---

## 3. 模型、工具、技能、runtime：怎麼分工

這四個概念如果分不清，很容易誤判能力邊界。

### Model = 大腦
負責：

- 理解需求
- 推理
- 寫摘要 / 寫程式 / 規劃步驟
- 根據觀察做決策

但模型本身 **不會**：

- 自己讀你的磁碟
- 自己看 GitHub 私有 repo
- 自己操作 tmux
- 自己打開手機鏡頭
- 自己背景常駐檢查

### Tool = 手和眼
負責：

- `read/write/edit`：檔案
- `exec/process`：shell / 長任務 / 背景程序
- `browser`：瀏覽器操作
- `nodes`：裝置能力（相機、畫面、通知、定位、system.run）
- `cron`：排程
- `sessions_*`：子代理 / 歷史 / 發送

**沒有工具，再強模型也只能猜。**

### Skill = 工作 SOP / 戰術模板
負責：

- 告訴代理「什麼情境該用什麼工具」
- 規範安全邊界
- 提供命令模式、排錯順序、輸出格式
- 降低模型每次從零思考的成本

你可以把 skill 想成：**帶有操作經驗的 playbook**。

### Runtime = 執行位置與執行方式
常見實務上可這樣理解：

- **main agent**：你正在對話的主要代理
- **subagent runtime**：隔離上下文的小代理，做完回報
- **ACP runtime / harness**：把 Claude Code / Codex / Pi / OpenCode 這種外部 coding harness 綁進 OpenClaw 工作流
- **node runtime**：裝置本地執行，例如手機/電腦上的 device-local action
- **gateway host runtime**：shell/exec 通常跑在 gateway 所在主機

一句話：

- **模型決定會不會想**
- **工具決定能不能做**
- **技能決定會不會做對**
- **runtime 決定在哪裡做、做得到多少**

---

## 4. Agents / Subagents / ACP harnesses：實務理解

## 4.1 Main agent
主代理就是平常跟你對話的那個。適合：

- 快速問答
- 協調任務
- 小修改
- 查資料
- 決策和彙整

不適合把所有複雜工作都塞進來，因為上下文會變髒。

## 4.2 Subagent
subagent 適合做「可獨立完成」的任務：

- 寫一個功能
- 掃 repo 找問題
- 做一輪 issue triage
- 長時間跑背景檢查

OpenClaw 的 `sessions_spawn` 會：

- 開新 session
- 給子代理隔離上下文
- 執行完後自動 announce 給主對話
- 預設不讓子代理再一直往下 spawn

**實戰觀念：subagent 是工作執行者，不是聊天角色。**

## 4.3 ACP harness
ACP runtime 比較像「把外部 coding agent / harness 接入 OpenClaw 的長工作通道」。
實務上適合：

- 在 Telegram / Discord thread/topic 綁定一個 coding harness
- 持續對同一個外部代理下指令
- 保留 thread-like 工作流
- 把 Claude Code / Codex / Pi 這類工具當作可持續互動的工作會話

如果你只是要一次性請子代理處理任務，subagent 就夠。
如果你要的是 **持續操控外部 coding harness**，才要想 ACP。

### 粗分原則

- **一般複雜任務** → subagent
- **長時間 coding flow / thread-bound harness** → ACP runtime
- **只是本地 shell 一次性操作** → exec

---

## 5. Skills 是什麼，為什麼真的有用

Skill 不是插件商店式的裝飾品，而是把常見任務從「看運氣」變成「有流程」。

它的價值在於：

- 減少模型瞎猜 CLI / flags
- 把高風險操作前置成檢查清單
- 讓排錯順序更穩定
- 讓相同需求每次都走同一套路

對技術使用者來說，skill 的真正價值不是 convenience，而是 **降低操作隨機性**。

---

## 6. 你最值得先用好的高價值 skills

以下是對你最有價值的一批。

### 6.1 coding-agent
**用途**：把寫程式、重構、PR review、長任務交給 Codex / Claude Code / Pi / OpenCode。

**何時最好用**：

- 新功能開發
- 中大型重構
- 需要探索大量檔案
- PR review 要在乾淨上下文裡做

**實務重點**：

- Codex / Pi / OpenCode 通常需要 PTY
- Claude Code 建議 `--print --permission-mode bypassPermissions`
- 長任務要配 `background:true`
- 要把 `workdir` 設準，避免代理亂逛

**對你特別有用的場景**：

- 讓主代理做 PM / reviewer
- 讓 coding-agent 當 implementation worker
- 用 process/tmux 監控長任務

### 6.2 github
**用途**：GitHub issue / PR / CI / run log / API 查詢。

**適合**：

- 查 PR 狀態
- 看 CI fail 在哪裡
- 建 issue / 留 comment / merge PR
- 快速拉 repo metadata

**為什麼重要**：
這個 skill 讓 OpenClaw 從「會寫 code」升級成「會跟工程流程互動」。

### 6.3 gh-issues
**用途**：批量抓 GitHub issues，spawn subagents 修復，開 PR，甚至追 review comments。

這個 skill 非常像 **issue orchestrator**。

**高價值場景**：

- 針對 bug label 批量處理
- watch 模式持續監控新 issue / review
- cron-safe 模式做定時掃描
- 把 repo maintenance 自動化

**如果你常帶團隊或維護 repo，這個 skill 很值。**

### 6.4 healthcheck
**用途**：檢查 OpenClaw 主機安全狀態、OpenClaw 安全審核、版本狀態、風險姿態。

**它很重要，因為很多人會誤以為 OpenClaw 幫你處理了主機安全。其實沒有。**

它會區分：

- OpenClaw 自身安全設定
- OS / firewall / SSH / 更新策略
- 遠端暴露方式
- 風險容忍度

**適合做基線檢查 + 定期 cron audit。**

### 6.5 node-connect
**用途**：排 iOS / Android / macOS node 配對與路由問題。

你只要開始玩：

- Android node
- iOS node
- macOS node mode
- Tailscale / remote gateway

這個 skill 就幾乎是必備。

它的價值不只是排錯，而是強迫你先釐清 topology：

- 同機
- 同 LAN
- 同 tailnet
- 公網 / reverse proxy

這種思路很工程，能少走很多冤枉路。

### 6.6 tmux
**用途**：遠端控制 tmux session、送按鍵、抓 pane output。

如果你把 Claude Code / Codex / 互動式 CLI 長期跑在 tmux，這 skill 很實用。

**典型場景**：

- 監控長時間編碼工作
- 回答互動式 prompt
- 抓取 session 狀態
- 遠端接手 TUI 任務

### 6.7 session-logs
**用途**：查自己過去 session JSONL 歷史。

這個 skill 很像「可稽核記憶層」。

適合：

- 找之前到底講過什麼
- 尋找決策脈絡
- 做回顧 / 成本分析 / tool usage 分析

對長期使用者來說，這比單純記憶更可靠，因為它是可查詢的歷史資料。

### 6.8 weather
**用途**：簡單天氣查詢。

不是核心 skill，但很適合放在 heartbeat 裡做低成本實用檢查。

---

## 7. 如何真的讓 OpenClaw 更有效

## 7.1 Prompt 要像委派，不要像閒聊

最有效的 prompt 通常包含這 5 件事：

1. **目標**：你要產出什麼
2. **範圍**：哪些檔案 / repo / 系統
3. **限制**：不要做什麼、不要動什麼
4. **驗收**：怎樣算完成
5. **回報格式**：你要它怎麼報告

### 好例子

- 「幫我檢查這個 repo 最近 5 個 failed CI，按 root cause 分類，先不要改 code，只給我修復優先順序。」
- 「在 `firmware/` 內找造成 boot timeout 的路徑，先做分析與最小修補提案，不要直接改 10 個檔案。」
- 「幫我用 subagent 做 PR review，列 blocker / nits / 風險，不要重複作者已知事項。」

### 差例子

- 「幫我看一下」
- 「你覺得怎麼辦」
- 「讓它更好」

對強模型也是一樣：**模糊需求只會得到模糊行為。**

## 7.2 把 workspace 文件當成能力放大器

你現在這套 OpenClaw 本身就有這個思路：

- `AGENTS.md`：規則、工作方式、紅線
- `SOUL.md`：語氣與人格
- `USER.md`：你的背景與偏好
- `TOOLS.md`：環境特定資訊
- `MEMORY.md` / `memory/*.md`：長短期記憶
- `HEARTBEAT.md`：週期巡檢 SOP

### 真正有幫助的寫法

**AGENTS.md**：
- 哪些操作可直接做
- 哪些一定先問
- commit / branch / PR 習慣
- 你討厭什麼回覆風格

**TOOLS.md**：
- SSH host alias
- 常用 server / camera / device 名稱
- 特定 repo 位置
- 常用 CLI 慣例

**USER.md**：
- 你的決策風格
- 你偏好的輸出格式
- 你最常做哪幾種任務

這些文件的作用不是「讓回答更人味」，而是**減少代理每次重新建立工作模型的成本**。

## 7.3 Memory 要有層次，不要把所有事都塞長記憶

實務上建議：

- `memory/YYYY-MM-DD.md`：原始事件、暫時線索、當天進展
- `MEMORY.md`：長期有價值的偏好、決策、慣例、重要背景

### 什麼該進 MEMORY.md

- 長期偏好
- 固定工作習慣
- 常見專案脈絡
- 值得永久保留的教訓

### 什麼不該進 MEMORY.md

- 一次性的 task 狀態
- 臨時 debug 細節
- 每天都會變的雜訊

**好的記憶系統不是越多越好，而是越容易在正確時候被用到越好。**

## 7.4 Heartbeat：讓助手主動，但不要煩

Heartbeat 適合：

- 批次檢查 email / calendar / weather / GitHub / CI
- 做輕量巡檢
- 整理 memory
- 回報重要變化

### 你可以把 HEARTBEAT.md 寫成這種風格

- 每日 2–4 次輪詢：GitHub 通知、重要 CI、日程、天氣
- 超過 8 小時沒主動提醒且有新事件才回報
- 深夜除非 urgent 不主動打擾
- 每次順便更新 `memory/heartbeat-state.json`

Heartbeat 的價值在於：**把多個低頻任務合併成一個低干擾巡檢節奏。**

## 7.5 Cron：給精準時間、獨立任務

Cron 適合：

- 每天固定時間跑安全 audit
- 每小時檢查特定 repo issue / review
- 早上固定整理 dashboard / 狀態
- 一次性 reminder

如果 heartbeat 是巡邏員，cron 就是排班系統。

### 一個好原則

- **需要精準時間** → cron
- **需要批次巡檢與情境感知** → heartbeat

## 7.6 Dashboard / Control UI / WebChat：別只靠 Telegram

現在 OpenClaw 本身就有 Gateway Control UI 與 WebChat。這些對技術用戶的價值很實際：

- 看 session 狀態
- 看工具結果
- 做配置與觀察
- 避免重度工具輸出全擠在聊天介面

如果你開始把 OpenClaw 用成控制平面，**Web UI 幾乎是必要，不是可有可無。**

## 7.7 GitHub Pages / 公開 artifacts：把輸出變可分享成果

很適合把 OpenClaw 產物做成：

- 分析報告 HTML
- 測試報告靜態頁
- 圖表 / 指標頁面
- 每日 / 每週摘要頁

常見做法：

- 讓代理生成 markdown / html / json artifacts
- commit 到 repo
- 用 GitHub Pages 或其他靜態站點公開

這樣聊天不只是結論，而是通往可瀏覽成果的入口。

## 7.8 安全遠端接入：優先 tailnet / SSH tunnel，不要急著公網暴露

從目前 README 的建議看，安全路徑很清楚：

### 優先順序
1. **Tailscale Serve**：尾網內 HTTPS，最適合私人遠端使用
2. **SSH tunnel**：簡單、可控
3. **Tailscale Funnel / public URL**：有明確需求再開

### 原則

- `gateway.bind` 盡量維持 loopback
- 真要遠端，優先 tailnet，不要直接裸露服務
- 公開入口要有 password/token auth
- 先做 `openclaw security audit --deep`

對你這種技術使用者，我會很直接：
**先把遠端 access path 想清楚，再談功能擴充。**

---

## 8. 哪些事情不是換更強模型就能補的

這一段很重要。

### 8.1 沒有工具權限，就做不了
例如：

- 想看 repo 實際內容 → 要 `read` / `git` / `gh`
- 想改檔案 → 要 `write` / `edit`
- 想跑測試 → 要 `exec`
- 想查 CI run → 要 `gh` 或 API
- 想控制手機/電腦 → 要 `node` 配對與授權

### 8.2 沒有正確 runtime，就做不對地方
例如：

- 想在手機上執行裝置動作，不是靠主機模型，而是靠 node runtime
- 想持續操作 Codex/Claude Code thread，不是單純 subagent，而是 ACP/harness flow
- 想跑背景長任務，不是同一個聊天回合硬撐，而是 background + process / subagent

### 8.3 沒有 skill，模型常會「差一點」
它可能知道大方向，但：

- CLI flag 亂猜
- 排錯順序不穩
- 少做前置檢查
- 漏掉安全邊界

### 8.4 沒有文件與記憶，模型每次都像剛上工
你如果沒有把：

- repo 慣例
- 遠端主機資訊
- 你偏好的工作方式
- 過去決策

寫進 workspace，模型再強也會反覆重新猜。

---

## 9. 給你的實戰建議：最值得先完成的升級順序

## 第 1 階段：把基本面做對

1. 補強 `AGENTS.md` / `TOOLS.md` / `USER.md`
2. 建立 `HEARTBEAT.md`
3. 確認 `MEMORY.md` 與 daily memory 使用規則
4. 熟悉 Control UI / WebChat

## 第 2 階段：把工程流接進來

1. 設好 `github`
2. 開始用 `coding-agent`
3. 把 PR review / issue triage 交給 subagent
4. 有需求再上 `gh-issues`

## 第 3 階段：把多裝置 / 遠端做穩

1. 決定 gateway 在哪台機器
2. 決定 remote access path（優先 Tailscale / SSH）
3. 需要時配 iOS / Android / macOS node
4. 用 `node-connect` 建立排錯基線

## 第 4 階段：把它變成會持續工作的系統

1. 用 heartbeat 做巡檢
2. 用 cron 做固定任務
3. 用 artifacts / GitHub Pages 發佈結果
4. 用 `healthcheck` 做定期安全檢查

---

## 10. 一套很務實的使用心法

### 問自己 4 個問題

1. **這件事主要是思考，還是操作？**
2. **如果要操作，需要哪些工具？**
3. **這是一次性任務，還是要長期維持上下文？**
4. **它應該在哪裡執行：主機、子代理、ACP harness、還是裝置 node？**

只要這四題答對，OpenClaw 大多就會好用很多。

---

## 11. 最後的結論

OpenClaw 的上限，不是單看模型，而是你是否把它組成一個完整系統：

- **模型**負責判斷與生成
- **工具**負責取得真實世界能力
- **skill**負責把任務做穩
- **runtime**負責在對的地方執行
- **workspace docs + memory** 負責長期一致性
- **heartbeat/cron/UI/remote access** 負責從一次性聊天進化成持續運作的助手

對你這種工程背景使用者，最值得追求的不是「更像聊天機器人」，而是：

> **把 OpenClaw 調成一個可觀測、可委派、可追蹤、可擴充的個人 AI 作業系統。**
