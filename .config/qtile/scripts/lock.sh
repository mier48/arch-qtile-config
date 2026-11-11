#!/bin/sh
# Secure X11 lock: xss-lock waits for this process, so DO NOT daemonize i3lock.
set -eu
umask 077

name=$(python -c 'import json,os,pathlib;p=pathlib.Path(os.path.expanduser("~/.config/qtile/config.json"));print(json.loads(p.read_text()).get("theme","obsidian"))' 2>/dev/null || printf '%s' obsidian)
case "$name" in
    cyberpunk) bg='0B101B' ;;
    darcula) bg='2B2B2B' ;;
    *) name=obsidian; bg='111820' ;;
esac

root="$HOME/.config/qtile/lockscreen"
cache="${XDG_CACHE_HOME:-$HOME/.cache}/qtile-lockscreen"
image="$cache/$name-3440x1440.png"
source="$root/$name.svg"

# Generate a public, static asset. Never screenshot the unlocked desktop.
if [ -f "$source" ] && command -v rsvg-convert >/dev/null 2>&1; then
    mkdir -p -m 700 "$cache"
    chmod 700 "$cache"
    if [ ! -f "$image" ] || [ "$source" -nt "$image" ]; then
        tmp=$(mktemp "$cache/.lock-XXXXXXXX.png")
        trap 'rm -f "$tmp"' EXIT HUP INT TERM
        if rsvg-convert -w 3440 -h 1440 -o "$tmp" "$source"; then
            mv -f "$tmp" "$image"
        fi
    fi
fi

if ! command -v i3lock >/dev/null 2>&1; then
    printf '%s\n' 'Bloqueo no disponible: instala i3lock.' >&2
    exit 1
fi

# -n / --nofork: remain in foreground so logind sleep inhibitor is not released early.
# An image is optional; failed image rendering falls back to solid color.
if [ -s "$image" ]; then
    exec i3lock -n -i "$image"
fi
exec i3lock -n -c "$bg"
