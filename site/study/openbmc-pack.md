# OpenBMC 1 週衝刺學習包

對象：有多年 embedded 經驗、曾熟 Redfish，但約 5 年沒碰；目前目標是**盡快能看懂 OpenBMC 專案、能追 issue、能改 Yocto/服務、能跟 MCTP/PLDM/CI 團隊對話**。

---

## 0. 先講結論：這 1 週最值得抓住的主線

如果只記 4 件事：

1. **OpenBMC 本質上是 Yocto 產出的 Linux 發行版**，不是單一 daemon。  
2. **資料真相多半在 D-Bus**；`bmcweb` 多半是把 D-Bus/服務狀態翻成 Redfish/REST。  
3. **Host/BMC/周邊管理通道正在從 IPMI 轉向 MCTP + PLDM**；MCTP 是 transport，PLDM 是 message/data model。  
4. **做事效率關鍵不在懂完 Yocto，而在知道哪幾層、哪幾個 recipe、哪幾個 cache、哪幾條 pipeline 會動到。**

---

## 1. Redfish：這 5 年實務上變了什麼？

你如果 5 年前停在「系統、電源、風扇、帳號、更新、基本 Event」那一代，現在重點不是核心精神變了，而是：

### 1.1 Redfish 已更成熟成為「完整管理平面」

過去比較像 modernized IPMI/REST API；現在更明顯變成：

- **完整 schema 生態**更大
- **互通性要求更高**（Interop Profile / validator / conformance）
- **事件、遙測、證書、更新流程**更完整
- 與 **CXL、Fabric、組態匯出匯入、aggregation/composability** 的整合更實用

### 1.2 實務上你要補的 delta

#### A. Telemetry 比以前重要很多

以前常停在 sensor pull；現在要補的是：

- `TelemetryService`
- metric report / trigger
- event 與 metric report 的串接
- bulk telemetry / streaming 的方向

對 BMC 團隊的意義：
- 不只是「能讀 sensor」；而是要能設計**可訂閱、可批次取用、可送出報表**的資料流。

#### B. Event 模型更成熟

現在要熟的是：

- EventService / EventDestination
- 訂閱過濾
- push event
- metric report event
- 與 journal/log service 的對映

在 OpenBMC 裡，這通常不是獨立資料庫概念，而是跟 `bmcweb`、log service、D-Bus state 對映有關。

#### C. 憑證/安全能力更完整

近幾年實務上更常看到：

- certificate lifecycle
- CSR / certificate install
- 自動 enrollment（SCEP / ACME 方向）
- service TLS / mTLS 管理
- 帳號、權限、security mode 類 schema 增長

如果你以前把 Redfish 當「管理資料 API」，現在要把它也看成**安全控制平面的一部分**。

#### D. Firmware Update / 組態管理比以前更像正式產品能力

你要注意：

- staged update / multipart upload / image store 類能力
- 服務組態匯入/匯出
- 多裝置/大規模更新情境

這跟 OpenBMC 團隊最直接的交集是：
- `bmcweb` API 行為
- software manager / image activation
- 後端 D-Bus 物件與 state machine

#### E. Interoperability / conformance 壓力更實際

這 5 年很明顯的一點是：

- 不只是「有 API」就算完成
- 要考慮 schema version、validator、profile、message registry
- 客戶/測試會更常拿 Redfish validator、interop profile 來卡你

**一句話總結：**  
Redfish 沒有「改宗」，但已從 API 規格成長成**產品互通與管理自動化的核心介面**。

---

## 2. OpenBMC 架構速覽：Redfish、bmcweb、D-Bus、MCTP、PLDM 在哪裡？

### 2.1 心智模型

```text
外部管理工具 / 自動化 / 測試系統
        |
   HTTPS / Redfish / REST / WebSocket
        |
      bmcweb
        |
     D-Bus / systemd / services
        |
  各種 OpenBMC daemon 與 manager
        |
   MCTP transport  <---->  Host / NIC / satellite controller / PCIe 裝置
        |
      PLDM messages
```

### 2.2 分層理解

#### 最外層：Redfish / REST

- 對外 API 入口多由 **`bmcweb`** 提供
- `bmcweb` 同時承擔：
  - Redfish
  - OpenBMC REST
  - websocket / event
  - 某些 console / KVM 相關 web 能力

#### 中間層：D-Bus

