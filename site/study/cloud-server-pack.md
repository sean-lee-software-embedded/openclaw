# 雲端伺服器 / AI 伺服器速讀包

> 目標：讓已有嵌入式 / 伺服器背景的人，在看新聞、開供應商會議、聽 NVIDIA / Dell / ODM 簡報時，能快速聽懂 80% 以上的術語。

## 1. 先抓大圖：現在 AI 伺服器在講什麼？

過去雲端伺服器多半以 **CPU server** 為中心；現在高成長段幾乎都在 **AI server / AI factory**。
關鍵變化不是只有「GPU 變快」，而是整個系統設計單位從 **單機** 變成 **整櫃、整叢集、整資料中心 fabric**。

現在業界最常談的 6 個軸：

1. **算力密度**：每機、每櫃、每 MW 可塞多少 AI 算力
2. **記憶體容量 / 頻寬**：尤其 HBM3e / 未來 HBM4
3. **互連**：GPU 內部 scale-up（NVLink / NVSwitch）+ 櫃外 scale-out（InfiniBand / Ethernet）
4. **散熱與供電**：高功耗推動液冷、rack power redesign、busbar / 高壓直流等討論
5. **可量產性**：CoWoS、HBM、NIC、switch、冷板、CDU、機櫃供應鏈是否跟得上
6. **商業角色分工**：NVIDIA 定平台，ODM/OEM 做系統，CSP / enterprise 買整體方案

一句話總結：

> **AI 伺服器競爭，已經不是單顆 GPU 規格戰，而是「整個 rack-scale 平台 + 網路 + 散熱 + 供電 + 供應鏈」戰。**

---

## 2. NVIDIA 命名先搞懂：世代、晶片、平台、系統

很多人第一次聽會混在一起。建議這樣拆：

### A. 世代（architecture / platform generation）
- **Hopper**：前一代主力
- **Blackwell**：目前主戰場
- **Rubin**：下一代，重點更偏向 agentic AI / reasoning / rack-scale co-design

### B. 單顆 GPU / superchip 名稱
- **H100**：Hopper 世代主力 AI GPU
- **H200**：Hopper 的記憶體強化版，導入 **HBM3e**
- **B200**：Blackwell GPU
- **GB200**：**Grace CPU + 2 顆 Blackwell GPU** 的 superchip / 模組概念
- **GB300**：Blackwell Ultra 世代，通常可理解成 GB200 的強化進階版

### C. 板級 / 平台 / 系統名稱
- **HGX**：NVIDIA 的高階 GPU baseboard / scale-up 平台，常見 8-GPU
- **DGX**：NVIDIA 自家整機 / 整體解決方案品牌
- **MGX**：模組化伺服器參考架構，給 OEM / ODM 快速做多種型號
- **NVL72**：72-GPU 的 rack-scale NVLink domain 命名

### D. 網路 / 互連 / 基礎設施名詞
- **NVLink**：GPU 間高速互連（偏 scale-up）
- **NVSwitch**：讓多 GPU 全互連、低延遲的交換晶片
- **Spectrum-X**：NVIDIA 的 AI Ethernet 平台
- **Quantum / InfiniBand**：NVIDIA 在 HPC / AI scale-out 常見的高效能網路
- **BlueField**：DPU / infrastructure offload
- **ConnectX**：NIC / SuperNIC 家族

最實用的理解法：

> **H100 / H200 / B200 / GB200 / GB300 是算力元件名；HGX / DGX / MGX / NVL72 是系統或平台名。**

---

## 3. 三代產品線怎麼記

## Hopper：H100 / H200

### H100
- Hopper 世代代表作
- 重點：讓大型 AI training / inference 正式全面進入資料中心主流
- 關鍵詞：**Transformer Engine、FP8、NVLink 4、HGX H100、DGX H100**
- 你在新聞裡看到「H100 shortage」「H100 cluster」基本都指這一代

### H200
- 本質上仍屬 Hopper 家族
- 最大賣點不是重做整個架構，而是 **HBM3e + 更大容量 / 更高頻寬記憶體**
- 對 LLM inference、記憶體吃重工作負載更有感
- 常見說法：**H200 是 Hopper 補足記憶體瓶頸的版本**

