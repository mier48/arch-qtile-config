#!/usr/bin/env python3
"""Rofi VPN selector for NetworkManager profiles.

Only VPN and WireGuard NetworkManager profiles are shown. All mutations use
profile UUIDs as argv (never a shell), with no secrets or network requests.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass

UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
VPN_TYPES = {"vpn", "wireguard"}


@dataclass(frozen=True)
class Profile:
    uuid: str
    name: str
    type: str
    active: bool


def command(*args: str, timeout: int = 6) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["nmcli", *args], text=True, capture_output=True, timeout=timeout, check=False
    )


def notify(title: str, message: str, *, critical: bool = False) -> None:
    # No credentials or command stderr in notifications: NM could log secrets.
    if shutil.which("dunstify"):
        subprocess.run(
            ["dunstify", "-u", "critical" if critical else "normal", title, message],
            check=False, timeout=3,
        )
    else:
        print(f"{title}: {message}", file=sys.stderr)


def ids(active: bool = False) -> dict[str, str]:
    args = ("-t", "-f", "UUID,TYPE", "connection", "show")
    if active:
        args += ("--active",)
    result = command(*args, timeout=4)
    if result.returncode != 0:
        raise RuntimeError("NetworkManager no está disponible")
    found = {}
    for line in result.stdout.splitlines():
        parts = line.split(":", 1)
        if len(parts) == 2 and UUID.fullmatch(parts[0]) and parts[1].strip() in VPN_TYPES:
            found[parts[0].lower()] = parts[1].strip()
    return found


def profiles() -> list[Profile]:
    all_ids = ids()
    active_ids = ids(active=True)
    result = []
    for uuid, kind in all_ids.items():
        name_result = command("--escape", "no", "-g", "connection.id", "connection",
                              "show", "uuid", uuid, timeout=4)
        if name_result.returncode == 0:
            label = " ".join(name_result.stdout.split()).strip()
            if label:
                result.append(Profile(uuid, label, kind, uuid in active_ids))
    return sorted(result, key=lambda item: (not item.active, item.name.casefold(), item.uuid))


def status() -> str:
    try:
        count = len(ids(active=True))
        return f"VPN  ON ({count})" if count else "VPN  OFF"
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        return "VPN  ?"


def rofi(options: list[str]) -> str | None:
    process = subprocess.run(
        ["rofi", "-dmenu", "-i", "-no-custom", "-p", "VPN",
         "-theme-str", "window { width: 600px; } listview { lines: 9; }"],
        input="\n".join(options) + "\n",
        text=True, capture_output=True, check=False, timeout=120,
    )
    if process.returncode != 0:
        return None
    return process.stdout.rstrip("\n")


def menu() -> int:
    if not shutil.which("nmcli") or not shutil.which("rofi"):
        notify("VPN", "Necesitas NetworkManager (nmcli) y Rofi.", critical=True)
        return 1
    try:
        available = profiles()
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        notify("VPN", "No se pueden consultar los perfiles de NetworkManager.", critical=True)
        return 1

    if not available:
        notify("VPN", "No hay perfiles VPN/WireGuard importados en NetworkManager.")
        return 0

    # Stable index selects a UUID, not a potentially malicious or duplicate name.
    options = [
        ("●" if p.active else "○") + f"  {p.name[:60]}  [{p.type.upper()}]  ·  {p.uuid}"
        for p in available
    ]
    choice = rofi(options)
    if choice is None or choice not in options:
        return 0

    selected = available[options.index(choice)]
    action = ("down" if selected.active else "up")
    result = command(
        "--wait", "30", "connection", action, "uuid", selected.uuid, timeout=38
    )
    if result.returncode:
        notify("VPN", "No se pudo cambiar la VPN. Consulta NetworkManager o el agente de autenticación.", critical=True)
        return 1
    notify("VPN", ("Desconectada: " if selected.active else "Conectada: ") + selected.name[:80])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Selector VPN NetworkManager para Qtile")
    parser.add_argument("--status", action="store_true", help="Estado breve para Qtile")
    args = parser.parse_args()
    if args.status:
        print(status())
        return 0
    return menu()


if __name__ == "__main__":
    raise SystemExit(main())
