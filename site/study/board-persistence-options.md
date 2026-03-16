# PRJ-11：Board 持久化重設方案（跨裝置 / 可追蹤）

## 問題本質

目前 `board.html` 的資料存放方式是：

- 初始資料寫在前端頁面內
- 使用者操作後存進瀏覽器 `localStorage`
- 之後只由**當前瀏覽器 / 當前裝置**讀回

這個模型的根本限制：

1. **不共享**
   - A 裝置新增 PRJ-11，B 裝置看不到
   - 同一個人換手機、換電腦，也像是不同系統

2. **不可協作**
   - 多人使用時，每人都在改自己的本地副本
   - 沒有單一真實來源（single source of truth）

3. **不可稽核**
   - 無法可靠追蹤誰在什麼時間改了哪張 ticket
   - 也沒有可用的歷史版本、變更紀錄、回滾機制

4. **易遺失**
   - 清掉瀏覽器資料、換瀏覽器、無痕模式，都可能直接消失

5. **不適合 scrum / board ticket 管理**
   - Ticket 應該是「專案資產」，不是「某個瀏覽器暫存」
   - 只要任務要被追蹤、分派、更新狀態，就不能依賴 localStorage

結論：**目前做法適合 demo，不適合正式追蹤。**

---

## 評估目標

這次不是追求最完整 Jira 替代品，而是找：

- 能在 **GitHub Pages / 靜態站** 現況下快速落地
- 讓每張 task 真的變成可追蹤 ticket
- 能跨裝置同步
- 後續能逐步升級，不用整個重做

評估維度：

- 部署複雜度
- 跨裝置同步能力
- 多人協作能力
- 歷史追蹤 / auditability
- 與目前 GitHub Pages 架構相容性
- 後續演進空間

---

## 方案比較

## 方案 A：GitHub repo 裡放 `board-data.json`，前端讀取

做法：

- 將 board 資料改存成 repo 內的 JSON，例如 `site/data/board-data.json`
- `board.html` 改為啟動時 fetch JSON
- GitHub Pages 負責公開讀取

### 優點

- 與現在靜態站最相容
- 前端改動小
- 所有裝置都能讀到同一份資料
- JSON 可進 git，有版本歷史

### 缺點

- **只能解決「共享讀取」**，不能自然解決「共享寫入」
- 瀏覽器前端無法安全地直接寫回 GitHub repo
- 若要從頁面直接更新 JSON，需要 GitHub token，但 token 不能安全放在前端
- 多人同時編輯時容易衝突

### 適用情境

- 適合先把 board 從 localStorage 升級成「共享唯讀資料源」
- 不適合真正的即時 ticket 寫入系統

### 判斷

**可當過渡層，但不能當完整答案。**

---

## 方案 B：Static JSON + commit workflow（手動或腳本更新）

做法：

- 仍以 JSON 當資料源
- 但新增 / 更新 ticket 不在前端直接寫入
- 改由：
  - 開發者手動改 JSON + commit
  - 或用 script / GitHub Action / CLI 來更新 JSON

### 優點

- 實作快
- 完全符合 GitHub Pages 靜態部署模型
- 每次變更都有 commit 紀錄
- 不需要額外後端服務

### 缺點

- 操作流不順，像「內容發布」不是「任務管理」
- 非技術使用者不友善
- 無法自然支援多人日常更新
- 衝突與 merge 成本高

### 適用情境

- 少量 ticket
- 主要由 1 位維護者操作
- 目標是先把資訊集中，而不是建立真正 workflow

### 判斷

**比 localStorage 好很多，但仍偏 workaround。**

---

## 方案 C：GitHub Issues 當 backend（建議優先考慮）

做法：

- 每張 task = 一張 GitHub Issue
- board 欄位對應：
  - 狀態：label / issue state / project field
  - 優先級：label
  - 負責人：assignee
  - sprint / epic：milestone、label，或 issue body/frontmatter
- `board.html` 改成呼叫 GitHub API（建議經由小型代理層，不要直接在前端放 token）讀取 issues
- 新增 / 更新 ticket 時，實際上是在建立 / 更新 GitHub Issue

### 優點

- **天然有 ticket identity**：每張 issue 都有唯一 ID / URL / 歷史
- **天然可追蹤**：comment、timeline、assignee、label、closed/reopen 都有
- **多人協作成熟**：通知、權限、mention、審核流程都現成
- **與工程開發流程接近**：issue ↔ PR ↔ commit 可以串起來
- 不必自己重新發明 audit log