**一句話記憶：**
H100 是 Hopper 主戰機，H200 是同代的「大記憶體強化版」。

---

## 4. Blackwell：B200 / GB200 / GB300 為什麼那麼常被提？

## B200
- Blackwell 核心 GPU
- NVIDIA 官方定位是新一代 AI factory engine
- 重點不是只看單卡，而是看它如何進入 **HGX B200**、**GB200 NVL72** 這類系統
- 特徵：更高 AI throughput、FP4 / 新 Transformer Engine、更高整體效率

## GB200
- **Grace + Blackwell** 的 CPU-GPU 緊耦合設計
- 核心概念是：CPU 與 GPU 不只是 PCIe 接起來，而是透過 **NVLink-C2C** 做高頻寬 coherent / 緊密互連
- 比較像一個「AI superchip building block」

## GB200 NVL72
這是近一年最重要的名詞之一。

它代表：
- 36 顆 Grace CPU
- 72 顆 Blackwell GPU
- 一整個液冷機櫃
- 72-GPU 的 NVLink domain
- NVIDIA 說法是可視為單一巨型 GPU 域來運作

這個名詞重要，因為它標誌著：

> **討論單位從 server node，升級成 rack-scale AI system。**

供應商若說「我們支援 GB200 NVL72」，其實不只是說能裝 GPU，通常也暗示：
- 機櫃機構設計
- 液冷能力
- 高功率配電
- 背板 / 纜線 / serviceability
- 網路與交換拓樸
都要跟上。

## GB300 / Blackwell Ultra
- 可理解成 Blackwell 平台再往上推的強化版
- 重點通常在：更多記憶體、更高推論效能、面向更大模型與更高 token throughput
- 開會時若聽到 **GB300 NVL72**，直覺就是：
  - 同樣是 rack-scale NVL72 類架構
  - 但屬於 Blackwell Ultra 升級版
  - 訴求是更高效率、更大模型、更高輸出吞吐

**一句話記憶：**
- **B200**：Blackwell GPU
- **GB200**：Grace + Blackwell superchip
- **GB200 NVL72**：72 GPU 整櫃系統
- **GB300**：Blackwell Ultra 進階版

---

## 5. Rubin：為什麼大家已經開始談？

Rubin 是 Blackwell 之後的下一代平台。

現在談 Rubin，不一定表示量產馬上到位，而是因為大客戶 / ODM / 零組件供應鏈都會提早一年以上規劃。

Rubin 的關鍵訊號：
- NVIDIA 強調 **reasoning / agentic AI / long-context**
- 強調 **data center is the unit of compute**
- 更明確往 **rack-scale co-design** 走
- 更高代際的 **NVLink / Switch / networking / security / power / cooling** 一起設計

如果 Blackwell 是把「AI rack」變成主角，
那 Rubin 更像是把「AI factory」變成真正的產品化單位。

開會時聽到 Rubin，通常代表對方想傳達：
1. 不只賣 GPU，而是賣下一代整體平台敘事
2. 客戶規劃已經從 8-GPU server 跳到 rack / pod / fabric 層級
3. 供應鏈要開始考慮 HBM4、下一代 NIC / switch、功耗與液冷升級

---

## 6. HGX / DGX / MGX / NVL72 到底差在哪？

## HGX
可以把 HGX 理解成：

> **NVIDIA 高階多 GPU 伺服器核心平台 / baseboard 標準。**

它通常整合：
- 多顆 NVIDIA GPU
- NVLink / NVSwitch
- 搭配指定的網路與軟體堆疊

你常看到的：
- HGX H100
- HGX H200
- HGX B200

這通常不是終端品牌機，而是供 OEM / ODM 拿來做整機的重要基礎。

## DGX
DGX 是 NVIDIA 自家品牌整體方案，重點是：
- NVIDIA 幫你把硬體、軟體、管理、部署方法都打包
- 常被視為 **enterprise / research / AI factory** 的高端標準解

