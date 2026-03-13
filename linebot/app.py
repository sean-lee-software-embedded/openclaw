#!/usr/bin/env python3
import json, os, threading, requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
YOUR_LINE_USER_ID = os.environ.get("LINE_USER_ID", "")

# ✏️ 填入你們三個人的 LINE User ID
ALLOWED_USERS = [
    # "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 你
    # "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 兄弟 A
    # "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 兄弟 B
]

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:14b"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "latest_summary.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
_conversations = {}

def load_conversations():
    global _conversations
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            _conversations = json.load(f)

def save_conversations():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(_conversations, f, ensure_ascii=False, indent=2)

def add_to_history(user_id, role, content):
    if user_id not in _conversations:
        _conversations[user_id] = []
    _conversations[user_id].append({"role": role, "content": content})
    if len(_conversations[user_id]) > 12:
        _conversations[user_id] = _conversations[user_id][-12:]
    save_conversations()

def ask_llm(user_id, user_message):
    history = _conversations.get(user_id, [])
    history_text = ""
    for msg in history[-6:]:
        prefix = "使用者" if msg["role"] == "user" else "助手"
        history_text += f"{prefix}：{msg['content']}\n"
    prompt = f"""你是一個技術助理，擅長 Cloud、OpenBMC、Linux 和 AI 相關知識。用繁體中文回答，簡潔有重點。

{history_text}使用者：{user_message}
助手："""
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 800}
        }, timeout=60)
        reply = resp.json()["response"].strip()
        add_to_history(user_id, "user", user_message)
        add_to_history(user_id, "assistant", reply)
        return reply
    except Exception as e:
        return f"⚠️ 龍蝦暫時睡著了...\n錯誤：{str(e)[:100]}"

def get_today_articles():
    if not os.path.exists(ARTICLES_FILE):
        return "尚未爬取任何文章 📭"
    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    from datetime import date
    today = str(date.today())
    today_articles = [a for a in articles.values() if a["date"] == today]
    if not today_articles:
        return "今天還沒有新文章 🕐"
    by_topic = {}
    for a in today_articles:
        by_topic.setdefault(a["topic_label"], []).append(a)
    lines = [f"📰 {today} 完整列表\n"]
    for label, arts in by_topic.items():
        lines.append(label)
        for a in arts[:5]:
            lines.append(f"• {a['title']}\n  {a['url']}")
        lines.append("")
    return "\n".join(lines)[:4500]

def get_latest_summary():
    if not os.path.exists(SUMMARY_FILE):
        return "還沒有摘要，請等明天早上 8 點爬蟲跑完 🕗"
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return f"📋 {data['date']} 摘要\n\n{data['summary']}"

def handle_command(user_id, text):
    t = text.strip().lower()
    if t in ["今日新聞", "今天新聞", "news", "新聞"]:
        return get_today_articles()
    elif t in ["摘要", "summary", "今日摘要"]:
        return get_latest_summary()
    elif t in ["help", "幫助", "指令", "?"]:
        return (
            "🦞 龍蝦 Bot 指令列表\n\n"
            "📰 今日新聞 → 今天完整文章列表\n"
            "📋 摘要 → 今日 AI 生成摘要\n"
            "🧹 清除記憶 → 重置對話\n"
            "❓ 其他任何問題 → 問本地 LLM\n\n"
            "每天早上 8:00 自動推播摘要 ⏰"
        )
    elif t in ["清除記憶", "reset", "重置"]:
        _conversations.pop(user_id, None)
        save_conversations()
        return "🧹 對話記憶已清除！"
    return None

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id

    # 白名單檢查（如果 ALLOWED_USERS 是空的就跳過，方便初始設定）
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="這隻龍蝦是私人的 🦞")
        )
        return

    user_text = event.message.text.strip()
    reply = handle_command(user_id, user_text)

    if reply is None:
        def respond():
            answer = ask_llm(user_id, user_text)
            line_bot_api.push_message(user_id, TextSendMessage(text=answer))
        threading.Thread(target=respond, daemon=True).start()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="🦞 龍蝦思考中...")
        )
        return

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="🦞 龍蝦 Bot 啟動！\n\n輸入「幫助」看所有指令\n每天早上 8:00 會推播技術新聞摘要 ✅")
    )

def push_daily_summary():
    if not YOUR_LINE_USER_ID:
        print("[WARN] 未設定 LINE_USER_ID")
        return
    summary = get_latest_summary()
    line_bot_api.push_message(YOUR_LINE_USER_ID, TextSendMessage(text=summary))
    print("[INFO] 今日摘要已推播至 LINE")

if __name__ == "__main__":
    load_conversations()
    print("🦞 LINE Bot 啟動中... port 5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