### 缺點

- UI 需要做 mapping，不是原生就等於 scrum board
- 若要在公開 GitHub Pages 前端直接寫 GitHub API，會碰到 token 安全問題
- GitHub Issues 很適合工程 ticket，但若未來要非常客製的欄位 / 報表，可能受限

### 適用情境

- 目前已有 GitHub repo
- 任務本質偏工程 / 專案追蹤
- 希望快速把「每件事都變 ticket」落地

### 判斷

**這是目前最實際、風險最低、最符合現況的方案。**

---

## 方案 D：輕量 API / backend（Cloudflare Workers / Supabase / Firebase / 自架小服務）

做法：

- 建立一個真正的資料 API
- 前端只呼叫 API 讀寫 ticket
- 資料可存 PostgreSQL / SQLite / Supabase / Firestore 等

### 優點

- 架構最正統
- 可自由定義資料模型、權限、欄位、查詢、報表
- 未來要做 webhook、通知、統計、權限控管都比較容易

### 缺點

- 需要額外部署與維運
- 需要處理認證、授權、API 安全、備份、監控
- 對目前「GitHub Pages 靜態站」來說跳幅較大

### 適用情境

- ticket 數量、使用者數、流程複雜度都持續成長
- 需要真正的產品級 board system
- 願意接受後端維運成本

### 判斷

**長期最好，但不是現在最快。**

---

## 方案 E：前端直連 GitHub API（在瀏覽器放 token）

做法：

- `board.html` 直接呼叫 GitHub API 建 issue / 改 label
- token 放在前端或 localStorage

### 優點

- 看起來最快

### 缺點

- **不安全，基本上不建議**
- token 很容易外洩
- 公開 GitHub Pages 上尤其不適合

### 判斷

**排除。**

---

## 建議結論

## 最佳下一步：**以 GitHub Issues 作為 ticket 真實來源（system of record）**

原因很直接：

1. **現在就有 GitHub repo / GitHub Pages**
2. **task 本來就適合映射成 issue**
3. **需要跨裝置、可追蹤、可稽核**，GitHub Issues 都已內建
4. **比自建 backend 快很多**
5. 之後若未來真的要升級，也能把 Issues 當過渡資料源，不是白做

### 核心設計建議

- `board.html` 不再把 `issues` 存 localStorage 當主資料
- localStorage 最多只保留：
  - UI 偏好（例如 filter、sidebar 開關、排序）
  - 暫存草稿（非正式資料）
- 正式 ticket 來源改為 GitHub Issues

### 欄位映射建議

- `key`：用 issue number，例如 `PRJ-11`
- `title`：issue title
- `description`：issue body
- `status`：label（`todo` / `inprogress` / `inreview` / `done`）
- `priority`：label（`p0` / `p1` / `p2` / `p3`）
- `type`：label（`story` / `bug` / `task`）
- `assignee`：GitHub assignee
- `sprint`：milestone 或 `sprint:*` label
- `epic`：`epic:*` label，或 issue body 中引用 epic
- `comments`：issue comments
- `createdAt / updatedAt`：GitHub 內建欄位

這樣一來，board 只是 GitHub Issues 的視圖層，不再自己承擔資料真實來源角色。

---

## 分階段落地方案

## Phase 1：最快可用（建議先做）

目標：**先讓所有 task 變成真正可共享、可追蹤的 ticket**

### 作法

1. 定義 label 規則
   - `status:todo`
   - `status:inprogress`
   - `status:inreview`
   - `status:done`
   - `type:story` / `type:bug` / `type:task`
   - `priority:p0` ~ `priority:p3`
   - `epic:*`

2. 人工或腳本將現有 board item 匯入 GitHub Issues

3. `board.html` 改成：
   - 先讀 GitHub Issues API 或預先生成的 JSON
   - 以 labels / assignee / milestone 渲染 board

4. localStorage 只保留 UI 狀態，不再存正式 issue data

### 兩種 Phase 1 實作路徑

#### 1A. 最穩：GitHub Action 定時輸出 `issues.json`

流程：
- GitHub Action 讀 repo issues
- 轉成前端需要的 `issues.json`
- 輸出到 `site/data/issues.json`
- GitHub Pages 前端只 fetch 這份 JSON

優點：
- 前端完全不用 token
- 最符合靜態站模型
- 穩、簡單、低風險

缺點：
- 不是即時，會有同步延遲（例如 1~5 分鐘，或每次 push / schedule）

#### 1B. 較靈活：加一個極小 proxy API