簡單講：
- **HGX 比較像平台底座**
- **DGX 比較像 NVIDIA 親自交付的完整成品 / 解決方案**

## MGX
MGX 是非常值得懂的名詞。

它不是某一台機器，而是：

> **NVIDIA 推給 OEM / ODM 的模組化參考架構。**

價值在於：
- 加快產品開發
- 降低重複設計成本
- 支援多種 CPU / GPU / 網路 / 機構組合
- 讓同一生態系更快切換到新世代 GPU

MGX 跟供應鏈關係很深，因為它直接碰到：
- 機構件
- 散熱模組
- 電源架構
- 連接器 / 線纜
- 板卡布局
- rack integration

## NVL72
NVL72 不是單顆晶片，也不是一般 2U/4U 伺服器。
它代表 **72 顆 GPU 的 NVLink 網域 rack-scale system**。

你可以把它視為：
- system topology 名稱
- rack SKU 類別
- NVIDIA 對「整櫃 AI 算力單元」的品牌化命名

**一句話分辨：**
- **HGX**：高階 GPU 平台底座
- **DGX**：NVIDIA 整機 / 整體方案
- **MGX**：模組化參考架構
- **NVL72**：72-GPU rack-scale 系統形態

---

## 7. NVLink / NVSwitch / InfiniBand / Spectrum-X：一定要會分

這是會議裡最容易混掉的地方。

## NVLink
- 用來做 **GPU 與 GPU 之間的高速互連**
- 偏向 **scale-up**：讓同一台或同一個緊密系統裡的多 GPU 像一個更大系統
- 核心目標：降低多 GPU 溝通成本，避免 Tensor Core 在等資料

對 LLM 很重要，因為 tensor parallel / expert parallel 都很吃 GPU 間同步。

## NVSwitch
- 不是線，而是交換晶片
- 作用是讓多 GPU **非阻塞、高頻寬地彼此互通**
- 沒有 NVSwitch，多 GPU 可能退化成點對點拓樸，all-to-all 通訊效率差很多

白話講：
- **NVLink 是高速道路**
- **NVSwitch 是大型交流道 / 交換中樞**

## InfiniBand
- 傳統 HPC / 大型 AI cluster 常用的高效能網路
- 優勢是低延遲、高效能 collective、成熟的超算 / AI 訓練生態
- 通常偏高階、大型訓練叢集、極致性能導向

## Spectrum-X
- NVIDIA 主打的 **AI Ethernet 平台**
- 用標準乙太網路路線，但透過 switch + SuperNIC + 軟體優化，讓 AI traffic 跑得更像 AI fabric
- 對 hyperscaler / cloud 重要，因為很多 CSP 更偏好 Ethernet 生態、操作與成本模型

**最實用結論：**
- **NVLink / NVSwitch**：櫃內 / 節點內 / scale-up 核心
- **InfiniBand / Ethernet (Spectrum-X)**：櫃與櫃之間 / cluster scale-out 核心

如果一個供應商說自己「同時支援 NVLink + InfiniBand / Spectrum-X」，意思通常是：

> 櫃內高密度 GPU scale-up + 櫃外大型叢集 scale-out 都有對應方案。

---

## 8. BlueField / ConnectX 是什麼角色？

## ConnectX
- 傳統上可理解成 NVIDIA / Mellanox 的高效能 NIC 家族
- 在 AI server 裡就是負責把主機 / GPU cluster 接上高速網路
- 新一代常會提到 **ConnectX-8 / SuperNIC / 800GbE** 等字眼

## BlueField
- 是 **DPU**，不只是網卡
- 把部分基礎設施功能從 CPU 卸載出去：
  - 網路處理
  - 安全 / isolation
  - storage / data path
  - virtualization / multi-tenancy
- 在 hyperscale / cloud 環境特別重要

白話區分：
- **ConnectX**：偏高效能 NIC / 網路介面角色
- **BlueField**：偏 infrastructure offload / DPU / 雲端平台角色

開會時若提到 BlueField，多半不是在談 AI 算力本身，而是在談：
- 雲端多租戶
- 安全隔離
- 資料面卸載
- composable infrastructure

---

