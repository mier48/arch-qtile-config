#!/bin/sh
# Obsidian X11 startup; invoked once by Qtile startup_once.
start_once() {
    name="$1"
    shift
    if command -v "$name" >/dev/null 2>&1 &&
        ! pgrep -u "$(id -u)" -x "$name" >/dev/null 2>&1; then
        "$name" "$@" &
    fi
}

start_once picom --config "$HOME/.config/picom/picom.conf"
start_once dunst -conf "$HOME/.config/dunst/dunstrc"
start_once nm-applet
start_once udiskie -t

if command -v xss-lock >/dev/null 2>&1 &&
   command -v i3lock >/dev/null 2>&1; then
    start_once xss-lock --transfer-sleep-lock -- i3lock -n -c 111820
fi

source="$HOME/.config/qtile/wallpapers/obsidian.svg"
cache="$HOME/.cache/obsidian"
image="$cache/wallpaper-3440x1440.png"

if [ -f "$source" ] && command -v rsvg-convert >/dev/null 2>&1; then
    mkdir -p "$cache"
    if [ ! -f "$image" ] || [ "$source" -nt "$image" ]; then
        tmp="$cache/wallpaper-$$.png"
        if rsvg-convert -w 3440 -h 1440 -o "$tmp" "$source"; then
            mv -f "$tmp" "$image"
        else
            rm -f "$tmp"
        fi
    fi
fi

if [ -f "$image" ] && command -v feh >/dev/null 2>&1; then
    feh --no-fehbg --bg-fill "$image"
elif command -v xsetroot >/dev/null 2>&1; then
    xsetroot -solid '#111820'
fi
