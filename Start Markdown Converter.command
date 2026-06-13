#!/bin/zsh

APP_ROOT="$(cd "$(dirname "$0")" && pwd)"
URL="http://127.0.0.1:8000"
LOG_DIR="$APP_ROOT/logs"
LOG_FILE="$LOG_DIR/server.log"
CURL="/usr/bin/curl"
OPEN="/usr/bin/open"

mkdir -p "$LOG_DIR"
cd "$APP_ROOT" || exit 1

if "$CURL" -fsS "$URL" >/dev/null 2>&1; then
  "$OPEN" "$URL"
  exit 0
fi

if [ ! -x "$APP_ROOT/.venv/bin/python" ]; then
  echo "Missing .venv. Run this once:"
  echo "python3 -m venv .venv"
  echo ".venv/bin/python -m pip install -r requirements.txt"
  read -r "unused?Press return to close."
  exit 1
fi

(
  for _ in {1..50}; do
    if "$CURL" -fsS "$URL" >/dev/null 2>&1; then
      "$OPEN" "$URL"
      exit 0
    fi
    sleep 0.2
  done
) &

echo "Starting Markdown Converter..."
echo "Leave this Terminal window open while you use the app."
echo "Close this window or press Control-C to stop it."
echo

exec "$APP_ROOT/.venv/bin/python" -u -m app.server 2>&1 | tee "$LOG_FILE"
