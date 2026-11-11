#!/bin/sh
# Theme-aware i3lock wrapper for manual and logind-triggered locks.
set -eu
name=$(python -c 'import json,os,pathlib; p=pathlib.Path(os.path.expanduser("~/.config/qtile/config.json")); print(json.loads(p.read_text()).get("theme","obsidian"))' 2>/dev/null || printf obsidian)
case "$name" in
    cyberpunk) bg=0B101B ;;
    darcula) bg=2B2B2B ;;
    *) bg=111820 ;;
esac
exec i3lock -n -c "$bg"
