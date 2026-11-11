#!/bin/sh
# Explicit, opt-in system installation of a Qt6 SDDM theme.
# Does not enable SDDM, change PAM, or modify another display manager.
set -eu
umask 022

usage() {
    printf '%s\n' "Uso: sudo sh sddm/install-theme.sh {obsidian|cyberpunk|darcula}"
    exit 2
}
[ "$#" -eq 1 ] || usage
case "$1" in
    obsidian|cyberpunk|darcula) theme="$1" ;;
    *) usage ;;
esac
[ "$(id -u)" -eq 0 ] || { printf '%s\n' "Ejecutar con sudo." >&2; exit 1; }

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$SCRIPT_DIR/operator-hud"
dest="/usr/share/sddm/themes/operator-$theme"
conf="/etc/sddm.conf.d/90-operator-hud.conf"

for file in "$source_dir/Main.qml" "$source_dir/metadata.desktop" "$source_dir/themes/$theme.conf"; do
    [ -f "$file" ] || { printf 'Falta: %s\n' "$file" >&2; exit 1; }
done
command -v sddm >/dev/null 2>&1 || {
    printf '%s\n' 'SDDM no está instalado. Instala sddm (Qt 6) antes de continuar.' >&2
    exit 1
}

install -d -m 755 /usr/share/sddm/themes /etc/sddm.conf.d
if [ -e "$dest" ]; then
    if [ -L "$dest" ] || [ ! -d "$dest" ]; then
        printf 'Ruta insegura o incompatible: %s\n' "$dest" >&2
        exit 1
    fi
    backup="$dest.backup.$(date +%Y%m%d%H%M%S)"
    mv -- "$dest" "$backup"
    printf 'Copia del tema anterior: %s\n' "$backup"
fi
install -d -m 755 "$dest"
install -m 644 "$source_dir/Main.qml" "$dest/Main.qml"
install -m 644 "$source_dir/metadata.desktop" "$dest/metadata.desktop"
install -m 644 "$source_dir/themes/$theme.conf" "$dest/theme.conf"

if [ -L "$conf" ]; then
    printf 'No se sobrescribe un enlace simbólico: %s\n' "$conf" >&2
    exit 1
fi
if [ -f "$conf" ]; then
    cp -p -- "$conf" "$conf.backup.$(date +%Y%m%d%H%M%S)"
fi
tmp=$(mktemp /etc/sddm.conf.d/.operator-hud.XXXXXXXX)
trap 'rm -f "$tmp"' EXIT HUP INT TERM
printf '[Theme]\nCurrent=operator-%s\n' "$theme" > "$tmp"
chmod 644 "$tmp"
mv -f "$tmp" "$conf"

printf '%s\n' "Tema instalado: operator-$theme"
printf '%s\n' "No se ha habilitado ni reiniciado SDDM; no se ha modificado PAM."
printf '%s\n' "Prueba el greeter antes de activar SDDM. Consulta sddm/README.md."
