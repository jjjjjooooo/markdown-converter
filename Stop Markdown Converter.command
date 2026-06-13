#!/bin/zsh

PID="$(/usr/sbin/lsof -tiTCP:8000 -sTCP:LISTEN)"

if [ -n "$PID" ]; then
  kill "$PID"
  echo "Markdown Converter stopped."
else
  echo "Markdown Converter is not running on port 8000."
fi

read -r "unused?Press return to close."
