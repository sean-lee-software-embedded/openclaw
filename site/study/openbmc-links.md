# OpenBMC 高價值官方連結清單

只放**高價值、官方、足夠支撐 1 週衝刺**的連結。  
用途不是蒐藏，而是讓你快速建立正確地圖。

---

## 1. OpenBMC 官方總覽

### OpenBMC docs repo / 文件入口
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/README.md
- 用途：先知道 OpenBMC 文件有哪些主題、常見開發與使用文件在哪

### OpenBMC interface overview
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/architecture/interface-overview.md
- 用途：快速理解 OpenBMC 對外/對內介面、network services、host-BMC 連線脈絡

### OpenBMC docs GitHub mirror
- https://github.com/openbmc/docs
- 用途：比較容易瀏覽與搜尋整體文件樹

---

## 2. bmcweb / Redfish in OpenBMC

### bmcweb repo
- https://github.com/openbmc/bmcweb
- 用途：OpenBMC 的 web server / Redfish 實作主體；看 route、schema mapping、auth、event 行為

### OpenBMC Redfish cheatsheet
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/REDFISH-cheatsheet.md
- 用途：快速喚回常用操作感覺

### OpenBMC REST API intro
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/rest-api.md
- 用途：理解非 Redfish 的 OpenBMC REST 介面背景

---

## 3. D-Bus / inventory / sensor 觀念

### D-Bus inventory architecture
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/architecture/dbus-inventory.md
- 用途：理解 inventory 如何在 D-Bus 表達與關聯

### Sensor architecture
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/architecture/sensor-architecture.md
- 用途：看 sensor 在 OpenBMC 內部是如何建模與發布

### ObjectMapper / D-Bus interfaces repo
- https://github.com/openbmc/phosphor-dbus-interfaces
- 用途：找 interface 定義；做 D-Bus <-> service 映射時很好用

---

## 4. MCTP / PLDM（OpenBMC 角度）

### OpenBMC MCTP design
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/designs/mctp/mctp.md
- 用途：理解 OpenBMC 為何導入 MCTP、transport 與 messaging 分離、userspace vs kernel 方向

### OpenBMC in-kernel MCTP design
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/designs/mctp/mctp-kernel.md
- 用途：看新設計偏好的 kernel/socket 方向

### OpenBMC PLDM stack design
- https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/designs/pldm-stack.md
- 用途：理解 requester/responder、PLDM 與 D-Bus 的映射、設計目標

### libmctp repo
- https://github.com/openbmc/libmctp
- 用途：補 userspace MCTP stack 觀念與實作線索

### OpenBMC PLDM repo
- https://github.com/openbmc/pldm
- 用途：看實際 PLDM daemon / library / 相關實作

---

## 5. DMTF 官方規格（只列最該看的）

### DMTF PMCI standards hub
- https://www.dmtf.org/standards/pmci
- 用途：MCTP / PLDM / SPDM 等 platform management communications 規格總入口

### DMTF Redfish standards hub
- https://www.dmtf.org/standards/redfish
- 用途：Redfish release、spec、schema、white paper、overview 總入口

### Redfish Developer Hub
- https://redfish.dmtf.org/
- 用途：開發者友善入口；找 schema、工具、教學比較方便

### Redfish Specification (DSP0266)
- https://www.dmtf.org/dsp/DSP0266
- 用途：協定層與服務行為主規格

### Redfish Data Model (DSP0268)
- https://www.dmtf.org/dsp/DSP0268
- 用途：schema / data model 主體

### MCTP Base Specification（從 PMCI 入口進）
- https://www.dmtf.org/standards/pmci
- 用途：補 EID、message/packet、binding 等核心觀念

### PLDM Base / FRU / Platform Monitoring and Control / FW Update（從 PMCI 入口進）
- https://www.dmtf.org/standards/pmci
- 用途：依需求補對應 Type 規格，先看 Base、FRU、Platform Monitoring、FW Update

---

## 6. Yocto：只抓 OpenBMC 真正需要的

### Yocto docs 入口
- https://docs.yoctoproject.org/
- 用途：官方總文件入口

### Yocto concepts
- https://docs.yoctoproject.org/overview-manual/concepts.html
- 用途：補 BitBake、recipe、class、config、layer、sstate 的整體概念

### Yocto devtool
- https://docs.yoctoproject.org/dev/dev-manual/devtool.html
- 用途：快速 patch / 修改 recipe / 匯出修改時很實用

### BitBake user manual
- https://docs.yoctoproject.org/bitbake/
- 用途：需要追 task、變數、override 行為時查

### OpenEmbedded Layer Index
- https://layers.openembedded.org/
- 用途：查 layer / recipe 來源與版本

---

## 7. OpenBMC / Yocto layer 與建置實作

### meta-phosphor
- https://github.com/openbmc/meta-phosphor
- 用途：OpenBMC 核心 layer，很多 recipe 會落在這

### openbmc 主 repo
- https://github.com/openbmc/openbmc
- 用途：看整體 layer 組成、機種設定、subtree 結構

### meta-openembedded
- https://github.com/openembedded/meta-openembedded
- 用途：很多 OpenBMC recipe 依賴會從這裡來

### poky
- https://github.com/yoctoproject/poky
- 用途：Yocto 基底發行版與 OE-Core 入口

---

## 8. Jenkins / CI-CD 官方文件

### Jenkins Pipeline
- https://www.jenkins.io/doc/book/pipeline/
- 用途：Jenkinsfile、Declarative/Scripted、best practices

### Jenkins Shared Libraries
- https://www.jenkins.io/doc/book/pipeline/shared-libraries/
- 用途：多平台/多產品線共用 pipeline 邏輯

### Jenkins Kubernetes plugin
- https://plugins.jenkins.io/kubernetes/
- 用途：動態 agent pod；Yocto 大 build 很常見

### Jenkins on Kubernetes
- https://www.jenkins.io/doc/book/installing/kubernetes/
- 用途：若 CI 基礎設施走 k8s，可看部署與運作模式

---

## 9. 這 1 週建議閱讀順序

### 第 1 層：先建立地圖
1. OpenBMC README  
2. interface overview  
3. bmcweb repo  
4. DMTF Redfish hub

### 第 2 層：補 inside-the-box protocol
5. MCTP design  
6. PLDM stack design  
7. PMCI standards hub

### 第 3 層：補 build / CI
8. Yocto concepts  
9. Yocto devtool  
10. Jenkins Pipeline  
11. Shared Libraries  
12. Kubernetes plugin

---

## 10. 如果只留 8 個連結

1. OpenBMC interface overview  
   https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/architecture/interface-overview.md

2. bmcweb repo  
   https://github.com/openbmc/bmcweb

3. D-Bus interfaces repo  
   https://github.com/openbmc/phosphor-dbus-interfaces

4. OpenBMC MCTP design  
   https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/designs/mctp/mctp.md

5. OpenBMC PLDM stack design  
   https://gerrit.openbmc.org/plugins/gitiles/openbmc/docs/+/master/designs/pldm-stack.md

6. DMTF Redfish hub  
   https://www.dmtf.org/standards/redfish

7. Yocto concepts  
   https://docs.yoctoproject.org/overview-manual/concepts.html

8. Jenkins Pipeline  
   https://www.jenkins.io/doc/book/pipeline/
