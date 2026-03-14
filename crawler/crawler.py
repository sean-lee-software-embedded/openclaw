#!/usr/bin/env python3
import json, os, time, hashlib, feedparser, requests
from datetime import datetime, date

DATA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data")
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")
SUMMARY_FILE  = os.path.join(DATA_DIR, "latest_summary.json")
OLLAMA_URL    = "http://localhost:11434/api/generate"
OLLAMA_MODEL  = "qwen2.5:14b"

FEEDS = {
    "cloud_server": {
        "label": "☁️ Cloud Server 市場動態",
        "sources": [
            ("ServeTheHome",       "https://www.servethehome.com/feed/"),
            ("The Register DC",    "https://www.theregister.com/data_centre/rss"),
            ("The New Stack",      "https://thenewstack.io/feed/"),
            ("AnandTech",          "https://www.anandtech.com/rss/"),
            ("Data Center Dynamics","https://www.datacenterdynamics.com/en/rss/"),
        ]
    },
    "openbmc_redfish": {
        "label": "🔧 OpenBMC / Redfish",
        "sources": [
            ("OpenBMC Releases",   "https://github.com/openbmc/openbmc/releases.atom"),
            ("Phoronix",           "https://www.phoronix.com/rss.php"),
            ("OCP News",           "https://www.opencompute.org/feed"),
            ("DMTF News",          "https://www.dmtf.org/about/rss-feeds"),
            ("LWN.net",            "https://lwn.net/headlines/rss"),
        ]
    },
    "ai_news": {
        "label": "🤖 AI 最新消息",
        "sources": [
            ("HuggingFace Blog",   "https://huggingface.co/blog/feed.xml"),
            ("Anthropic News",     "https://www.anthropic.com/news/rss"),
            ("VentureBeat AI",     "https://venturebeat.com/category/ai/feed/"),
            ("The Batch",          "https://www.deeplearning.ai/the-batch/feed/"),
            ("Papers With Code",   "https://paperswithcode.com/latest.rss"),
        ]
    },
}

# ── helpers ──────────────────────────────────────────────────────────────────

def load_articles() -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_articles(data: dict):
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def article_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]

# ── fetch ─────────────────────────────────────────────────────────────────────

def fetch_feeds() -> dict:
    articles  = load_articles()
    today     = str(date.today())
    new_count = 0

    for topic, config in FEEDS.items():
        for source_name, feed_url in config["sources"]:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    url = entry.get("link", "")
                    if not url:
                        continue
                    aid = article_id(url)
                    if aid not in articles:
                        articles[aid] = {
                            "id":          aid,
                            "title":       entry.get("title", "").strip(),
                            "url":         url,
                            "source":      source_name,
                            "topic":       topic,
                            "topic_label": config["label"],
                            "date":        today,
                            "summary":     "",
                            "sent":        False,
                        }
                        new_count += 1
                time.sleep(1)
            except Exception as e:
                print(f"[WARN] {source_name}: {e}")

    save_articles(articles)
    print(f"[INFO] 爬蟲完成，新增 {new_count} 篇文章")
    return articles

# ── summarise ────────────────────────────────────────────────────────────────

def summarize_with_llm(articles: dict) -> str | None:
    today         = str(date.today())
    today_articles = [a for a in articles.values() if a["date"] == today and not a["sent"]]
    if not today_articles:
        print("[INFO] 今天沒有新文章")
        return None

    by_topic: dict = {}
    for a in today_articles:
        by_topic.setdefault(a["topic"], []).append(a)

    parts = []
    for topic, arts in by_topic.items():
        label  = arts[0]["topic_label"]
        titles = "\n".join([f"- {a['title']} ({a['source']})" for a in arts])
        parts.append(f"{label}:\n{titles}")

    all_titles = "\n\n".join(parts)
    total      = len(today_articles)

    prompt = f"""你是技術新聞摘要助手。以下是今天 ({today}) 的技術新聞標題，請用繁體中文做簡潔摘要。

{all_titles}

要求：
1. 每個分類用 emoji 標題開頭
2. 列出 2-3 條最重要的新聞，每條 1 句話說明重點
3. 最後一行加上：「📎 共 {total} 篇，輸入今日新聞看完整列表」
4. 全文不超過 600 字

直接輸出，不要多餘的前言："""

    print("[INFO] 請本地 LLM 摘要中...")
    try:
        resp    = requests.post(OLLAMA_URL, json={
            "model":   OLLAMA_MODEL,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": 0.3},
        }, timeout=120)
        summary = resp.json()["response"].strip()
        return summary
    except Exception as e:
        print(f"[ERROR] LLM 摘要失敗: {e}")
        lines = [f"📅 {today} 今日技術新聞"]
        for _, arts in by_topic.items():
            lines.append(arts[0]["topic_label"])
            for a in arts[:3]:
                lines.append(f"• {a['title']}")
        return "\n".join(lines)

def mark_as_sent(articles: dict):
    today = str(date.today())
    for a in articles.values():
        if a["date"] == today:
            a["sent"] = True
    save_articles(articles)

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[{datetime.now()}] 開始爬蟲...")
    articles = fetch_feeds()
    summary  = summarize_with_llm(articles)
    if summary:
        print("\n===== 今日摘要 =====")
        print(summary)
        print("====================\n")
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            json.dump({"date": str(date.today()), "summary": summary},
                      f, ensure_ascii=False, indent=2)
        mark_as_sent(articles)
