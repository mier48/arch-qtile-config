"""Operator HUD 2.0: on-demand Qtile Extras popups.

Qtile 0.37 / qtile-extras 0.37: no persistent popup, no blocking NM or
nvidia-smi calls in the main UI thread. All labels use cached local data;
the optional graphs use Qtile's native polling widgets.
"""
from __future__ import annotations

from libqtile import widget
from libqtile.lazy import lazy

from . import system_state as state
from .theme import colors as C

try:
    from qtile_extras.popup import PopupRelativeLayout, PopupText, PopupWidget
except ImportError:
    PopupRelativeLayout = None
    PopupText = None
    PopupWidget = None

FONT = "JetBrainsMono Nerd Font"


def _label(text: str, x: float, y: float, width: float,
           *, color: str | None = None, size: int = 12, height: float = 0.13):
    return PopupText(
        text=text,
        pos_x=x, pos_y=y, width=width, height=height,
        font=FONT, fontsize=size, foreground=color or C["text"],
        v_align="middle",
    )


def _format(value: float | None, unit: str) -> str:
    return "—" if value is None else f"{value:.0f}{unit}"


def _unavailable(qtile) -> bool:
    if PopupRelativeLayout is not None:
        return False
    # Safe fallback: show local data in a native Qtile notification if extras absent.
    qtile.spawn("dunstify 'Operator HUD' 'Instala qtile-extras 0.37 para activar los popups'")
    return True


def show_network_popup(qtile):
    """Display NetworkManager connection status; never imply VPN anonymity."""
    if _unavailable(qtile):
        return
    info = state.peek_network()
    vpn = state.vpn_label(info)
    network = state.network_label(info)
    accent = C["focus"] if info.vpn else C["inactive"]
    controls = [
        _label("NETWORK / OPERATOR", .06, .07, .88, color=C["focus"], size=15),
        _label("CONEXIÓN LOCAL", .06, .29, .39, color=C["inactive"]),
        _label(network, .46, .29, .50, color=C["light"], size=12),
        _label("WIREGUARD", .06, .50, .39, color=C["inactive"]),
        _label(vpn, .46, .50, .50, color=accent, size=12),
        _label("Solo NetworkManager · sin consultar IP pública", .06, .74, .90,
               color=C["inactive"], size=10),
    ]
    popup = PopupRelativeLayout(
        qtile, width=500, height=260,
        background=C["color1"], border=C["grey"], border_width=1,
        controls=controls, initial_focus=None,
        close_on_click=True,
    )
    popup.show(relative_to=3, relative_to_bar=True)


def show_system_popup(qtile):
    """Show cached local snapshots and graph widgets only when requested."""
    if _unavailable(qtile):
        return
    data = state.peek_telemetry()
    details = [
        ("CPU", _format(data.cpu_percent, "%")),
        ("MEMORIA", _format(data.memory_percent, "%")),
        ("TEMP CPU", _format(data.cpu_temp_c, "°C")),
        ("NVIDIA GPU", _format(data.gpu_percent, "%")),
        ("TEMP GPU", _format(data.gpu_temp_c, "°C")),
        ("VRAM GPU", _format(data.gpu_memory_mib, " MiB")),
    ]
    controls = [
        _label("SYSTEM / LOCAL TELEMETRY", .045, .035, .91,
               color=C["focus"], size=16, height=.09),
    ]
    for index, (title, value) in enumerate(details):
        col, row = index // 3, index % 3
        x = .05 + col * .48
        y = .16 + row * .11
        controls.extend([
            _label(title, x, y, .25, color=C["inactive"], size=11, height=.09),
            _label(value, x + .26, y, .19, color=C["light"], size=12, height=.09),
        ])

    controls.extend([
        _label("CPU / HISTORIAL", .05, .54, .44, color=C["focus"], size=11, height=.07),
        _label("RAM / HISTORIAL", .54, .54, .44, color=C["focus"], size=11, height=.07),
        PopupWidget(
            widget=widget.CPUGraph(graph_color=C["focus"], fill_color=C["color2"],
                                   background=C["color1"], update_interval=3),
            pos_x=.05, pos_y=.63, width=.44, height=.23,
        ),
        PopupWidget(
            widget=widget.MemoryGraph(graph_color=C["color4"], fill_color=C["color2"],
                                      background=C["color1"], update_interval=5),
            pos_x=.53, pos_y=.63, width=.44, height=.23,
        ),
        _label("Lecturas locales · los guiones indican sensor no disponible",
               .05, .88, .91, color=C["inactive"], size=10, height=.08),
    ])
    popup = PopupRelativeLayout(
        qtile, width=750, height=500,
        background=C["color1"], border=C["grey"], border_width=1,
        controls=controls, initial_focus=None, close_on_click=False,
        hide_on_timeout=15,
    )
    popup.show(centered=True)
