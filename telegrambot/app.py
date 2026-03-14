#!/usr/bin/env python3
"""
🦞 Lobster Bot — Telegram edition
"""
import json, os, logging, requests
from datetime import date
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BOARD_URL          = os.environ.get("BOARD_URL", "http://localhost:3333")
MAC_IP             = "192.168.1.101"

# Whitelist of Telegram user IDs (integers). Leave empty to allow all.
ALLOWED_USERS: list[int] = [
    8626127659,  # 空空肖肖
    # 987654321,  # 兄弟 A
    # 111222333,  # 兄弟 B
]

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:14b"
DATA_DIR     = os.path.join(os.path.dirname(__file__), "..", "data")
ARTICLES_FILE      = os.path.join(DATA_DIR, "articles.json")
SUMMARY_FILE       = os.path.join(DATA_DIR, "latest_summary.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")

# ── conversation store ──────────────────────────────────────────────────────

_conversations: dict = {}

def load_conversations():
    global _conversations
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            _conversations = json.load(f)

def save_conversations():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(_conversations, f, ensure_ascii=False, indent=2)

def add_to_history(uid: str, role: str, content: str):
    if uid not in _conversations:
        _conversations[uid] = []
    _conversations[uid].append({"role": role, "content": content})
    if len(_conversations[uid]) > 12:
        _conversations[uid] = _conversations[uid][-12:]
    save_conversations()

# ── LLM ────────────────────────────────────────────────────────────────────

def ask_llm(uid: str, user_message: str) -> str:
    history = _conversations.get(uid, [])
    history_text = ""
    for msg in history[-6:]:
        prefix = "使用者" if msg["role"] == "user" else "助手"
        history_text += f"{prefix}：{msg['content']}\n"
    prompt = (
        "你是一個技術助理，擅長 Cloud、OpenBMC、Linux 和 AI 相關知識。"
        "用繁體中文回答，簡潔有重點。\n\n"
        f"{history_text}使用者：{user_message}\n助手："
    )
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model":   OLLAMA_MODEL,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": 0.7, "num_predict": 800},
        }, timeout=60)
        reply = resp.json()["response"].strip()
        add_to_history(uid, "user", user_message)
        add_to_history(uid, "assistant", reply)
        return reply
    except Exception as e:
        return f"⚠️ 龍蝦暫時睡著了...\n錯誤：{str(e)[:100]}"

# ── content helpers ─────────────────────────────────────────────────────────

def get_today_articles() -> str:
    if not os.path.exists(ARTICLES_FILE):
        return "尚未爬取任何文章 📭"
    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    today = str(date.today())
    today_articles = [a for a in articles.values() if a["date"] == today]
    if not today_articles:
        return "今天還沒有新文章 🕐"
    by_topic: dict = {}
    for a in today_articles:
        by_topic.setdefault(a["topic_label"], []).append(a)
    lines = [f"📰 {today} 完整列表\n"]
    for label, arts in by_topic.items():
        lines.append(label)
        for a in arts[:5]:
            lines.append(f"• {a['title']}\n  {a['url']}")
        lines.append("")
    return "\n".join(lines)[:4096]

def get_latest_summary() -> str:
    if not os.path.exists(SUMMARY_FILE):
        return "還沒有摘要，請等明天早上 8 點爬蟲跑完 🕗"
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return f"📋 {data['date']} 摘要\n\n{data['summary']}"