流程：
- 前端打小型 API
- API 代呼叫 GitHub API
- token 放 server side

優點：
- 可以較即時
- 後續支援新增 / 更新 issue 比較自然

缺點：
- 需要額外部署一層服務

### Phase 1 建議選擇

**先做 1A（GitHub Action 產出 `issues.json`）。**

原因：
- 幾乎不改部署模型
- 安全性最好
- 可以很快驗證「GitHub Issues 當資料源」是否順手

---

## Phase 2：中期較佳方案

目標：**不只看板可視化，還能從 board 介面操作 ticket**

### 作法

新增一層輕量寫入服務，例如：
- Cloudflare Workers
- Vercel Serverless Function
- Netlify Function
- 或 repo 外的小型 Node API

負責：
- 建立 issue
- 更新 label / assignee / milestone
- 新增 comment
- 驗證使用者身份（至少 basic gate）
- 安全保存 GitHub token

### 好處

- 保持 GitHub Issues 為真實來源
- board UI 可以真的拖拉改狀態、建立 ticket
- GitHub Pages 仍可保留為前端靜態站

### 這一階段的架構會變成

- Frontend：GitHub Pages
- Write API：serverless / lightweight backend
- Source of truth：GitHub Issues

這是我認為**最平衡**的中期型態。

---

## Phase 3：長期最佳方案

目標：**當 ticket 流量、使用者數、客製需求變多時，升級成正式 ticket service**

### 作法

建立自有 ticket backend：
- DB：Postgres / Supabase
- API：REST / GraphQL
- Auth：GitHub OAuth / Google OAuth / internal auth
- Event：webhook / audit log / notification

GitHub Issues 角色可改為：
- 與工程開發同步的外部鏡像
- 或只保留 code-related work item

### 適合升級的訊號

- 需要更細的權限模型
- 需要自訂欄位很多
- 需要複雜報表 / burn-down / SLA / workflow rule
- 非工程人員大量使用
- Issue label / milestone 映射開始變得勉強

---

## 實務建議：這個專案現在怎麼選

如果目標是：

- 這兩天內就把 board 從 demo 變成可用
- 又不想立刻維運後端

那我的建議是：

### **先做 GitHub Issues + GitHub Action 匯出 JSON**

也就是：

1. **所有正式 task 改用 GitHub Issues 建立與管理**
2. `board.html` 改成讀 `issues.json`
3. `issues.json` 由 GitHub Action 從 Issues 自動產生
4. localStorage 退回成 UI cache only

這樣的好處是：

- 立刻跨裝置
- 立刻有歷史紀錄
- 立刻能分享 ticket URL
- 立刻能接 PR / commit
- 幾乎不破壞現有 GitHub Pages 架構

---

## 最小可行資料模型（若要先轉 JSON）

若 Phase 1 先透過 `issues.json` 給前端吃，建議格式像這樣：

```json
{
  "project": {
    "key": "PRJ",
    "name": "OpenClaw Project Board",
    "source": "github-issues",
    "repo": "owner/repo",
    "syncedAt": "2026-03-16T01:30:00Z"
  },
  "issues": [
    {
      "id": 11,
      "key": "PRJ-11",
      "number": 11,
      "title": "Redesign board persistence for cross-device tracking",
      "type": "story",
      "status": "todo",
      "priority": "p1",
      "assignee": "sean",
      "epic": "board-foundation",
      "sprint": "sprint-1",
      "url": "https://github.com/owner/repo/issues/11",
      "description": "...",
      "labels": ["status:todo", "type:story", "priority:p1"],
      "createdAt": "2026-03-16T01:00:00Z",
      "updatedAt": "2026-03-16T01:20:00Z"
    }
  ]
}
```

重點不是欄位多漂亮，而是：**前端資料模型要明確承認 source of truth 在 GitHub，不在瀏覽器。**

---

## 最後結論

### 不建議再延伸 localStorage 模型

因為它先天就不是協作型 ticket system 的基礎。

### 最務實的路

- **最快可用**：GitHub Issues + GitHub Action 匯出 `issues.json`
- **中期較佳**：GitHub Issues + 輕量寫入 API
- **長期最佳**：正式 backend / DB ticket service

如果只選一個「現在就該做」的 next step：

## **把 board 的正式資料源改成 GitHub Issues。**

這一步最關鍵。因為一旦 ticket identity 與歷史開始落在 GitHub，後面 UI、同步、報表、API 都還能慢慢補；但如果正式資料還留在 localStorage，後面所有功能都會建立在錯的基礎上。