- OpenBMC 內部服務之間最核心的 IPC 是 **D-Bus**
- inventory、sensor、state、logging、software、network 等，多半用 D-Bus object / property / signal 表達
- **很多 Redfish 資料不是 bmcweb 自己算出來，而是從 D-Bus 讀出來再轉 schema**

#### 服務層：各種 manager / daemon

常見思路：
- 某個 daemon 管 sensor / inventory / logging / software / state
- 這些 daemon 在 D-Bus 上暴露物件
- `bmcweb` 把它們翻出去

#### Host / device 通道層：MCTP + PLDM

- 面向 host firmware、satellite controller、NIC、PCIe 裝置等「box 內管理通訊」時，OpenBMC 越來越常走 **MCTP + PLDM**
- **MCTP**：把不同實體媒介（I2C/SMBus、PCIe、UART…）抽象成共同 transport
- **PLDM**：在 MCTP 之上提供 inventory / sensor / control / FRU / firmware update 等標準訊息模型

### 2.3 你該怎麼看 OpenBMC 問題

#### 如果是「Redfish 回傳不對」
先問：
1. `bmcweb` route/schema mapping 有沒有問題？
2. 對應的 D-Bus object/property 存不存在？
3. 後端 daemon 有沒有把資料放上 D-Bus？

#### 如果是「Host/BMC 裝置資料不對」
先問：
1. MCTP endpoint discovery / EID / routing 是否正常？
2. PLDM requester/responder 流程是否正常？
3. PLDM 資料有沒有正確轉成 D-Bus inventory / sensor / state？
4. `bmcweb` 是否只是把上游錯資料照實翻出？

**這是 OpenBMC debug 最重要的觀念：外面看 Redfish，裡面多半要追 D-Bus，再往下追 transport/protocol。**

---

## 3. MCTP essentials：你要懂到什麼程度才算能工作？

### 3.1 一句話定義

**MCTP = 管理訊息的傳輸層標準。**  
它解決的是「管理訊息如何在不同裝置之間被送到正確 endpoint」，不是定義高層管理語意。

### 3.2 為什麼重要

IPMI 的問題之一是 transport 與 data model 綁太死，而且硬體通道限制多。MCTP 的價值在：

- 把 **transport** 從高層 protocol 拆開
- 可以跑在多種 physical binding 上
- 以上層來看，只需要知道對方的 **EID（Endpoint ID）**
- 為 PLDM、SPDM、NVMe-MI 等提供共同通道

### 3.3 你至少要熟的名詞

- **EID**：MCTP endpoint 的邏輯位址
- **Bus owner**：負責 discovery / EID assignment / routing 管理的角色
- **Binding**：MCTP 跑在哪種媒介上，例如 SMBus/I2C、PCIe、serial
- **Message vs Packet**：大訊息可能被切成多個 packet 傳送，再重組
- **Routing / discovery**：多 endpoint 存在時，誰分配、誰找到誰

### 3.4 在 OpenBMC 裡它出現在哪

你會在這幾個層面看到它：

- kernel 或 userspace 的 MCTP stack
- MCTP daemon / socket API / D-Bus interface
- endpoint discovery
- 給 `pldmd`、SPDM、裝置管理 daemon 當 transport

OpenBMC 官方設計文件的方向是：
- **新設計偏向 kernel-based MCTP + sockets API**
- 舊式 userspace demux 架構存在，但不建議新案採用

### 3.5 實務上要問的 5 個問題

1. 這條通道的 **binding** 是什麼？（SMBus / PCIe / UART / 其他）  
2. 誰是 **bus owner**？  
3. EID 是誰分的？是否穩定？  
4. 上層傳的是 **PLDM / SPDM / vendor message** 哪一種？  
5. 問題是在 **transport 不通**，還是上層 payload decode/handler 有錯？

### 3.6 對你最有價值的認知

如果你以前是 Redfish 強，MCTP 最大思維轉換是：

- Redfish 解的是 **northbound management API**
- MCTP 解的是 **inside-the-box management transport**

兩者不是替代關係，是上下游關係。

---

## 4. PLDM essentials：真正會用到的核心

### 4.1 一句話定義

**PLDM = 跑在 MCTP 等 transport 上的平台管理訊息與資料模型。**

### 4.2 為什麼重要

PLDM 在 OpenBMC 特別重要，因為它更適合處理：

- 平台 inventory
- sensors / effecters
- FRU
- firmware update
- BIOS/config
- BMC 與 host / add-on device / satellite MC 之間的標準互動

