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
from . import system_state as state
from .popups import show_network_popup, show_system_popup

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

def vpn_indicator():
    """Original VPN icon: theme accent when WireGuard is active, grey otherwise."""
    def icon_markup():
        vpn = state.network_state().vpn
        color = C["focus"] if vpn is True else C["inactive"]
        return f'<span foreground="{color}">󰖂</span>'

    return widget.GenPollText(
        func=icon_markup, font=FONT, fontsize=16,
        foreground=C["inactive"], background=C["dark"],
        padding=11, update_interval=10, markup=True,
        mouse_callbacks={
            "Button1": lazy.spawn(VPN),
            "Button3": lazy.function(show_network_popup),
        },
    )


def system_button():
    return widget.TextBox(
        text="󰍛", font=FONT, fontsize=16,
        foreground=C["focus"], background=C["dark"],
        padding=11, mouse_callbacks={"Button1": lazy.function(show_system_popup)},
    )


def context_box():
    children = [
        widget.GenPollText(
            func=lambda: state.network_label(state.network_state()),
            font=FONT, fontsize=11, foreground=C["text"],
            background=C["dark"], padding=8, update_interval=10,
        ),
        widget.GenPollText(
            func=lambda: state.telemetry_label(state.telemetry()),
            font=FONT, fontsize=11, foreground=C["text"],
            background=C["dark"], padding=8, update_interval=15,
        ),
    ]
    if which("checkupdates"):
        children.append(
            widget.CheckUpdates(
                font=FONT, fontsize=11, distro="Arch_checkupdates",
                display_format="UPD {updates}", no_update_string="UPD 0",
                colour_have_updates=C["focus"],
                colour_no_updates=C["inactive"],
                background=C["dark"], update_interval=1800, padding=8,
            )
        )
    return widget.WidgetBox(
        widgets=children, font=FONT, fontsize=15,
        background=C["dark"], foreground=C["color4"],
        text_closed="󰅂", text_open="󰅀",
        padding=9, close_button_location="left",
        start_opened=False,
    )


def controls(primary):
    result = []
    if primary:
        result.extend([
            separator(),
            context_box(),
            system_button(),
            vpn_indicator(),
            separator(),
            widget.Systray(background=C["dark"], icon_size=17, padding=5),
        ])
    result.extend([
        separator(),
        widget.Clock(
            font=FONT, fontsize=12,
            format="%d/%m  %H:%M",
            foreground=C["light"], background=C["dark"], padding=11,
        ),
    ])
    if primary:
        result.extend([
            action("󰔎", THEMES, foreground=C["color4"], size=16),
            action("󰒃", BLACKARCH, foreground=C["focus"], size=16),
            action("⏻", POWER, foreground=C["focus"], size=18, padding=15),
        ])
    return result


def build_widgets(primary=False, compact=False):
    items = [launcher(), space(8), *workspace_widgets()]
    if not compact:
        items.extend([separator(), *layout_status(), separator(), task_list()])
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
