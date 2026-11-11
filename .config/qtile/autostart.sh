#!/bin/sh
# X11 session startup. All commands are optional and run at most once.

start_once() {
    name="$1"
    shift
    if command -v "$name" >/dev/null 2>&1 && ! pgrep -x "$name" >/dev/null 2>&1; then
        "$name" "$@" &
    fi
}

start_once picom
start_once dunst
start_once nm-applet
start_once udiskie -t

# Optional wallpaper with a theme-consistent fallback.
wallpaper="$HOME/Images/wallpaper/wallpaper-4.jpg"
if command -v feh >/dev/null 2>&1 && [ -f "$wallpaper" ]; then
    feh --no-fehbg --bg-fill "$wallpaper"
elif command -v xsetroot >/dev/null 2>&1; then
    xsetroot -solid '#111820'
fi