### 4.3 你至少要熟的 PLDM Type

對 OpenBMC 工作最常碰到的，不用一開始全背，先抓這些：

- **Base**：基礎能力、type/command、版本、TID 等
- **Platform Monitoring and Control**：sensors / effecters / PDRs
- **FRU Data**：裝置 FRU / inventory 資料
- **Firmware Update**：FW update 流程
- **BIOS / config**：平台設定與 BIOS 相關模型

### 4.4 sensors 與 effecters 是關鍵差異

比起 IPMI 的 sensor 偏監控導向，PLDM 很重要的一點是：

- **sensor** = 觀測
- **effecter** = 控制

這讓 OpenBMC 在 host/device 管理模型上更自然，不用把一堆控制語意硬塞進 OEM 命令。

### 4.5 PDR（Platform Descriptor Records）為什麼重要

PDR 可以理解成：

- 平台元件、sensor、effecter、entity 的描述資料
- 讓 requester 知道有哪些東西可監控/控制
- 在多裝置、自描述裝置情境中很重要

你做 debug 時，若 PLDM 世界跟 D-Bus 世界對不上，PDR 常是關鍵切點。

### 4.6 在 OpenBMC 裡它出現在哪

PLDM 在 OpenBMC 常見角色：

- **BMC 當 requester**：去發 PLDM 命令給其他裝置
- **BMC 當 responder**：回應 host 或其他 requester 的 PLDM 命令
- `pldmd` / PLDM library 處理 encode/decode、message flow
- 把 PLDM 的 FRU/sensor/inventory/control 映射到 D-Bus 物件
- `bmcweb` 再從 D-Bus 往上翻成 Redfish

### 4.7 實務 debug checklist

若 PLDM 相關功能有問題，優先檢查：

1. MCTP transport 通不通  
2. endpoint / EID / discovery 是否正常  
3. requester/responder 角色有沒有搞反  
4. type / command / completion code 是否合理  
5. PDR / FRU record 內容是否正確  
6. D-Bus 映射是否成功  
7. Redfish 只是沒翻到，還是底層根本沒資料

---

## 5. Yocto：OpenBMC 工作真正必要的部分

你不需要先變成 Yocto 專家；先把**能動手改 OpenBMC**需要的部分補齊。

### 5.1 必懂的 8 件事

#### 1) Layer 結構

至少知道：
- `poky` / OE-Core 是基底
- OpenBMC 自己有 `meta-phosphor`、`meta-openbmc-machines` 等 layer
- vendor / board 會再疊 BSP layer、machine layer、product layer

你做事情時，先問：
**這個變更應該落在哪一層？**

#### 2) Recipe / bbappend

- `.bb`：定義怎麼抓 source、怎麼 build、裝哪些檔案
- `.bbappend`：對既有 recipe 疊 patch/config/install

OpenBMC 日常改動很多時候不是改 build system 本身，而是：
- patch 某 daemon
- 改 packageconfig
- 加 systemd unit
- 調 image install

#### 3) machine / distro / local.conf 的責任分界

- **machine**：板級/SoC/硬體差異
- **distro**：政策、套件、版本、整體預設
- **local.conf**：本地實驗，不應變成正式產品設定來源

#### 4) BitBake 基本操作

至少熟這幾個：
- `bitbake <target>`
- `bitbake -e <target>`：追變數來源
- `bitbake -c clean <target>` / `-c cleansstate`
- 看 task log / workdir / temp log

#### 5) devtool

當你要快速 patch 某元件時很好用：
- 拉 source 到 workspace
- 修改
- build / test
- 匯出 patch 回 recipe

#### 6) sstate 與 DL_DIR

CI 與本機效率最重要：
- **DL_DIR**：source 下載快取
- **sstate-cache**：task 輸出快取

不懂這兩個，你會被 build 時間折磨。

#### 7) image 組成

要知道 image 怎麼把服務放進去：
- 什麼 package 被 install
- 哪些 systemd service 被 enable
- 哪些 feature 被 distro / machine 打開

#### 8) patch 流

OpenBMC/Yocto 開發常見流程是：
- 改 upstream source 或 fork source
- 在 layer 用 patch / bbappend 套進來
- 用 bitbake 驗證

### 5.2 不用先深鑽的東西

第一週先不用太沉迷：

- 每個 class 細節
- SDK / extensible SDK 深層機制
- multiconfig 複雜玩法
- 特殊 package backend 細節
- 每個 task 的內部原理

