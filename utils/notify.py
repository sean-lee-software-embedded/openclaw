#!/usr/bin/env python3
"""
推播訊息到 Telegram 的工具函數
可以從任何腳本 import 使用
"""
import os, requests

BOT_TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN",
    "8232639804:AAEv-3CqJ_FaSBdUGlEIH0kbaSoI56mVkqk"
)
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8626127659")

def send(text: str, parse_mode: str = "HTML") -> bool:
    """推播訊息到 Telegram，成功回傳 True"""
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": parse_mode},
            timeout=15,
        )
        return r.ok
    except Exception as e:
        print(f"[WARN] Telegram 推播失敗: {e}")
        return False

if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) or "🦞 測試訊息"
    ok = send(msg)
    print("✅ 推播成功" if ok else "❌ 推播失敗")
