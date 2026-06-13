#!/bin/zsh

set -euo pipefail

APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP_BUNDLE="$APP_ROOT/Markdown Converter.app"
ICON_PNG="$APP_ROOT/assets/markdown-converter-icon.png"
ICON_RSRC="/private/tmp/markdown-converter-icon.rsrc"
ICON_FILE="$APP_BUNDLE/Icon"$'\r'

if [ ! -d "$APP_BUNDLE" ]; then
  echo "Missing app bundle: $APP_BUNDLE" >&2
  exit 1
fi

if [ ! -f "$ICON_PNG" ]; then
  echo "Missing icon source: $ICON_PNG" >&2
  exit 1
fi

sips -i "$ICON_PNG" >/dev/null
DeRez -only icns "$ICON_PNG" > "$ICON_RSRC"
Rez -append "$ICON_RSRC" -o "$ICON_FILE"
SetFile -a V "$ICON_FILE"
SetFile -a C "$APP_BUNDLE"
touch "$APP_BUNDLE"

echo "Applied custom Finder icon to $APP_BUNDLE"
