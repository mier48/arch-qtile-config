#!/bin/sh
# Operator HUD: install versioned dotfiles as the regular user, with backups.
set -eu

usage() {
    cat <<'EOF'
Uso: sh scripts/install-dotfiles.sh --check
     sh scripts/install-dotfiles.sh --apply [--theme obsidian|cyberpunk|darcula]

--check  Comprueba dependencias y tests sin modificar archivos (predeterminado).
--apply  Instala los siete directorios de ~/.config con respaldo y rollback.
--theme  Tema inicial; si se omite, conserva el tema seleccionado anteriormente.
EOF
}

mode=check
requested_theme=
while [ "$#" -gt 0 ]; do
    case "$1" in
        --check) mode=check ;;
        --apply) mode=apply ;;
        --theme)
            [ "$#" -ge 2 ] || { usage >&2; exit 2; }
            requested_theme=$2
            shift ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
    shift
done
case "$requested_theme" in
    ''|obsidian|cyberpunk|darcula) ;;
    *) printf '%s\n' 'Tema inválido.' >&2; exit 2 ;;
esac

[ "$(id -u)" -ne 0 ] || {
    printf '%s\n' 'No ejecutes el instalador de dotfiles con sudo.' >&2
    exit 1
}

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
config="$HOME/.config"
components='qtile fish alacritty fastfetch rofi dunst picom'

[ -d "$root/.config/qtile" ] || {
    printf '%s\n' 'No se encontró la raíz del repositorio.' >&2
    exit 1
}
for component in $components; do
    [ -d "$root/.config/$component" ] || {
        printf 'Falta el directorio %s en el repositorio.\n' "$component" >&2
        exit 1
    }
done

if [ "$mode" = check ]; then
    failed=0
    for cmd in python qtile alacritty fish rofi dunst picom fastfetch \
        i3lock xss-lock xset xrandr feh rsvg-convert thunar scrot \
        nm-applet udiskie pgrep; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            printf 'FALTA: %s\n' "$cmd"
            failed=1
        fi
    done
    if [ "$failed" -ne 0 ]; then
        printf '%s\n' 'Instala los paquetes del README y repite --check.' >&2
        exit 1
    fi
    (cd "$root" && python -m unittest discover -s tests -q)
    printf '%s\n' 'Dependencias principales y tests estáticos: OK.'
    exit 0
fi

# Test the repository before replacing a working user configuration.
(cd "$root" && python -m unittest discover -s tests -q)
mkdir -p "$config"
[ -d "$config" ] && [ ! -L "$config" ] || {
    printf '%s\n' 'La ruta de configuración debe ser un directorio real.' >&2
    exit 1
}

theme=$requested_theme
if [ -z "$theme" ] && [ -f "$config/qtile/config.json" ]; then
    theme=$(python - "$config/qtile/config.json" <<'PY'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as stream:
        value = json.load(stream).get("theme")
    print(value if value in ("obsidian", "cyberpunk", "darcula") else "obsidian")
except (OSError, ValueError, TypeError):
    print("obsidian")
PY
)
fi
[ -n "$theme" ] || theme=obsidian

stamp=$(date +%Y%m%d-%H%M%S)-$$
stage=$(mktemp -d "$config/.operator-stage.XXXXXXXX")
saved=
installed=
committed=0

rollback() {
    status=$?
    trap - 0 HUP INT TERM
    if [ "$committed" -ne 1 ]; then
        printf '%s\n' 'Fallo: restaurando la configuración anterior.' >&2
        for component in $installed; do
            if [ -e "$config/$component" ] || [ -L "$config/$component" ]; then
                mv -- "$config/$component" "$config/$component.failed.$stamp" || :
            fi
        done
        for component in $saved; do
            if [ -e "$config/$component.backup.$stamp" ] || [ -L "$config/$component.backup.$stamp" ]; then
                mv -- "$config/$component.backup.$stamp" "$config/$component" || :
            fi
        done
    fi
    rm -rf -- "$stage"
    exit "$status"
}
trap rollback 0
trap 'exit 1' HUP INT TERM

for component in $components; do
    cp -a -- "$root/.config/$component" "$stage/$component"
done
for component in $components; do
    if [ -e "$config/$component" ] || [ -L "$config/$component" ]; then
        mv -- "$config/$component" "$config/$component.backup.$stamp"
        saved="$saved $component"
        printf 'Respaldo: %s\n' "$config/$component.backup.$stamp"
    fi
    mv -- "$stage/$component" "$config/$component"
    installed="$installed $component"
done

python "$config/qtile/scripts/theme-switch.py" "$theme" --no-reload
committed=1
printf '\nInstalación completada. Tema: %s\n' "$theme"
printf '%s\n' 'No se han instalado paquetes, habilitado servicios ni modificado SDDM/PAM.'
printf '%s\n' 'Verifica: qtile check -c ~/.config/qtile/config.py'