### 5.3 OpenBMC 情境下最實用的 Yocto 心法

- **先知道 recipe 在哪，再談修改**
- **先用 `bitbake -e` 查變數覆蓋來源**
- **先分清是 source 問題、recipe 問題、image 組包問題、systemd enable 問題**
- **沒有共享 sstate / DL_DIR 的 CI，幾乎一定慢到失去耐心**

---

## 6. Jenkins / CI-CD：OpenBMC / Yocto 團隊真正需要的部分

### 6.1 先抓大原則

對 OpenBMC/Yocto pipeline，核心不是花俏 deploy，而是：

- **可重現 build 環境**
- **快取策略**
- **大 build 的資源隔離**
- **artifact/映像/測試結果留存**
- **分支與 patch 驗證自動化**

### 6.2 必懂主題

#### 1) Jenkinsfile / Pipeline as Code

這是基本盤：
- pipeline 應版本控管
- PR/branch 自動帶出一致流程
- build/test/release 行為可 review

#### 2) Declarative Pipeline

除非已有大量 Groovy 歷史包袱，通常先以 Declarative 為主，因為：
- 容易看
- 容易維護
- 比較適合跨團隊

#### 3) Shared Library

對多產品線或多板子很重要。可以把共用流程抽出：
- checkout
- cache mount
- kas/bitbake build
- artifact upload
- test stage
- log/archive/prune 規則

#### 4) Containerized build agent

Yocto/OpenBMC build 相依多、主機污染重，建議：
- 用固定 container image 當 agent
- 工具鏈版本固定
- 把 host 差異降到最低

#### 5) Kubernetes dynamic agents（若團隊規模值得）

如果 build 量大：
- Jenkins controller 不必自己扛所有 job
- 可用 k8s plugin 動態拉起 agent pod
- 每個 build 用完即丟
- 搭配 PVC / network storage 留 cache

#### 6) Yocto 快取策略

這是最關鍵的實戰點：

- 共用 `DL_DIR`
- 共用 `SSTATE_DIR` 或 sstate mirror
- 規劃 cache 清理策略
- 分清「可共享」與「會污染 reproducibility」的項目

#### 7) Artifact 管理

至少要留：
- image / tarball / manifest
- build logs
- test logs
- SBOM/版本資訊（若產品流程需要）
- 對應 git SHA / layer revision

### 6.3 一條夠用的 pipeline 心智模型

```text
checkout layers/source
 -> restore DL_DIR / sstate cache
 -> build container/pod startup
 -> kas/bitbake build target image
 -> unit/static checks (可選)
 -> boot/smoke test/QEMU or lab target (可選)
 -> archive image/logs/manifests
 -> publish result / notify / tag release (必要時)
```

### 6.4 你要特別注意的坑

- **沒有 cache**：每次 cold build，CI 成本爆炸
- **cache 沒治理**：舊 cache 汙染、磁碟爆滿、難重現
- **agent 不固定**：建置偶發失敗、環境飄移
- **artifact 不完整**：出問題無法追溯哪個 layer/commit 造成
- **共享 library 過度魔法化**：新人完全看不懂 pipeline 真正做什麼

### 6.5 Jenkins 在 OpenBMC 團隊的最低實用線

你不需要先會寫很炫的 Groovy；先能做到：

- 看懂 Jenkinsfile
- 看懂 agent / stage / sh / archive / post
- 知道 cache 在哪
- 知道 build target 怎麼定義
- 知道失敗時去哪拿 bitbake log、artifact、console output

---

## 7. 7 天衝刺計畫：目標是「快速能工作」

每天建議 2.5～4 小時。  
主軸是：**先建立定位能力，再補 protocol 與 build/CI 手感。**

### Day 1 — 建立全局圖

目標：知道 OpenBMC 各層在幹嘛，不迷路。

做法：
- 看 OpenBMC docs 的總覽與 interface overview
- 看 `bmcweb` repo README / 目錄
- 把「外部 API -> bmcweb -> D-Bus -> backend services」畫成自己的圖

產出：
- 自己寫一頁架構筆記
- 列出常見故障切點：API / D-Bus / daemon / transport

### Day 2 — Redfish refresh（只補 delta，不重學基礎）

目標：把 5 年的差異補回來。

做法：
- 快看 DMTF Redfish release page 與近年 overview
- 重點掃：Telemetry、EventService、CertificateService、UpdateService、Interop/Profile
- 對照以前熟悉的 model，標出新增重點

