#!/bin/sh
# Allowlisted power actions, confirmation on destructive commands, no eval.
set -u

error() {
    if command -v dunstify >/dev/null 2>&1; then
        dunstify -u critical "Obsidian · Energía" "$1"
    else
        printf '%s\n' "$1" >&2
    fi
}

choose() {
    rofi -dmenu -i -no-custom -p "$1" \
        -theme-str 'window { width: 460px; } listview { lines: 5; }'
}
confirm() {
    selected=$(printf 'No\nSí\n' | choose "$1") || return 1
    [ "$selected" = "Sí" ]
}
command -v rofi >/dev/null 2>&1 || { error "Falta rofi."; exit 1; }

choice=$(printf '%s\n' \
    'Bloquear sesión' 'Suspender' 'Cerrar sesión' 'Reiniciar' 'Apagar' |
    choose 'ENERGÍA') || exit 0

case "$choice" in
    'Bloquear sesión')
        if command -v i3lock >/dev/null 2>&1; then
            i3lock -c 111820 || error "No se pudo bloquear."
        else
            error "Bloqueo no disponible: instala i3lock."
        fi
        ;;
    'Suspender')
        if ! command -v i3lock >/dev/null 2>&1 ||
           ! pgrep -u "$(id -u)" -x xss-lock >/dev/null 2>&1; then
            error "Suspensión cancelada: inicia xss-lock con i3lock."
            exit 1
        fi
        if confirm "Confirmar suspensión"; then
            systemctl suspend || error "No se pudo suspender."
        fi
        ;;
    'Cerrar sesión')
        if confirm "Confirmar cierre de sesión"; then
            qtile cmd-obj -o cmd -f shutdown || error "No se pudo cerrar Qtile."
        fi
        ;;
    'Reiniciar')
        if confirm "Confirmar reinicio"; then
            systemctl reboot || error "No se pudo reiniciar."
        fi
        ;;
    'Apagar')
        if confirm "Confirmar apagado"; then
            systemctl poweroff || error "No se pudo apagar."
        fi
        ;;
    *) exit 0 ;;
esac