## 9. HBM3e、CoWoS 為什麼是供應鏈熱詞？

## HBM3e
- High Bandwidth Memory 的新一代版本
- 特色：超高記憶體頻寬、靠近 GPU/AI accelerator 封裝
- AI 訓練與推論非常吃記憶體頻寬，所以 HBM 是核心資源
- H200、Blackwell、GB300 類話題常常會一起帶到 HBM3e

**會議上聽到 HBM，多半代表：不是在聊 DRAM 成本，而是在聊 AI 加速器能不能把資料餵飽。**

## CoWoS
- TSMC 的先進封裝技術（Chip-on-Wafer-on-Substrate）
- AI GPU 常把大晶片與 HBM 用先進封裝整合
- 近兩年 CoWoS 會常被當作產能瓶頸代名詞

市場上講「AI server 需求旺」，很多時候真正限制出貨的不是機殼，而是：
- CoWoS 產能
- HBM 供應
- 網路晶片 / 光模組
- 液冷零組件

所以你在產業新聞裡看到「CoWoS 擴產」，其實是 AI 供應鏈的 upstream 關鍵訊號。

---

## 10. Rack-scale / liquid cooling / power delivery：為什麼突然變成主角？

## Rack-scale
傳統伺服器習慣以 1U / 2U / 4U 單機為中心。
AI 伺服器到了 GB200 / NVL72 / Rubin 這類平台後，系統設計重心變成：
- 機櫃整體熱設計
- 機櫃配電
- 線材與 service loop
- rack 內交換 / backplane / manifold
- 維修方式與部署節奏

也就是：

> **現在賣的不只是 server，而是整櫃可運作的 AI system。**

## Liquid cooling
高密度 AI 櫃功耗太高，風冷開始面臨：
- 噪音 / 風阻 / 散熱極限
- 機房空調成本高
- 機櫃功率密度無法再往上堆

因此液冷迅速變主流議題，尤其是：
- direct-to-chip 冷板
- CDU（coolant distribution unit）
- manifold / quick disconnect
- 漏液風險 / 維運 SOP
- facility 端供回水條件

你若在供應商簡報看到「liquid-ready」和「liquid-cooled」，要分清楚：
- **liquid-ready**：預留或可支援，不等於現在就是液冷量產櫃
- **liquid-cooled**：系統本身就是以液冷為主設計

## Power delivery
AI 櫃上升到極高功率後，大家開始談：
- 更高櫃功率密度
- busbar / power shelf / battery integration
- AC 到 DC 轉換效率
- 甚至 800VDC 等新配電討論

這是因為 AI 工廠拼的不只是晶片，也拼：
- 你機房供電能不能跟上
- PDU / PSU / backup 架構能不能撐
- 整體 PUE 與 TCO 能不能合理

---

## 11. Dell / Compal / ODM / OEM / CSP 在生態裡怎麼分工？

這一段超重要，因為你跟不同公司開會，說法會差很多。

## NVIDIA
- 定義 GPU、CPU、interconnect、reference architecture、軟體堆疊
- 近年更進一步主導「整個 AI factory platform」敘事
- 不只是賣 chip，而是在定整個系統規格語言

## ODM
ODM（Original Design Manufacturer）是實際把系統設計 / 製造做出來的主力。
在 AI server 時代，ODM 角色更重要，因為系統複雜度大幅提高。

ODM 常做：
- 主機板 / baseboard / 機構整合
- 熱設計與液冷整合
- power shelf / cable / rack integration
- 製造導入與量產
- 有時直接供貨給 CSP（白牌 / 準白牌）

**Compal（仁寶）** 這類公司就可放在 ODM 角色理解。
在 AI 伺服器生態裡，ODM 的價值不是代工而已，而是：

> **把 NVIDIA 參考平台變成可量產、可維修、可部署的實際產品。**

## OEM
OEM（Original Equipment Manufacturer）像 Dell、HPE、Lenovo、Supermicro 這類，通常是：
- 用自己的品牌賣企業客戶
- 提供售前 / 售後 / 認證 / 導入 / 服務
- 把系統整合成企業可買、可運行、可保固的解決方案

