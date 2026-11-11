#!/bin/sh
# Operator HUD command palette. No user input is executed as shell code.
set -u

command -v rofi >/dev/null 2>&1 || exit 1

choice=$(printf '%s\n' \
    '01  Aplicaciones' \
    '02  Ventanas' \
    '03  Terminal' \
    '04  Monitor del sistema' \
    '05  Archivos' \
    '06  Temas' \
    '07  WireGuard' \
    '08  Notificaciones' \
    '09  Comando' \
    '10  Energía' |
    rofi -dmenu -i -no-custom -p 'OPERADOR' \
        -theme-str 'window { width: 580px; } listview { lines: 10; }') || exit 0

case "$choice" in
    '01  Aplicaciones') exec rofi -show drun ;;
    '02  Ventanas') exec rofi -show window ;;
    '03  Terminal') exec alacritty ;;
    '04  Monitor del sistema')
        if command -v btop >/dev/null 2>&1; then
            exec alacritty -e btop
        fi
        command -v dunstify >/dev/null 2>&1 &&
            dunstify 'Operator HUD' 'Falta btop: sudo pacman -S btop'
        exit 1
        ;;
    '05  Archivos') exec thunar ;;
    '06  Temas') exec /bin/sh "$HOME/.config/qtile/scripts/theme-menu.sh" ;;
    '07  VPN') exec python "$HOME/.config/qtile/scripts/vpn-menu.py" ;;
    '08  Notificaciones') exec dunstctl history-pop ;;
    '09  Comando') exec rofi -show run ;;
    '10  Energía') exec /bin/sh "$HOME/.config/qtile/scripts/power-menu.sh" ;;
    *) exit 0 ;;
esac
