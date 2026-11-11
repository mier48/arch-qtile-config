"""Obsidian bar: consistent typography, restrained colors and useful metrics."""

from shutil import which

from libqtile import widget
from libqtile.lazy import lazy

from .theme import colors

FONT = "JetBrainsMono Nerd Font"
C = colors


def separator():
    return widget.Sep(
        linewidth=1,
        padding=13,
        size_percent=44,
        foreground=C["grey"],
        background=C["dark"],
    )


def left_widgets():
    return [
        widget.TextBox(
            text="",
            font=FONT,
            fontsize=19,
            foreground=C["focus"],
            background=C["dark"],
            padding=15,
            mouse_callbacks={"Button1": lazy.spawn("rofi -show drun")},
        ),
        widget.GroupBox(
            font=FONT,
            fontsize=12,
            background=C["dark"],
            foreground=C["light"],
            active=C["text"],
            inactive=C["inactive"],
            highlight_method="block",
            block_highlight_text_color=C["dark"],
            this_current_screen_border=C["focus"],
            this_screen_border=C["color4"],
            other_current_screen_border=C["grey"],
            other_screen_border=C["grey"],
            urgent_alert_method="block",
            urgent_border=C["urgent"],
            borderwidth=1,
            rounded=True,
            disable_drag=True,
            margin_x=2,
            margin_y=4,
            padding_x=9,
            padding_y=5,
            spacing=4,
        ),
        widget.Spacer(length=18),
        widget.WindowName(
            font=FONT,
            fontsize=12,
            foreground=C["inactive"],
            background=C["dark"],
            max_chars=58,
            padding=7,
            empty_group_string="",
        ),
        widget.Spacer(),
    ]


def right_widgets(primary=False):
    result = [
        widget.CurrentLayout(
            font=FONT,
            fontsize=12,
            foreground=C["color4"],
            background=C["dark"],
            padding=8,
        ),
        separator(),
        widget.CPU(
            font=FONT,
            fontsize=12,
            format="CPU {load_percent:.0f}%",
            foreground=C["text"],
            background=C["dark"],
            update_interval=3,
            padding=9,
        ),
        widget.Memory(
            font=FONT,
            fontsize=12,
            format="RAM {MemPercent:.0f}%",
            foreground=C["text"],
            background=C["dark"],
            update_interval=5,
            padding=9,
        ),
        separator(),
        widget.Net(
            font=FONT,
            fontsize=12,
            interface=None,
            format="↓ {down:.0f}{down_suffix}/s  ↑ {up:.0f}{up_suffix}/s",
            foreground=C["text"],
            background=C["dark"],
            update_interval=3,
            padding=9,
        ),
    ]

    if primary and which("checkupdates"):
        result.extend([
            separator(),
            widget.CheckUpdates(
                font=FONT,
                fontsize=12,
                distro="Arch_checkupdates",
                display_format="UPD {updates}",
                no_update_string="UPD 0",
                colour_have_updates=C["focus"],
                colour_no_updates=C["inactive"],
                background=C["dark"],
                update_interval=1800,
                padding=7,
            ),
        ])

    # One Systray across all X11 monitors.
    if primary:
        result.extend([
            separator(),
            widget.Systray(
                background=C["dark"],
                icon_size=18,
                padding=5,
            ),
        ])

    result.extend([
        separator(),
        widget.Clock(
            font=FONT,
            fontsize=13,
            format="%d/%m  %H:%M",
            foreground=C["light"],
            background=C["dark"],
            padding=12,
        ),
        widget.TextBox(
            text="󰔎",
            font=FONT,
            fontsize=16,
            foreground=C["color4"],
            background=C["dark"],
            padding=10,
            mouse_callbacks={"Button1": lazy.spawn("/bin/sh ~/.config/qtile/scripts/theme-menu.sh")},
        ),
        widget.TextBox(
            text="⏻",
            font=FONT,
            fontsize=18,
            foreground=C["focus"],
            background=C["dark"],
            padding=14,
            mouse_callbacks={
                "Button1": lazy.spawn("/bin/sh ~/.config/qtile/scripts/power-menu.sh"),
            },
        ),
    ])
    return result


def build_widgets(primary=False):
    return [*left_widgets(), *right_widgets(primary=primary)]


primary_widgets = build_widgets(primary=True)
secondary_widgets = build_widgets(primary=False)

widget_defaults = {
    "font": FONT,
    "fontsize": 12,
    "foreground": C["text"],
    "background": C["dark"],
    "padding": 5,
}
extension_defaults = widget_defaults.copy()