### Dell 的位置
Dell 的強項不是自己定義 GPU，而是：
- 把 NVIDIA 平台包成 **enterprise 可採購、可維運、可分期導入** 的方案
- 常以「AI Factory with NVIDIA」這類方式呈現
- 對企業客戶，Dell 賣的是：
  - 伺服器
  - 儲存
  - 網路
  - 管理
  - 服務 / 顧問 / support
  - 與既有 IT 架構接軌

所以 Dell 在生態中的角色可理解為：

> **把 NVIDIA 技術平台，產品化成企業可落地的 AI 基礎建設方案。**

## CSP
CSP（Cloud Service Provider）像 AWS、Microsoft Azure、Google Cloud、Oracle Cloud，或更廣義 hyperscaler / neo-cloud。

CSP 在生態裡通常是：
- 最大買家之一
- 對成本、功耗、供貨、網路拓樸有最強議價能力
- 很多會直接跟 ODM 合作做客製化白牌系統
- 對 Ethernet、可維運性、多租戶、安全隔離特別敏感

如果是 CSP 視角，重點常是：
- 每 token 成本
- 每 MW 產出
- 叢集運行效率
- 網路壅塞控制
- 部署速度與失效率

## 一張圖記住
- **NVIDIA**：定平台與核心技術語言
- **ODM（如 Compal）**：把平台做成可量產系統
- **OEM（如 Dell）**：把系統包成品牌解決方案賣給企業
- **CSP**：大量採購 / 自建雲端 AI 服務，常直接影響產品方向

---

## 12. 目前市場最值得關注的趨勢

## 趨勢 1：AI server 從「GPU 盒子」變成「AI factory」
你會越來越常聽到 AI factory，不只是 marketing。
它代表：
- 資料中心本身變成生產 intelligence 的工廠
- 重點是持續輸出 token / inference / training throughput
- 評估單位從單卡 TFLOPS 變成整體 TCO 與 utilization

## 趨勢 2：推論（inference）的重要性快速上升
以前市場話題常以 training 為中心，現在很多投資開始轉向：
- 大模型推論吞吐
- token latency
- 每 token 成本
- reasoning model 長上下文負載

這也是為什麼 NVIDIA 現在強調：
- FP4 / FP8
- NVLink / NVSwitch
- rack-scale inference
- cost per token

## 趨勢 3：網路從配角變主角
大規模 AI cluster 的瓶頸常不是單卡，而是：
- all-reduce / all-to-all 通訊
- 擴展效率
- 壅塞控制
- NIC / switch / optical power

因此 networking 現在已經不是附屬品，而是平台核心。

## 趨勢 4：Ethernet 在 AI cloud 的份量變重
InfiniBand 仍很強，但大量雲端業者偏好 Ethernet。
Spectrum-X 這種產品，反映 NVIDIA 正在搶 AI Ethernet 話語權。

## 趨勢 5：供應鏈瓶頸往上游與機房基礎設施延伸
不只 GPU 缺，還可能缺：
- HBM
- CoWoS
- 高速 NIC / switch / optics
- 液冷零件
- 機房電力與冷卻能力

## 趨勢 6：OEM / ODM 都在往 rack integration 走
只會做單機已不夠。
未來勝負更像是：
- 誰能快速交付整櫃
- 誰能做好液冷整合
- 誰能把維修與部署 SOP 標準化
- 誰能跨世代沿用設計、縮短 NPI 週期

---

## 13. 會議 / 新聞 / vendor conversation 最常出現的關鍵句型

### 句型 1：
「我們支援 HGX B200 / GB200 路線圖。」

翻譯：
我們已經跟上 NVIDIA 新世代高階平台，至少在產品規劃上沒有掉隊。

### 句型 2：
「我們提供液冷 rack-scale solution。」

翻譯：
我們不只賣伺服器本體，也在搶整櫃 AI 基礎設施案子。

### 句型 3：
「我們支援 Spectrum-X / 800G networking。」

翻譯：
我們想證明自己不只懂算力節點，也懂 AI cluster networking。

### 句型 4：
「我們採用 MGX 以縮短 time-to-market。」

