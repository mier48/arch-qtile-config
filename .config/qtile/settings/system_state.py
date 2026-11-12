"""Read-only local state for the Operator HUD.

No public-IP lookups, shell evaluation, privilege escalation or network requests.
NetworkManager is authoritative only for connections that it manages. A WireGuard
connection managed by wg-quick is therefore deliberately not counted as active.

All costly reads happen in GenPollText worker threads, are time-bounded and
shared via a small thread-safe monotonic cache. Popup callbacks use peek_* only,
so clicking the bar never waits for a driver or NetworkManager subprocess.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

try:
    import psutil
except ImportError:  # Allows the diagnostic module to work before Qtile is installed.
    psutil = None

T = TypeVar("T")
_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, tuple[float, object]] = {}
_CACHE_TTL = 12.0
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


@dataclass(frozen=True)
class NetworkState:
    vpn: bool | None = None
    connected: bool | None = None
    interface: str = "—"
    medium: str = "Desconocido"


@dataclass(frozen=True)
class Telemetry:
    cpu_percent: float | None = None
    memory_percent: float | None = None
    cpu_temp_c: float | None = None
    gpu_percent: float | None = None
    gpu_temp_c: float | None = None
    gpu_memory_mib: float | None = None


def _cached(key: str, producer: Callable[[], T], seconds: float = _CACHE_TTL) -> T:
    # Never hold a lock while querying NetworkManager or the GPU driver.
    with _CACHE_LOCK:
        entry = _CACHE.get(key)
        if entry is not None and time.monotonic() - entry[0] < seconds:
            return entry[1]  # type: ignore[return-value]
    result = producer()
    with _CACHE_LOCK:
        _CACHE[key] = (time.monotonic(), result)
    return result


def _peek(key: str) -> object | None:
    with _CACHE_LOCK:
        entry = _CACHE.get(key)
        return None if entry is None else entry[1]


def _command(*args: str, timeout: float = 2.5) -> str | None:
    if not shutil.which(args[0]):
        return None
    try:
        env = dict(os.environ, LC_ALL="C")
        process = subprocess.run(
            args, env=env, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return process.stdout if process.returncode == 0 else None


def _read_network() -> NetworkState:
    connections = _command(
        "nmcli", "-t", "-f", "UUID,TYPE", "connection", "show", "--active"
    )
    devices = _command("nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device", "status")

    vpn: bool | None = None
    if connections is not None:
        vpn = any(
            (parts := line.split(":")) and len(parts) == 2
            and bool(_UUID.fullmatch(parts[0]))
            and parts[1].strip().lower() == "wireguard"
            for line in connections.splitlines()
        )

    if devices is None:
        return NetworkState(vpn=vpn)

    for line in devices.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        interface, medium, state = parts
        if medium not in {"ethernet", "wifi"}:
            continue
        if state.lower().startswith("connected"):
            return NetworkState(
                vpn=vpn,
                connected=True,
                interface=interface[:24] or "—",
                medium="Ethernet" if medium == "ethernet" else "Wi-Fi",
            )
    return NetworkState(vpn=vpn, connected=False, medium="Sin conexión")


def network_state() -> NetworkState:
    return _cached("network", _read_network)


def peek_network() -> NetworkState:
    value = _peek("network")
    return value if isinstance(value, NetworkState) else NetworkState()


def _parse_number(text: str) -> float | None:
    try:
        return float(text.strip())
    except (ValueError, TypeError):
        return None


def _cpu_temperature() -> float | None:
    if psutil is None:
        return None
    try:
        sensors = psutil.sensors_temperatures(fahrenheit=False)
        for name in ("coretemp", "k10temp", "zenpower", "cpu_thermal"):
            for sensor in sensors.get(name, ()):
                label = sensor.label.lower()
                if name == "coretemp" and label and "package" not in label:
                    continue
                temp = float(sensor.current)
                if -10 <= temp <= 125:
                    return temp
    except (AttributeError, OSError, NotImplementedError, ValueError):
        pass
    return None


def _read_telemetry() -> Telemetry:
    cpu = memory = None
    if psutil is not None:
        try:
            cpu = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory().percent
        except (OSError, RuntimeError):
            pass

    gpu_percent = gpu_temp = gpu_memory = None
    result = _command(
        "nvidia-smi", "--id=0",
        "--query-gpu=utilization.gpu,temperature.gpu,memory.used",
        "--format=csv,noheader,nounits", timeout=2.0,
    )
    if result is not None:
        first = result.splitlines()
        parts = first[0].split(",") if first else []
        if len(parts) >= 3:
            gpu_percent, gpu_temp, gpu_memory = map(_parse_number, parts[:3])

    return Telemetry(
        cpu_percent=cpu,
        memory_percent=memory,
        cpu_temp_c=_cpu_temperature(),
        gpu_percent=gpu_percent,
        gpu_temp_c=gpu_temp,
        gpu_memory_mib=gpu_memory,
    )


def telemetry() -> Telemetry:
    return _cached("telemetry", _read_telemetry, seconds=15.0)


def peek_telemetry() -> Telemetry:
    value = _peek("telemetry")
    return value if isinstance(value, Telemetry) else Telemetry()


def _metric(value: float | None, *, unit: str = "%") -> str:
    return "—" if value is None else f"{value:.0f}{unit}"


def network_label(value: NetworkState) -> str:
    if value.connected is None:
        return "RED ?"
    if not value.connected:
        return "RED OFF"
    return f"{value.medium.upper()} {value.interface}"


def vpn_label(value: NetworkState) -> str:
    if value.vpn is None:
        return "WG/NM ?"
    return "WG/NM ON" if value.vpn else "WG/NM OFF"


def telemetry_label(value: Telemetry) -> str:
    return (
        f"CPU {_metric(value.cpu_percent)} "
        f"· RAM {_metric(value.memory_percent)} "
        f"· TCPU {_metric(value.cpu_temp_c, unit='°C')} "
        f"· GPU {_metric(value.gpu_percent)} / {_metric(value.gpu_temp_c, unit='°C')}"
    )
