#!/usr/bin/env python3
"""Atomically switch the complete Qtile X11 theme stack.

Usage: python ~/.config/qtile/scripts/theme-switch.py <obsidian|cyberpunk|darcula>
       python ~/.config/qtile/scripts/theme-switch.py --list
       python ~/.config/qtile/scripts/theme-switch.py --current
       python ~/.config/qtile/scripts/theme-switch.py darcula --no-reload
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HOME = Path.home()
CONFIG = HOME / ".config"
QTILE = CONFIG / "qtile"
THEMES = ("obsidian", "cyberpunk", "darcula")
TARGETS = (
    ("alacritty", "themes/{name}.toml", "themes/active.toml"),
    ("rofi", "themes/{name}.rasi", "themes/active.rasi"),
    ("fish", "themes/{name}.fish", "conf.d/theme.fish"),
    ("fastfetch", "themes/{name}.jsonc", "config.jsonc"),
    ("dunst", "themes/{name}.conf", "dunstrc"),
    ("picom", "themes/{name}.conf", "picom.conf"),
)


def current() -> str:
    try:
        return json.loads((QTILE / "config.json").read_text(encoding="utf-8"))["theme"]
    except (OSError, KeyError, ValueError):
        return "obsidian"


def atomic_copy(source: Path, dest: Path) -> None:
    data = source.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=dest.parent, prefix=".theme-", delete=False) as fh:
            temp_path = Path(fh.name)
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, dest)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def atomic_text(data: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=dest.parent,
            prefix=".theme-", delete=False
        ) as fh:
            temp_path = Path(fh.name)
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, dest)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def checked_source(component: str, source: str, name: str) -> Path:
    result = CONFIG / component / source.format(name=name)
    if not result.is_file():
        raise FileNotFoundError(result)
    return result


def change(name: str, reload_desktop: bool) -> None:
    if name not in THEMES:
        raise ValueError(f"Tema desconocido: {name}")

    # Preflight all sources before modifying the active configuration.
    candidates = [
        (checked_source(component, template, name), CONFIG / component / target)
        for component, template, target in TARGETS
    ]
    qtile_palette = QTILE / "themes" / f"{name}.json"
    wallpaper = QTILE / "wallpapers" / f"{name}.svg"
    if not qtile_palette.is_file() or not wallpaper.is_file():
        raise FileNotFoundError("Falta la paleta Qtile o el fondo del tema.")
    json.loads(qtile_palette.read_text(encoding="utf-8"))
    json.loads((CONFIG / "fastfetch" / "themes" / f"{name}.jsonc").read_text(encoding="utf-8"))

    for src, dst in candidates:
        atomic_copy(src, dst)
    # Change Qtile last; its selected theme is the authoritative state.
    atomic_text(json.dumps({"theme": name}, indent=2) + "\n", QTILE / "config.json")
    print(f"Tema activo: {name}")

    if reload_desktop and os.environ.get("DISPLAY"):
        wallpaper_script = QTILE / "scripts" / "wallpaper.sh"
        if wallpaper_script.is_file():
            subprocess.run(["/bin/sh", str(wallpaper_script)], check=False)

        if shutil.which("dunstctl"):
            subprocess.run(["dunstctl", "reload"], check=False, timeout=5)

        # Restart only our own Picom when already running.
        if shutil.which("pgrep") and shutil.which("picom"):
            found = subprocess.run(
                ["pgrep", "-u", str(os.getuid()), "-x", "picom"],
                capture_output=True, check=False
            )
            if found.returncode == 0:
                for line in found.stdout.decode().splitlines():
                    try:
                        os.kill(int(line), signal.SIGTERM)
                    except (ProcessLookupError, PermissionError, ValueError):
                        pass
                # Picom will be restarted after Qtile reload by the helper below.
                subprocess.Popen(
                    ["/bin/sh", "-c", 'sleep 0.4; exec picom --config "$HOME/.config/picom/picom.conf"'],
                    start_new_session=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

        if shutil.which("qtile"):
            subprocess.run(
                ["qtile", "cmd-obj", "-o", "cmd", "-f", "reload_config"],
                check=False, timeout=8
            )
        print("Fish: abre una terminal nueva. Alacritty recarga los colores automáticamente.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cambiar los temas del escritorio Qtile")
    parser.add_argument("theme", nargs="?", choices=THEMES)
    parser.add_argument("--list", action="store_true", help="Listar temas")
    parser.add_argument("--current", action="store_true", help="Mostrar el tema actual")
    parser.add_argument("--no-reload", action="store_true", help="No recargar la sesión gráfica")
    args = parser.parse_args()
    if args.list:
        print("\n".join(THEMES))
    elif args.current or not args.theme:
        print(current())
    else:
        try:
            change(args.theme, not args.no_reload)
        except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
            print(f"Error cambiando el tema: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
