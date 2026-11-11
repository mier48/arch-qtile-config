#!/bin/sh
# Validate the locking chain before allowing a suspend from the power menu.
set -eu
for cmd in i3lock xss-lock loginctl; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        printf 'Falta: %s\n' "$cmd" >&2
        exit 1
    fi
done
# Check that the current user's xss-lock daemon exists; no kill or restart.
pgrep -u "$(id -u)" -x xss-lock >/dev/null 2>&1 || {
    printf '%s\n' 'xss-lock no está activo. No suspendas desde este menú.' >&2
    exit 1
}
