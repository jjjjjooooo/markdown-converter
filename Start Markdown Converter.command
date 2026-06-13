#!/bin/zsh

APP_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_ROOT" || exit 1

if [ ! -x "$APP_ROOT/.venv/bin/python" ]; then
  echo "Missing .venv. Run this once:"
  echo "python3 -m venv .venv"
  echo ".venv/bin/python -m pip install -r requirements.txt"
  read -r "unused?Press return to close."
  exit 1
fi

if ! "$APP_ROOT/.venv/bin/python" -c 'from app.desktop import load_tkinter; load_tkinter()' >/dev/null 2>&1; then
  echo "This .venv Python does not include Tkinter."
  echo "Create the virtual environment with a Python build that supports Tkinter, then reinstall requirements:"
  echo "python3 -c 'import tkinter'"
  echo "python3 -m venv .venv"
  echo ".venv/bin/python -m pip install -r requirements.txt"
  read -r "unused?Press return to close."
  exit 1
fi

echo "Starting Markdown Converter..."
echo

exec "$APP_ROOT/.venv/bin/python" -m app.desktop
