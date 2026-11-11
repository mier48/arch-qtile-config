#!/bin/sh
set -eu
command -v rofi >/dev/null 2>&1 || exit 1
choice=$(printf '%s\n' Obsidian Cyberpunk Darcula |
    rofi -dmenu -i -no-custom -p "TEMA" -theme-str 'window { width: 480px; } listview { lines: 3; }') || exit 0
case "$choice" in
    Obsidian) name=obsidian ;;
    Cyberpunk) name=cyberpunk ;;
    Darcula) name=darcula ;;
    *) exit 0 ;;
esac
exec python "$HOME/.config/qtile/scripts/theme-switch.py" "$name"