def get_board_status() -> str:
    try:
        r = requests.get(f"{BOARD_URL}/api/board", timeout=5)
        b = r.json()
        cards   = b.get("cards", [])
        sprints = b.get("sprints", [])
        active  = next((s for s in sprints if s.get("status") == "active"), None)

        col_count = {}
        for c in cards:
            col = c.get("kanban_column", "backlog")
            col_count[col] = col_count.get(col, 0) + 1

        lines = ["📋 Board 狀態\n"]
        col_labels = {
            "backlog": "📥 Backlog", "todo": "📋 To Do",
            "in_progress": "⚙️ In Progress", "review": "👀 Review", "done": "✅ Done"
        }
        for cid, label in col_labels.items():
            n = col_count.get(cid, 0)
            lines.append(f"{label}: {n} 張")

        if active:
            sprint_cards = [c for c in cards if c.get("sprint_id") == active["id"]]
            total = sum(c.get("story_points", 0) for c in sprint_cards)
            done  = sum(c.get("story_points", 0) for c in sprint_cards if c.get("scrum_column") == "s_done")
            pct   = int(done / total * 100) if total else 0
            lines.append(f"\n🏃 {active['name']}: {done}/{total} pts ({pct}%)")
        else:
            lines.append("\n🏃 目前沒有進行中的 Sprint")

        return "\n".join(lines)
    except Exception as e:
        return f"⚠️ Board 連不上 ({str(e)[:60]})\n確認 board/server.py 有在跑"

# ── access control ──────────────────────────────────────────────────────────

def is_allowed(user_id: int) -> bool:
    return not ALLOWED_USERS or user_id in ALLOWED_USERS

# ── command handlers ────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦞 龍蝦 Bot 啟動！\n\n輸入「幫助」看所有指令\n每天早上 8:00 會推播技術新聞摘要 ✅"
    )

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦞 龍蝦 Bot 指令列表\n\n"
        "📰 今日新聞 → 今天完整文章列表\n"
        "📋 摘要 → 今日 AI 生成摘要\n"
        "📊 /board → Board 連結 + 狀態\n"
        "📈 /status → Board 卡片統計\n"
        "🧹 清除記憶 → 重置對話\n"
        "❓ 其他任何問題 → 問本地 LLM\n\n"
        "每天早上 8:00 自動推播摘要 ⏰"
    )

async def cmd_news(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id): return
    await update.message.reply_text(get_today_articles())

async def cmd_summary(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id): return
    await update.message.reply_text(get_latest_summary())

async def cmd_board(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id): return
    status = get_board_status()
    link   = f"http://{MAC_IP}:3333"
    await update.message.reply_text(
        f"{status}\n\n🔗 打開 Board：{link}"
    )

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id): return
    await update.message.reply_text(get_board_status())

async def cmd_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id): return
    uid = str(update.effective_user.id)
    _conversations.pop(uid, None)
    save_conversations()
    await update.message.reply_text("🧹 對話記憶已清除！")

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_allowed(user.id):
        await update.message.reply_text("這隻龍蝦是私人的 🦞")
        return

    uid  = str(user.id)
    text = update.message.text.strip()
    t    = text.lower()

    if t in ["今日新聞", "今天新聞", "news", "新聞"]:
        await update.message.reply_text(get_today_articles()); return
    if t in ["摘要", "summary", "今日摘要"]:
        await update.message.reply_text(get_latest_summary()); return
    if t in ["help", "幫助", "指令", "?"]:
        await cmd_help(update, ctx); return
    if t in ["清除記憶", "reset", "重置"]:
        await cmd_reset(update, ctx); return
    if t in ["board", "看板", "board狀態"]:
        await cmd_board(update, ctx); return

    thinking = await update.message.reply_text("🦞 龍蝦思考中...")
    reply = ask_llm(uid, text)
    await thinking.edit_text(reply)

# ── main ────────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    load_conversations()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("help",    cmd_help))
    app.add_handler(CommandHandler("news",    cmd_news))
    app.add_handler(CommandHandler("summary", cmd_summary))
    app.add_handler(CommandHandler("board",   cmd_board))
    app.add_handler(CommandHandler("status",  cmd_status))
    app.add_handler(CommandHandler("reset",   cmd_reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🦞 Lobster Telegram Bot 啟動中...")
    app.run_polling()

if __name__ == "__main__":
    main()
