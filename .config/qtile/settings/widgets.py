"""Operator HUD: clickable workspaces, live task switcher and status capsules.

All widgets are built per-screen (no widget object is reused across bars).
Colors are provided by the selected Obsidian/Cyberpunk/Darcula palette.
"""

import shlex
import sys
from pathlib import Path
from shutil import which

from libqtile import widget
from libqtile.lazy import lazy

from .theme import colors as C

FONT = "JetBrainsMono Nerd Font"
SCRIPTS = Path.home() / ".config" / "qtile" / "scripts"


def script(name):
    return f"/bin/sh {shlex.quote(str(SCRIPTS / name))}"


COMMAND = script("operator-menu.sh")
THEMES = script("theme-menu.sh")
POWER = script("power-menu.sh")
VPN_SCRIPT = SCRIPTS / "vpn-menu.py"
VPN = shlex.join([sys.executable, str(VPN_SCRIPT)])
BLACKARCH = shlex.join([sys.executable, str(SCRIPTS / "blackarch-menu.py")])

def space(length=10):
    return widget.Spacer(length=length)

def separator():
    return widget.Sep(
        linewidth=1, padding=12, size_percent=43,
        foreground=C["grey"], background=C["dark"],
    )

def action(text, command, *, foreground=None, size=13, padding=11):
    return widget.TextBox(
        text=text,
        font=FONT,
        fontsize=size,
        foreground=foreground or C["text"],
        background=C["dark"],
        padding=padding,
        mouse_callbacks={"Button1": lazy.spawn(command)},
    )

def launcher():
    return widget.TextBox(
        text="  OPS",
        font=FONT,
        fontsize=13,
        fontshadow=None,
        foreground=C["focus"],
        background=C["color1"],
        padding=15,
        mouse_callbacks={"Button1": lazy.spawn(COMMAND)},
    )

def workspace_widgets():
    return [
        widget.TextBox(
            text="DESKS", font=FONT, fontsize=10,
            foreground=C["inactive"], background=C["dark"], padding=9,
        ),
        widget.GroupBox(
            font=FONT, fontsize=11,
            background=C["dark"],
            foreground=C["text"],
            active=C["text"],
            inactive=C["inactive"],
            highlight_method="line",
            this_current_screen_border=C["focus"],
            this_screen_border=C["color4"],
            other_current_screen_border=C["grey"],
            other_screen_border=C["grey"],
            urgent_alert_method="block",
            urgent_border=C["urgent"],
            borderwidth=2,
            rounded=False,
            disable_drag=True,
            hide_unused=False,
            visible_groups=[str(i) for i in range(1, 9)],
            margin_x=1,
            margin_y=5,
            padding_x=7,
            padding_y=4,
            spacing=3,
        ),
    ]

def task_list():
    return widget.TaskList(
        font=FONT,
        fontsize=11,
        foreground=C["text"],
        background=C["dark"],
        icon_size=0,
        max_title_width=190,
        spacing=6,
        margin_x=3,
        margin_y=5,
        padding_x=9,
        padding_y=5,
        border=C["focus"],
        borderwidth=1,
        unfocused_border=C["grey"],
        urgent_border=C["urgent"],
        highlight_method="block",
        rounded=True,
        txt_floating="FLOAT ",
        txt_minimized="MIN ",
        txt_maximized="MAX ",
        stretch=True,
    )

def layout_status():
    return [
        widget.TextBox(
            text="LAYOUT", fontsize=10, font=FONT,
            foreground=C["inactive"], background=C["dark"], padding=6,
        ),
        widget.CurrentLayout(
            font=FONT, fontsize=12,
            foreground=C["color4"], background=C["dark"], padding=9,
            mouse_callbacks={"Button1": lazy.next_layout()},
        ),
    ]

def telemetry():
    return [
        widget.CPU(
            font=FONT, fontsize=11,
            format="CPU {load_percent:.0f}%",
            foreground=C["text"], background=C["dark"],
            update_interval=3, padding=8,
        ),
        widget.Memory(
            font=FONT, fontsize=11,
            format="RAM {MemPercent:.0f}%",
            foreground=C["text"], background=C["dark"],
            update_interval=5, padding=8,
        ),
        widget.Net(
            font=FONT, fontsize=11,
            interface=None,
            format="↓{down:.0f}{down_suffix}/s  ↑{up:.0f}{up_suffix}/s",
            foreground=C["text"], background=C["dark"],
            update_interval=3, padding=8,
        ),
    ]

def controls(primary):
    result = []
    if primary and which("checkupdates"):
        result.extend([
            separator(),
            widget.CheckUpdates(
                font=FONT, fontsize=11,
                distro="Arch_checkupdates",
                display_format="UPD {updates}",
                no_update_string="UPD 0",
                colour_have_updates=C["focus"],
                colour_no_updates=C["inactive"],
                background=C["dark"],
                update_interval=1800, padding=8,
            ),
        ])
    if primary:
        result.extend([
            separator(),
            widget.Systray(
                background=C["dark"], icon_size=17, padding=5,
            ),
        ])
    result.extend([
        separator(),
        widget.Clock(
            font=FONT, fontsize=12,
            format="%d/%m  %H:%M",
            foreground=C["light"], background=C["dark"],
            padding=11,
        ),
    ])
    if primary:
        result.extend([
            action("󰔎", THEMES, foreground=C["color4"], size=16),
            # Permanent clickable VPN icon (Nerd Fonts md-vpn, U+F0582).
            # Uses the same action widget as the theme chooser.
            action("󰖂", VPN, foreground=C["color4"], size=16),
            action("󰒃", BLACKARCH, foreground=C["focus"], size=16),
            action("⏻", POWER, foreground=C["focus"], size=18, padding=15),
        ])
    return result

def build_widgets(primary=False, compact=False):
    items = [launcher(), space(8), *workspace_widgets()]
    if not compact:
        items.extend([separator(), *layout_status(), separator(), task_list()])
        if primary:
            items.extend([separator(), *telemetry()])
    else:
        # Narrow secondary monitors prioritize workspace switching over telemetry.
        items.append(widget.Spacer())
    items.extend(controls(primary))
    return items

widget_defaults = {
    "font": FONT,
    "fontsize": 12,
    "foreground": C["text"],
    "background": C["dark"],
    "padding": 5,
}
extension_defaults = widget_defaults.copy()
