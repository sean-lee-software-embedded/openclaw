# OpenClaw Cheatsheet（繁中實戰速查）

## 一句話判斷

- **要想清楚** → 換好 prompt / 模型
- **要真的做事** → 需要工具
- **要穩定重複做** → 需要 skill
- **要在對的地方做** → 需要對 runtime

---

## 1) 能力分層

### Model
負責理解、推理、規劃、寫內容。

### Tool
負責真實操作：
- 檔案：`read` / `write` / `edit`
- Shell：`exec` / `process`
- GitHub：`gh` 或 API
- 瀏覽器：`browser`
- 裝置：`nodes`
- 排程：`cron`
- 子代理：`sessions_spawn`

### Skill
針對任務的 SOP / playbook。

### Runtime
任務在哪裡跑：
- main agent
- subagent
- ACP harness
- gateway host
- device node

---

## 2) 任務路由速查

### 小事、一次性、低風險
- 直接 main agent + read/edit/exec

### 複雜任務、需要乾淨上下文
- 用 **subagent**

### 長時間 coding flow、要持續互動 thread
- 用 **ACP harness/runtime**

### 要在手機/電腦本機做事
- 用 **node runtime**

### 要固定時間跑
- 用 **cron**

### 要低頻巡檢、順便看上下文
- 用 **heartbeat**

---

## 3) 高價值 skills

### `coding-agent`
用於：
- 新功能
- 重構
- PR review
- 需要探索 repo 的任務

關鍵：
- Codex / Pi / OpenCode 常要 PTY
- Claude Code 用 `--print --permission-mode bypassPermissions`
- 長任務用 background
- `workdir` 要準

### `github`
用於：
- 查 PR / issue / CI / logs
- 建 issue / 留言 / merge

### `gh-issues`
用於：
- 自動抓 issues
- spawn subagents 修復
- 開 PR
- 追 review comments
- 適合 watch / cron 模式

### `healthcheck`
用於：
- OpenClaw 安全 audit
- 主機暴露面 / 更新 / firewall / SSH 檢查
- 建議定期跑

### `node-connect`
用於：
- iOS / Android / macOS node 配對失敗
- Tailscale / publicUrl / remote gateway / pairing 問題

### `tmux`
用於：
- 控制互動式 CLI session
- 監控 Claude/Codex 類長任務

### `session-logs`
用於：
- 查過去聊天紀錄
- 回顧決策脈絡
- 做成本 / 工具使用分析

### `weather`
用於：
- heartbeat 裡順手查天氣

---

## 4) 什麼不是強模型能解決的

### 單靠模型不行的事
- 讀你本地檔案
- 跑測試
- 查私有 GitHub
- 控制 tmux
- 操作手機鏡頭/通知
- 做背景排程

### 症狀判斷
- **回答很像，但沒真的做** → 缺工具
- **工具有了但一直做歪** → 缺 skill
- **看起來會，但做不到那台機器上** → runtime 不對
- **每次都忘記你的偏好** → docs / memory 不足

---

## 5) 最值得優化的 workspace 檔案

### `AGENTS.md`
寫：
- 可直接做 / 一定要先問的事
- commit / branch / PR 習慣
- 回覆風格偏好

### `TOOLS.md`
寫：
- SSH alias
- 常用 host / server / 裝置名稱
- 路徑與環境特定備註

### `USER.md`
寫：
- 你的背景
- 決策風格
- 偏好輸出格式
- 常做任務類型

### `MEMORY.md`
寫：
- 長期有效偏好
- 穩定流程
- 重要教訓

### `memory/YYYY-MM-DD.md`
寫：
- 當天進度
- 暫時線索
- 最近發生的事

### `HEARTBEAT.md`
寫：
- 定期要檢查什麼
- 什麼情況主動提醒
- 什麼情況保持安靜

---

## 6) Prompt 模板

### 任務委派模板
```text
目標：
範圍：
限制：
驗收標準：
回報格式：
```

### 範例 1：PR review
```text
幫我 review 這個 PR。
目標：找 blocker / 風險 / 測試缺口
範圍：只看本 PR 變更
限制：不要改 code
驗收標準：列出 must-fix 與 nice-to-have
回報格式：先摘要，再條列問題
```

### 範例 2：repo debug
```text
幫我在 firmware/ 找 boot timeout 根因。
限制：先分析，不要直接大改
驗收標準：給 root cause、最小修補方案、風險
```

---

## 7) Heartbeat vs Cron

### 用 Heartbeat
適合：
- Email / calendar / weather / GitHub 批次巡檢
- 有上下文的低頻主動提醒
- 記憶整理

### 用 Cron
適合：
- 每天固定時間任務
- 每小時安全檢查
- 固定 repo 掃描
- 一次性 reminder

### 快速判斷
- **需要準時** → cron
- **需要情境感知與批次** → heartbeat

---

## 8) 遠端接入優先順序

1. **Tailscale Serve**
2. **SSH tunnel**
3. **公開 URL / Funnel**（真的需要再開）

原則：
- 優先維持 `gateway.bind=loopback`
- 先做安全 audit
- 公網暴露一定要有 auth

---

## 9) 你很可能會用到的組合

### GitHub 維運組合
- `github` + `gh-issues` + subagents

### 編碼工作組合
- `coding-agent` + `tmux` + `process`

### 多裝置組合
- `node-connect` + nodes + Tailscale

### 長期記憶 / 回顧組合
- `session-logs` + MEMORY.md + daily memory

### 主動助理組合
- heartbeat + cron + dashboard/WebChat

---

## 10) 最佳實踐清單

- 任務大於 5–10 分鐘：丟 subagent 或 background
- repo 任務先說清楚 workdir / 範圍
- 把穩定資訊寫進 workspace docs，不要靠模型記住
- 需要定期執行的事，不要靠你每次重新提醒
- 先決定執行位置，再決定模型
- 先決定 access path，再開遠端功能

---

## 11) 給技術使用者的直白版結論

OpenClaw 要變強，不是只升模型，而是：

- 文件補全
- skill 用對
- runtime 選對
- tool 開對
- 自動化接上
- 安全邊界設好

> 把它當成「可委派的 AI 控制平面」，而不是單純聊天 bot，價值才會真正拉開。
