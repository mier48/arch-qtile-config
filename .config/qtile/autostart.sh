#!/bin/sh
# Operator HUD: one X11 autostart per login (Qtile startup_once).
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

# A standalone Qtile session needs a graphical Polkit agent for privileged actions.
# Avoid GTK theming dependencies; do not start a second agent if one already runs.
if [ -x /usr/bin/lxqt-policykit-agent ] &&
   ! pgrep -u "$(id -u)" -f '^/usr/bin/lxqt-policykit-agent($| )' >/dev/null 2>&1; then
    /usr/bin/lxqt-policykit-agent &
fi


# xss-lock watches XScreenSaver and logind's PrepareForSleep signal.
# --transfer-sleep-lock passes the logind delay FD to the lock command.
# lock.sh executes foreground i3lock -n; never background the locker itself.
if command -v xss-lock >/dev/null 2>&1 &&
   command -v i3lock >/dev/null 2>&1; then
    # 10 minute idle timeout. It intentionally does not disable XScreenSaver.
    if command -v xset >/dev/null 2>&1; then
        xset s 600 600
    fi
    start_once xss-lock --transfer-sleep-lock -- /bin/sh "$HOME/.config/qtile/scripts/lock.sh"
fi

/bin/sh "$HOME/.config/qtile/scripts/wallpaper.sh"
