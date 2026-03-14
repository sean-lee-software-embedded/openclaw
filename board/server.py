#!/usr/bin/env python3
import json, os, uuid
from datetime import datetime, date, timedelta
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
BOARD_FILE = os.path.join(DATA_DIR, "board.json")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

DEFAULT_BOARD = {
    "meta": {"version": 2},
    "kanban_columns": [
        {"id": "backlog",     "title": "📥 Backlog",     "order": 0},
        {"id": "todo",        "title": "📋 To Do",        "order": 1},
        {"id": "in_progress", "title": "⚙️ In Progress", "order": 2},
        {"id": "review",      "title": "👀 Review",       "order": 3},
        {"id": "done",        "title": "✅ Done",         "order": 4},
    ],
    "scrum_columns": [
        {"id": "s_todo",        "title": "To Do",       "order": 0},
        {"id": "s_in_progress", "title": "In Progress", "order": 1},
        {"id": "s_review",      "title": "In Review",   "order": 2},
        {"id": "s_done",        "title": "Done",        "order": 3},
    ],
    "sprints": [],
    "cards": [],
    "labels": [
        {"id": "cloud",   "name": "Cloud/BMC", "color": "#3b82f6"},
        {"id": "ai",      "name": "AI",        "color": "#8b5cf6"},
        {"id": "infra",   "name": "Infra",     "color": "#10b981"},
        {"id": "bug",     "name": "Bug",       "color": "#ef4444"},
        {"id": "feature", "name": "Feature",   "color": "#f59e0b"},
        {"id": "chore",   "name": "Chore",     "color": "#6b7280"},
    ]
}

def load():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(BOARD_FILE):
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    save(DEFAULT_BOARD)
    return DEFAULT_BOARD

def save(data):
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def nid(): return str(uuid.uuid4())[:8]
def now(): return datetime.now().isoformat()

@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/api/board")
def get_board():
    return jsonify(load())

@app.route("/api/sprints", methods=["POST"])
def create_sprint():
    board = load()
    d = request.json
    sprint = {
        "id": nid(),
        "name": d.get("name", f"Sprint {len(board['sprints'])+1}"),
        "goal": d.get("goal", ""),
        "start_date": d.get("start_date", str(date.today())),
        "end_date": d.get("end_date", str(date.today() + timedelta(days=14))),
        "status": "planning",
        "created_at": now(),
    }
    board["sprints"].append(sprint)
    save(board)
    return jsonify(sprint), 201

@app.route("/api/sprints/<sid>", methods=["PATCH"])
def update_sprint(sid):
    board = load()
    for s in board["sprints"]:
        if s["id"] == sid:
            s.update(request.json)
            save(board)
            return jsonify(s)
    return jsonify({"error": "not found"}), 404

@app.route("/api/sprints/<sid>/start", methods=["POST"])
def start_sprint(sid):
    board = load()
    for s in board["sprints"]:
        if s["status"] == "active":
            return jsonify({"error": "Another sprint is active"}), 400
    for s in board["sprints"]:
        if s["id"] == sid:
            s["status"] = "active"
            s["start_date"] = str(date.today())
            save(board)
            return jsonify(s)
    return jsonify({"error": "not found"}), 404

@app.route("/api/sprints/<sid>/complete", methods=["POST"])
def complete_sprint(sid):
    board = load()
    d = request.json or {}
    for s in board["sprints"]:
        if s["id"] == sid:
            s["status"] = "completed"
            s["completed_at"] = now()
            for c in board["cards"]:
                if c.get("sprint_id") == sid and c.get("scrum_column") != "s_done":
                    c["sprint_id"] = None
                    c["scrum_column"] = "s_todo"
            save(board)
            return jsonify(s)
    return jsonify({"error": "not found"}), 404

