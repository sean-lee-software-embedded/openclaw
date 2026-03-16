# iPhone 安全存取 OpenClaw Dashboard 路線評估

## 現況
目前 OpenClaw gateway 廣播的是：`ws://192.168.1.101:18789`（`gateway.bind=lan`）。
這條路線在桌機同網段可用，但 **iPhone 上的控制 / dashboard UI 不適合走純 LAN HTTP**，因為它會碰到 **secure context、裝置身分與瀏覽器限制**，所以常見現象就是：頁面能開、但控制功能不穩或直接失效。

## 各方案比較

### 1) Tailscale（推薦）
**適合：** 要讓 iPhone 安全登入自己的 OpenClaw 控制介面，且不想直接把管理介面公開到網際網路。

**優點**
- 走加密通道，iPhone 與主機有明確裝置身分
- 不需要自己維護公開 HTTPS 反向代理
- 不必暴露管理介面到公網
- 對 OpenClaw 這種「管理 / 控制面」最實際

**缺點**
- iPhone 與 Mac 都要裝 Tailscale，且登入同一 tailnet
- 第一次設定比 LAN 多一點步驟

**結論**
- 這是目前最實用、最安全、維護成本最低的方案

---

### 2) HTTPS Reverse Proxy（次選）
**適合：** 想用 Safari 直接走正式 HTTPS 網址，例如 `https://openclaw.example.com`。

**優點**
- 瀏覽器相容性最好，符合 secure context
- 不限同一個 LAN，可遠端使用

**缺點**
- 要處理網域、TLS 憑證、反向代理、WebSocket、存取保護
- 如果配置不嚴謹，等於把管理介面暴露到公網
- 維護成本比 Tailscale 高很多

**結論**
- 技術上可行，但對目前這個 setup 不是最短路
- 除非你明確需要「任何地方都能用 Safari 直接打公開網址」

---

### 3) localhost-only
**適合：** 只在主機本機管理 OpenClaw。

**優點**
- 最安全，完全不對外
- 最不容易踩到瀏覽器與網路暴露問題

**缺點**
- iPhone 幾乎不能直接用
- 只能在同一台 Mac 上操作

**結論**
- 安全，但不符合「iPhone dashboard access」需求

---

### 4) LAN HTTP
**適合：** 只做非常暫時、非常受限的內網測試。

**優點**
- 最快，不用多裝東西

**缺點**
- iPhone/Safari 對非 HTTPS secure context 有限制
- 控制 UI / 裝置身分 / Web 功能容易不穩
- 同網段任何人理論上都更容易碰到這個管理入口

**結論**
- **不建議當正式方案**
- 可以留給桌機臨時測試，但不適合 iPhone 管理入口

---

### 5) ngrok
**適合：** 臨時 demo 公開頁面，不適合管理面。

**優點**
- 很快拿到 HTTPS 公網網址

**缺點**
- 把管理入口送上公網，風險高
- 免費 / 臨時網址不穩定，不適合長期管理
- 對管理介面來說過度暴露，安全邊界差

**為什麼不建議**
- 你現在已經把公開內容移到 GitHub Pages，這是對的
- **公開內容** 與 **管理介面** 應分離；ngrok 比較像 demo 工具，不是穩健的 admin path

**結論**
- **不建議用來開放 OpenClaw dashboard/control UI**

---

### 6) Cloudflare Tunnel
**適合：** 想要公開 HTTPS，但又不想自己開 inbound port。

**優點**
- 比自行裸露 reverse proxy 更安全一些
- 有正式 HTTPS 網址，瀏覽器友善
- 不需要自己處理家用網路 port forwarding

**缺點**
- 依然是在做「公網可達的管理入口」
- 還是要額外做身份驗證、Access policy、WebSocket 相容驗證
- 對目前需求來說，仍比 Tailscale 複雜

**結論**
- 若未來真的需要「跨網際網路、用瀏覽器直接進入」可再考慮
- 但 **目前不是最佳第一步**

## 建議結論

### 最佳實務：**Tailscale + OpenClaw 走 tailnet / serve 路線**
原因很簡單：
1. iPhone 需要 secure、穩定、可識別裝置的連線方式
2. OpenClaw 控制面不應直接裸露到公網
3. 你目前已經把公開靜態內容放在 GitHub Pages，這很好；**dashboard 應與公開內容分流**

**一句話結論：**
- **公開頁面：GitHub Pages 保持公開**
- **管理 / dashboard：改走 Tailscale，不走 LAN HTTP，不走 ngrok**

## iPhone 具體設定步驟（推薦路線）

### A. Mac mini 端
1. 安裝並登入 Tailscale
2. 確認這台 Mac mini 已加入同一個 tailnet
3. 讓 OpenClaw 改走 tailnet 路線（優先考慮 `gateway.tailscale.mode=serve`；若環境較簡單，也可評估 `gateway.bind=tailnet`）
4. 重啟 OpenClaw gateway
5. 執行：
   ```bash
   openclaw qr --json
   ```
6. 確認輸出的 `gatewayUrl` 不再是：
   - `ws://192.168.x.x:18789`
   - `ws://localhost:18789`
   而是 tailnet / Tailscale 可達的位址

### B. iPhone 端
1. 安裝 Tailscale App
2. 登入與 Mac mini 相同的 tailnet
3. 確認 iPhone 上 Tailscale 已連線
4. 用 OpenClaw 的新 QR code 重新配對 / 重新連線
5. 若看到 `pairing required`，到主機批准裝置

### C. 配對確認
在主機上可用：
```bash
openclaw devices list
```
若有待核准裝置，再批准即可。

## 若真的要走 HTTPS 網址
只有在你明確想要：
- 不裝 Tailscale
- 直接用 Safari 開 `https://...`
- 從外網也能進管理頁

才建議考慮：
- Caddy / Nginx 反向代理
- 正式 TLS 憑證
- 嚴格存取控制
- 僅開 dashboard 所需路徑
- 驗證 WebSocket / session / auth 是否完整可用

這條路可做，但比 Tailscale 更容易把 admin surface 弄得太公開。

## 可安全先做的低風險準備（只建議，不直接變更）
1. **保留公開內容在 GitHub Pages**，不要把 dashboard 混進公開站
2. **維持 dashboard 與 public content 分離**
3. **先安裝 Tailscale 並登入同一 tailnet**
4. 完成後再檢查：
   ```bash
   openclaw qr --json
   ```
   看 `urlSource` 是否已從 `gateway.bind=lan` 變成 tailnet / serve 相關來源
5. 若未來才要做 HTTPS 公網入口，再另外規劃 Access policy，不要先用 ngrok 直通管理面

## 最短可行路線
1. Mac mini 安裝並登入 Tailscale
2. iPhone 安裝並登入同一個 Tailscale
3. OpenClaw 改成 tailnet / serve 路線
4. 重啟 gateway
5. 重新產生 QR code
6. iPhone 重新配對

**最短結論：**
- **不要再把 iPhone dashboard 建立在 LAN HTTP 上**
- **直接改走 Tailscale，是目前最 practical 的安全路線**