產出：
- 一張「以前 vs 現在」delta 清單
- 一張「OpenBMC 可能受影響的後端 mapping」清單

### Day 3 — D-Bus / bmcweb 實戰視角

目標：學會從 Redfish 往 D-Bus 倒查。

做法：
- 看 OpenBMC D-Bus / inventory / sensor 相關設計文件
- 看 `bmcweb` 內 Redfish route/mapping 的實際程式碼結構
- 嘗試理解 1~2 個資源（例如 Systems、Sensors/Log）的資料路徑

產出：
- 一張「某 Redfish resource 對到哪些 D-Bus 物件/服務」的對照表

### Day 4 — MCTP

目標：能跟做 host/device management 的人說同一種語言。

做法：
- 看 OpenBMC MCTP design doc
- 補 DMTF MCTP Base / binding 的名詞
- 理解 EID、bus owner、discovery、packet/message、routing

產出：
- 一頁 MCTP cheat sheet
- 一張 transport 問題的 debug flow

### Day 5 — PLDM

目標：知道 PLDM 如何進 OpenBMC 內部資料模型。

做法：
- 看 OpenBMC PLDM stack doc
- 補 Base / FRU / Platform Monitoring and Control / FW Update 的觀念
- 釐清 requester/responder 與 D-Bus 映射

產出：
- 一張「PLDM -> D-Bus -> Redfish」資料流圖
- 一份常見 type/record/debug 問題清單

### Day 6 — Yocto for OpenBMC

目標：不再怕 build system。

做法：
- 補 layer / recipe / bbappend / bitbake / devtool / sstate / DL_DIR
- 看 OpenBMC 相關 meta layer 結構
- 找 1 個實際 recipe，追到它如何進 image

產出：
- 一張 OpenBMC layer 地圖
- 一張「我如果要改某 service，要改哪裡」操作路徑

### Day 7 — Jenkins / CI-CD

目標：能看懂現有 pipeline，知道優先優化什麼。

做法：
- 看 Jenkins pipeline、shared library、k8s agent 官方文件
- 用 OpenBMC/Yocto 視角盤點：cache、container agent、artifact、測試切分
- 把你所在團隊或想像中的 pipeline 畫出來

產出：
- 一版最小可用 Jenkins pipeline 設計
- 一份 CI 改善優先級（cache > reproducibility > artifacts > test automation）

---

## 8. 如果只能用半天，該先學什麼？

優先順序：

1. **OpenBMC 架構圖：bmcweb / D-Bus / services / MCTP / PLDM**  
2. **Redfish 新增重點：Telemetry / Events / Cert / Update / Interop**  
3. **MCTP 與 PLDM 的角色分工**  
4. **Yocto layer + recipe + sstate/DL_DIR**  
5. **Jenkins pipeline + cache 基本盤**

---

## 9. 開始實際工作前，建議先能回答這 12 題

1. OpenBMC 內部資料主要靠什麼 IPC？  
2. `bmcweb` 在 OpenBMC 的角色是什麼？  
3. Redfish resource 出錯時，第一站要查哪？  
4. MCTP 解決的是 transport 還是 data model？  
5. PLDM 解決的是 transport 還是 platform management message/model？  
6. EID 是什麼？  
7. bus owner 在做什麼？  
8. PLDM requester 與 responder 差在哪？  
9. PDR 為什麼重要？  
10. Yocto 的 `.bb` 與 `.bbappend` 差在哪？  
11. `DL_DIR` 與 `sstate-cache` 差在哪？  
12. Yocto CI 最先該優化的是什麼？

如果你能順手回答以上問題，這週衝刺就已經足以讓你開始接 OpenBMC 相關工作。

---

## 10. 最後給有經驗工程師的直白建議

- **不要把 OpenBMC 當成單一韌體專案，要當成一套可組裝的 Linux 管理平台。**
- **不要從 Redfish API 表面停住，真正的 debug 能力來自 D-Bus 與後端服務定位。**
- **不要把 MCTP/PLDM 看成冷門協定；它們是 OpenBMC 對內管理演進的主戰場之一。**
- **Yocto 不需要先學滿，只要先學會找到層、recipe、cache、build log。**
- **CI/CD 先做可重現與快取，再談華麗自動化。**

這樣學，1 週內就能從「知道名詞」進到「能參與 debug / review / 設計討論」。