@app.route("/api/sprints/<sid>/burndown")
def burndown(sid):
    board = load()
    sprint = next((s for s in board["sprints"] if s["id"] == sid), None)
    if not sprint:
        return jsonify({"error": "not found"}), 404
    cards = [c for c in board["cards"] if c.get("sprint_id") == sid]
    total = sum(c.get("story_points", 0) for c in cards)
    start = datetime.fromisoformat(sprint["start_date"]).date()
    end   = datetime.fromisoformat(sprint["end_date"]).date()
    today = date.today()
    days  = max((end - start).days, 1)
    ideal = [{"date": str(start + timedelta(days=i)),
              "points": round(total * (1 - i/days), 1)}
             for i in range(days + 1)]
    actual = []
    for i in range((min(today, end) - start).days + 1):
        d = start + timedelta(days=i)
        remaining = sum(
            c.get("story_points", 0) for c in cards
            if not (c.get("scrum_column") == "s_done"
                    and c.get("updated_at","")[:10] <= str(d))
        )
        actual.append({"date": str(d), "points": remaining})
    done_pts = sum(c.get("story_points", 0)
                   for c in cards if c.get("scrum_column") == "s_done")
    return jsonify({"sprint": sprint, "total_points": total,
                    "completed_points": done_pts,
                    "ideal": ideal, "actual": actual})

@app.route("/api/cards", methods=["POST"])
def create_card():
    board = load()
    d = request.json
    card = {
        "id": nid(),
        "title": d.get("title", "New Story"),
        "description": d.get("description", ""),
        "type": d.get("type", "story"),
        "story_points": int(d.get("story_points", 0)),
        "priority": d.get("priority", "medium"),
        "labels": d.get("labels", []),
        "due_date": d.get("due_date", ""),
        "source_url": d.get("source_url", ""),
        "acceptance_criteria": d.get("acceptance_criteria", ""),
        "kanban_column": d.get("kanban_column", "backlog"),
        "sprint_id": d.get("sprint_id"),
        "scrum_column": d.get("scrum_column", "s_todo"),
        "backlog_order": d.get("backlog_order", len(board["cards"])),
        "order": len(board["cards"]),
        "created_at": now(),
    }
    board["cards"].append(card)
    save(board)
    return jsonify(card), 201

@app.route("/api/cards/<cid>", methods=["PATCH"])
def update_card(cid):
    board = load()
    for c in board["cards"]:
        if c["id"] == cid:
            c.update(request.json)
            c["updated_at"] = now()
            save(board)
            return jsonify(c)
    return jsonify({"error": "not found"}), 404

@app.route("/api/cards/<cid>", methods=["DELETE"])
def delete_card(cid):
    board = load()
    board["cards"] = [c for c in board["cards"] if c["id"] != cid]
    save(board)
    return jsonify({"ok": True})

@app.route("/api/cards/<cid>/move", methods=["PATCH"])
def move_card(cid):
    board = load()
    d = request.json
    for c in board["cards"]:
        if c["id"] == cid:
            if "kanban_column" in d: c["kanban_column"] = d["kanban_column"]
            if "scrum_column"  in d: c["scrum_column"]  = d["scrum_column"]
            if "sprint_id"     in d:
                c["sprint_id"] = d["sprint_id"]
                if d["sprint_id"] and not c.get("scrum_column"):
                    c["scrum_column"] = "s_todo"
            c["updated_at"] = now()
            save(board)
            return jsonify(c)
    return jsonify({"error": "not found"}), 404

@app.route("/api/news")
def get_news():
    f = os.path.join(DATA_DIR, "latest_summary.json")
    if not os.path.exists(f):
        return jsonify({"summary": "尚無摘要，請先跑 crawler.py"})
    with open(f, "r", encoding="utf-8") as fp:
        return jsonify(json.load(fp))

if __name__ == "__main__":
    print("🦞 Lobster Board API  →  http://0.0.0.0:3333")
    app.run(host="0.0.0.0", port=3333, debug=False)
