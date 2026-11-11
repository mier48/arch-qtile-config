#!/bin/sh
# Qtile X11 single-start services and dynamic wallpaper.
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
    start_once xss-lock --transfer-sleep-lock -- /bin/sh "$HOME/.config/qtile/scripts/lock.sh"
fi
/bin/sh "$HOME/.config/qtile/scripts/wallpaper.sh"
