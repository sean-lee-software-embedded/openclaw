# AI / 雲端伺服器術語作弊單

## 30 秒總結
- **Hopper / Blackwell / Rubin**：NVIDIA 三個連續世代
- **H100 / H200 / B200 / GB200 / GB300**：晶片 / superchip 產品名
- **HGX / DGX / MGX / NVL72**：平台 / 系統 / 架構名
- **NVLink / NVSwitch**：櫃內多 GPU 高速互連
- **InfiniBand / Spectrum-X Ethernet**：櫃外叢集網路
- **HBM3e / CoWoS**：AI 晶片性能與出貨能力的兩個關鍵上游詞
- **液冷 / rack-scale / cost per token**：現在 AI server 討論最常見的三大現場詞

---

## 一、名詞速配

### 世代
- **Hopper**：上一代主力
- **Blackwell**：目前主戰場
- **Rubin**：下一代，強調 reasoning / rack-scale / AI factory

### GPU / Superchip
- **H100**：Hopper 主力 GPU
- **H200**：Hopper + HBM3e 大記憶體版
- **B200**：Blackwell GPU
- **GB200**：Grace CPU + 2x Blackwell GPU 的 superchip
- **GB300**：Blackwell Ultra 強化版

### 平台 / 系統
- **HGX**：多 GPU 高階平台底座
- **DGX**：NVIDIA 自家完整 AI 系統 / 平台
- **MGX**：給 OEM / ODM 的模組化參考架構
- **NVL72**：72 GPU 的 rack-scale NVLink domain

---

## 二、一句話定義

### H100
Hopper 時代的代表作，讓大型 AI 訓練與推論真正成為資料中心主流。

### H200
H100 的記憶體強化版，最大賣點是 **HBM3e、容量更大、頻寬更高**。

### B200
Blackwell 家族核心 GPU，是新一代 AI factory 的主要算力元件。

### GB200
不是單純 GPU 卡，而是 **Grace CPU + Blackwell GPU 的緊耦合運算模組**。

### GB300
Blackwell Ultra 路線，通常代表更高推論效能與更大記憶體資源。

### HGX
NVIDIA 高階多 GPU 平台底座，很多 OEM / ODM 整機都建立在 HGX 上。

### DGX
NVIDIA 自己包好的整體 AI 解決方案，重點是硬體 + 軟體 + 支援服務。

### MGX
NVIDIA 的模組化 server 參考架構，讓夥伴更快做出不同型號。

### NVL72
72 顆 GPU 的整櫃系統形態，是 rack-scale AI system 的代表詞。

---

## 三、網路 / 互連別再混

### NVLink
GPU 與 GPU 之間的高速互連，偏 **scale-up**。

### NVSwitch
讓多顆 GPU 可以高頻寬、低延遲、近似全互連地交換資料。

### InfiniBand
大型 HPC / AI 訓練叢集常用高效能網路，偏極致性能。

### Spectrum-X
NVIDIA 主打的 **AI Ethernet 平台**，目標是讓 Ethernet 也能更適合 AI cloud。

### ConnectX
高效能 NIC / SuperNIC 家族，負責把節點高速接上網路。

### BlueField
DPU。負責網路 / 安全 / storage / infrastructure offload，不是主算力 GPU。

---

## 四、你開會最需要懂的差異

### NVLink / NVSwitch vs InfiniBand / Ethernet
- **NVLink / NVSwitch**：櫃內、節點內，多 GPU 串成大系統
- **InfiniBand / Ethernet**：櫃外、跨節點，把多櫃串成大叢集

### HGX vs DGX vs MGX
- **HGX**：平台底座
- **DGX**：NVIDIA 完整成品 / 解法
- **MGX**：模組化參考設計

### B200 vs GB200
- **B200**：GPU
- **GB200**：CPU + GPU superchip / building block

---

## 五、供應鏈與商業角色

### NVIDIA
定義 GPU、CPU、互連、reference architecture、軟體堆疊與整體平台語言。

### ODM（例：Compal）
把平台做成可量產、可部署、可維修的實際系統；很強調設計整合、NPI、成本、液冷與機構量產能力。

### OEM（例：Dell）
把系統包成品牌化、企業可採購的完整方案，重點是售前售後、認證、服務、support、整合導入。

### CSP
雲服務商 / hyperscaler。是超大買家，也是需求定義者，特別關心 cost per token、功耗、部署速度、多租戶與網路效率。

---

## 六、上游關鍵詞

### HBM3e
新一代高頻寬記憶體。對 AI GPU 很關鍵，因為大模型很吃記憶體頻寬與容量。

### CoWoS
先進封裝技術。AI GPU + HBM 的量產瓶頸常會跟它有關。

---

## 七、為什麼現在一直在講液冷與 rack-scale？

因為 AI 櫃功率密度越來越高，風冷越來越難撐。

### 你要抓的關鍵字
- liquid cooling
- cold plate
- CDU
- manifold
- quick disconnect
- rack power
- serviceability

### 白話翻譯
供應商不是只在賣一台伺服器，而是在賣「整櫃能長期運作的 AI 基礎設施」。

---

## 八、最近新聞最常用的 10 個詞

1. AI factory
2. rack-scale
3. NVL72
4. cost per token
5. liquid-cooled rack
6. HBM3e
7. CoWoS
8. Spectrum-X
9. BlueField
10. reasoning / agentic AI

---

## 九、實戰翻譯：聽到這句時代表什麼？

### 「我們支援 GB200 NVL72」
代表你不只做 server node，而是有能力碰整櫃級 AI 系統。

### 「我們導入 MGX 以縮短上市時間」
代表你在用 NVIDIA 模組化參考架構加快開發與跨代轉換。

### 「我們聚焦 AI factory」
代表你想賣的不只是硬體，而是整體基礎設施與運營敘事。

### 「我們提供 Spectrum-X Ethernet 解決方案」
代表你想切進 CSP / AI cloud 的 Ethernet 路線。

### 「我們強調 cost per token」
代表討論焦點已從訓練峰值性能，轉向商業化推論效率。

---

## 十、最小必背清單

如果只背 12 個詞，背這些：
- Hopper
- Blackwell
- Rubin
- H100
- H200
- B200
- GB200
- HGX
- DGX
- MGX
- NVLink
- Spectrum-X

如果再加 5 個：
- NVSwitch
- NVL72
- BlueField
- HBM3e
- CoWoS

---

## 十一、真正該記住的一句話

> 現在 AI / 雲端伺服器的主戰場，已從單機規格，轉向整櫃系統、網路互連、液冷供電、以及可量產供應鏈能力。

---

## 參考來源
- NVIDIA GB200 NVL72
- NVIDIA Blackwell Architecture
- NVIDIA H100 / H200
- NVIDIA HGX / DGX / MGX
- NVIDIA Spectrum-X
- NVIDIA Rubin platform
- NVIDIA NVLink / NVSwitch 技術文章
