#!/bin/sh
set -eu
root="$HOME/.config/qtile"
name=$(python -c 'import json,os,pathlib; p=pathlib.Path(os.path.expanduser("~/.config/qtile/config.json")); print(json.loads(p.read_text()).get("theme","obsidian"))' 2>/dev/null || printf obsidian)
case "$name" in obsidian|cyberpunk|darcula) ;; *) name=obsidian ;; esac
src="$root/wallpapers/$name.svg"
cache="$HOME/.cache/qtile-wallpapers"
out="$cache/$name-3440x1440.png"
if [ -f "$src" ] && command -v rsvg-convert >/dev/null 2>&1; then
    mkdir -p "$cache"
    if [ ! -f "$out" ] || [ "$src" -nt "$out" ]; then
        temp="$cache/.$name-$$.png"
        trap 'rm -f "$temp"' EXIT HUP INT TERM
        if rsvg-convert -w 3440 -h 1440 -o "$temp" "$src"; then
            mv -f "$temp" "$out"
        fi
    fi
fi
if [ -f "$out" ] && command -v feh >/dev/null 2>&1; then
    feh --no-fehbg --bg-fill "$out"
elif command -v xsetroot >/dev/null 2>&1; then
    case "$name" in cyberpunk) xsetroot -solid '#0B101B' ;; darcula) xsetroot -solid '#2B2B2B' ;; *) xsetroot -solid '#111820' ;; esac
fi