翻譯：
我們用 NVIDIA 模組化參考架構降低開發成本，趕快切進新平台。

### 句型 5：
「我們聚焦 token throughput / cost per token。」

翻譯：
討論重心從 training benchmark 轉向商業化推論效率。

### 句型 6：
「rack is the new server」或「data center is the unit of compute」

翻譯：
單機思維已不夠，要從整個機櫃 / fabric / facility 一起設計。

---

## 14. 建議你優先熟的術語優先序

如果時間有限，先熟這 15 個：

1. Hopper
2. Blackwell
3. Rubin
4. H100
5. H200
6. B200
7. GB200
8. GB300
9. HGX
10. DGX
11. MGX
12. NVLink
13. NVSwitch
14. Spectrum-X
15. HBM3e / CoWoS

第二層再補：
- BlueField
- ConnectX
- NVL72
- rack-scale
- liquid cooling
- cost per token
- AI factory

---

## 15. 你可以怎麼快速判讀一家公司的定位

### 如果它一直講：
- NVLink domain
- rack power
- manifold
- CDU
- serviceability

=> 它多半是在打 **rack integration / thermal / infrastructure** 能力。

### 如果它一直講：
- MGX
- time-to-market
- multiple configurations
- x86 + Grace + networking flexibility

=> 它多半是在打 **模組化平台設計 / ODM-OEM 快速開案能力**。

### 如果它一直講：
- AI factory with NVIDIA
- end-to-end solution
- enterprise deployment
- services / support

=> 它多半是在打 **OEM / enterprise solution** 故事，像 Dell 路線。

### 如果它一直講：
- multi-tenant AI cloud
- Ethernet
- isolation
- DPU
- orchestration

=> 它更接近 **CSP / cloud infrastructure** 敘事。

---

## 16. 最後濃縮版

### 你真正要記住的事

1. **Hopper → Blackwell → Rubin** 是代際主線
2. **H100 / H200 / B200 / GB200 / GB300** 是產品名，不要和 HGX / DGX / MGX 混
3. **HGX 是平台底座，DGX 是整體解，MGX 是模組化參考架構，NVL72 是 72-GPU 整櫃形態**
4. **NVLink / NVSwitch 管櫃內 scale-up；InfiniBand / Spectrum-X 管櫃外 scale-out**
5. **HBM3e、CoWoS、液冷、供電** 是 AI server 量產成敗關鍵
6. **ODM 做量產系統、OEM 做品牌解決方案、CSP 決定大量需求方向**
7. 現在業界真正關注的是 **每 token 成本、整櫃效率、網路效率、機房可部署性**，不只是單卡跑分

---

## 參考來源（優先採官方 / 高價值來源）

### NVIDIA 官方
- GB200 NVL72: https://www.nvidia.com/en-us/data-center/gb200-nvl72/
- Blackwell Architecture: https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/
- H100: https://www.nvidia.com/en-us/data-center/h100/
- H200: https://www.nvidia.com/en-us/data-center/h200/
- HGX: https://www.nvidia.com/en-us/data-center/hgx/
- DGX Platform: https://www.nvidia.com/en-us/data-center/dgx-platform/
- MGX: https://www.nvidia.com/en-us/data-center/products/mgx/
- Spectrum-X: https://www.nvidia.com/en-us/networking/spectrumx/
- Rubin: https://www.nvidia.com/en-us/data-center/technologies/rubin/
- NVLink / NVSwitch 技術文章: https://developer.nvidia.com/blog/nvidia-nvlink-and-nvidia-nvswitch-supercharge-large-language-model-inference/
- Rubin 技術文章: https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/

### 產業 / 生態補充
- Dell AI 敘事（官方入口可能因區域導向變動，關鍵字：AI Factory with NVIDIA）
- TSMC CoWoS（官方技術頁常有反爬或區域限制；若需可再另整理）

> 備註：本筆記刻意以「會議可用、新聞可讀、術語可拆」為主，不追求每項規格最完整表格。若要下一步，可再延伸做一版「供應鏈公司對照表」與「AI server BOM / 子系統地圖」。
