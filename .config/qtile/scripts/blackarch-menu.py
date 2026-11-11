#!/usr/bin/env python3
"""BlackArch Tool Center — installed-tool browser for Qtile X11.

Discover categories from *installed* pacman groups, not an outdated tool list.
Open package metadata or explicitly launch an installed executable. Never
install packages, request privileges, scan targets or interpret names as shell.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

GROUP_PREFIX = "blackarch-"
PACKAGE_NAME = re.compile(r"^[a-zA-Z0-9@._+:-]+$")
BIN_DIRS = frozenset(("/usr/bin", "/usr/sbin"))
ROFI_WIDTH = "window { width: 760px; } listview { lines: 12; }"

CATEGORY_NAMES = {
    "recon": "Reconocimiento",
    "scanner": "Escáneres",
    "webapp": "Aplicaciones web",
    "networking": "Redes",
    "wireless": "Redes inalámbricas",
    "sniffer": "Análisis de tráfico",
    "forensic": "Informática forense",
    "crypto": "Criptografía",
    "password": "Contraseñas",
    "reversing": "Ingeniería inversa",
    "binary": "Análisis de binarios",
    "debugger": "Depuración",
    "decompiler": "Descompilación",
    "disassembler": "Desensamblado",
    "fuzzer": "Fuzzing",
    "automation": "Automatización",
    "mobile": "Móviles",
    "database": "Bases de datos",
    "proxy": "Proxies",
    "tunnel": "Túneles",
    "exploitation": "Explotación",
    "malware": "Análisis de malware",
    "voip": "VoIP",
    "dos": "Pruebas de disponibilidad",
    "social": "Ingeniería social",
}


def run(*argv: str, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(argv), text=True, capture_output=True, check=False, timeout=timeout)


def notify(message: str, *, error: bool = False) -> None:
    if shutil.which("dunstify"):
        try:
            subprocess.run(
                ["dunstify", "-u", "critical" if error else "normal", "BlackArch", message],
                check=False, capture_output=True, timeout=3,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
    else:
        print(f"BlackArch: {message}", file=sys.stderr)


def installed_groups() -> dict[str, set[str]]:
    """Read locally installed pacman groups; no sync, root or network needed."""
    proc = run("pacman", "-Qg")
    if proc.returncode:
        raise RuntimeError("No se pudo leer la base de paquetes instalados de pacman.")
    groups: dict[str, set[str]] = {}
    general: set[str] = set()
    for line in proc.stdout.splitlines():
        fields = line.split(None, 1)
        if len(fields) != 2:
            continue
        group, package = fields
        if not PACKAGE_NAME.fullmatch(package):
            continue
        if group.startswith(GROUP_PREFIX):
            groups.setdefault(group[len(GROUP_PREFIX):], set()).add(package)
        elif group == "blackarch":
            general.add(package)

    # Keep tools with only the parent BlackArch group discoverable.
    classified = set().union(*groups.values()) if groups else set()
    unclassified = general - classified
    if unclassified:
        groups["otros"] = unclassified
    return groups


def choose(prompt: str, options: list[str]) -> str | None:
    if not options:
        return None
    response = subprocess.run(
        ["rofi", "-dmenu", "-i", "-no-custom", "-matching", "fuzzy",
         "-p", prompt, "-theme-str", ROFI_WIDTH],
        input="\n".join(options) + "\n",
        text=True, capture_output=True, check=False, timeout=240,
    )
    if response.returncode:
        return None
    selected = response.stdout.rstrip("\n")
    return selected if selected in options else None


def category_name(slug: str) -> str:
    return CATEGORY_NAMES.get(slug, slug.replace("-", " ").title())


def package_files(package: str) -> list[str]:
    if not PACKAGE_NAME.fullmatch(package):
        return []
    proc = run("pacman", "-Qlq", "--", package)
    return proc.stdout.splitlines() if proc.returncode == 0 else []


def executables(package: str) -> list[str]:
    found = set()
    for name in package_files(package):
        path = Path(name)
        if (
            str(path.parent) in BIN_DIRS
            and path.is_file()
            and os.access(path, os.X_OK)
        ):
            found.add(str(path))
    return sorted(found)


def open_terminal(*arguments: str) -> bool:
    if not shutil.which("alacritty"):
        notify("Alacritty no está instalado.", error=True)
        return False
    try:
        subprocess.Popen(
            ["alacritty", "-e", sys.executable, str(Path(__file__).resolve()), *arguments],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, start_new_session=True,
        )
        return True
    except OSError:
        notify("No se pudo abrir la terminal.", error=True)
        return False


def inspect(package: str, detail: str) -> int:
    if not PACKAGE_NAME.fullmatch(package) or detail not in {"info", "files"}:
        return 2
    args = ("pacman", "-Qi", "--", package) if detail == "info" else (
        "pacman", "-Ql", "--", package
    )
    try:
        proc = run(*args, timeout=10)
        print(f"\n  BLACKARCH / {package.upper()} / {detail.upper()}\n")
        print(proc.stdout if proc.returncode == 0 else "No se puede consultar el paquete.")
    except (OSError, subprocess.TimeoutExpired):
        print("Error consultando la base de paquetes.")
    try:
        input("\nPulsa Intro para cerrar...")
    except EOFError:
        pass
    return 0


def launch(package: str, path: str) -> int:
    """Launch selected packaged binary only, unprivileged and without shell."""
    if path not in executables(package):
        print("El ejecutable ya no pertenece al paquete indicado.", file=sys.stderr)
        return 2
    print(f"\n  BLACKARCH / {package.upper()}\n  Ejecutable: {path}\n")
    print("Se iniciará sin argumentos ni elevación de privilegios.\n")
    try:
        return subprocess.run([path], check=False).returncode
    except OSError as exc:
        print(f"No se pudo iniciar la herramienta: {exc}", file=sys.stderr)
        return 1
    finally:
        try:
            input("\nPulsa Intro para cerrar...")
        except EOFError:
            pass


def tool_actions(package: str) -> None:
    options = [
        "󰋽  Información del paquete",
        "󰋼  Archivos instalados",
        "󰆍  Seleccionar ejecutable y abrir terminal",
        "󰅖  Volver",
    ]
    selected = choose(f"HERRAMIENTA / {package[:32]}", options)
    if selected == options[0]:
        open_terminal("--inspect", "info", package)
    elif selected == options[1]:
        open_terminal("--inspect", "files", package)
    elif selected == options[2]:
        binaries = executables(package)
        if not binaries:
            notify(f"{package}: no hay ejecutables directamente en /usr/bin o /usr/sbin.")
            return
        binary = choose(f"EJECUTABLE / {package[:32]}", binaries)
        if binary is None:
            return
        confirmation = choose("CONFIRMAR EJECUCIÓN", [
            "Cancelar",
            "Ejecutar sin argumentos y sin sudo",
        ])
        if confirmation == "Ejecutar sin argumentos y sin sudo":
            open_terminal("--launch", package, binary)


def menu() -> int:
    if not shutil.which("rofi") or not shutil.which("pacman"):
        notify("Se necesitan Rofi y Pacman.", error=True)
        return 1
    try:
        groups = installed_groups()
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        notify("No se pudieron consultar las categorías instaladas de BlackArch.", error=True)
        return 1

    packages = set().union(*groups.values()) if groups else set()
    if not packages:
        notify("No se han detectado paquetes BlackArch instalados en grupos locales.")
        return 0

    categories = sorted(groups, key=lambda key: category_name(key).casefold())
    entries = [
        f"  Buscar herramientas instaladas  ·  {len(packages)}",
        f"󰋼  Todas las herramientas  ·  {len(packages)}",
    ]
    selections: dict[str, set[str]] = {
        entries[0]: packages,
        entries[1]: packages,
    }
    for slug in categories:
        label = f"󰒃  {category_name(slug)}  ·  {len(groups[slug])}"
        entries.append(label)
        selections[label] = groups[slug]

    while True:
        selected_group = choose("BLACKARCH / TOOL CENTER", entries)
        if selected_group is None:
            return 0
        group_packages = sorted(selections[selected_group])
        while True:
            tool = choose("BLACKARCH / HERRAMIENTAS", group_packages)
            if tool is None:
                break
            tool_actions(tool)


def main() -> int:
    parser = argparse.ArgumentParser(description="BlackArch Tool Center para Qtile")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--inspect", choices=("info", "files"))
    modes.add_argument("--launch", action="store_true")
    parser.add_argument("args", nargs="*")
    opts = parser.parse_args()
    if opts.inspect:
        if len(opts.args) != 1:
            parser.error("--inspect requiere exactamente un paquete")
        return inspect(opts.args[0], opts.inspect)
    if opts.launch:
        if len(opts.args) != 2:
            parser.error("--launch requiere paquete y ruta del ejecutable")
        return launch(*opts.args)
    if opts.args:
        parser.error("Argumentos inesperados")
    try:
        return menu()
    except (OSError, subprocess.TimeoutExpired):
        notify("Rofi o Pacman no responden.", error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
