#!/bin/bash
# 🦞 龍蝦系統每日排程
# 用法：crontab -e 加入：
#   0 8 * * * /Users/sean/projects/lobster_system/scripts/daily_run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."
LOG_DIR="$ROOT/logs"
LOG_FILE="$LOG_DIR/daily_$(date +%Y-%m-%d).log"

mkdir -p "$LOG_DIR"

echo "========================================" | tee -a "$LOG_FILE"
echo "🦞 龍蝦系統啟動: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

cd "$ROOT"

# activate virtualenv if available
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "[INFO] virtualenv 已啟動" | tee -a "$LOG_FILE"
fi

# run crawler
echo "[INFO] 開始爬蟲..." | tee -a "$LOG_FILE"
python3 crawler/crawler.py 2>&1 | tee -a "$LOG_FILE"

echo "[INFO] 完成！Log: $LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
