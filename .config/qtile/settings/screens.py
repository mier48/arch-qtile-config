"""Qtile X11 monitor detection and per-screen bars."""

import re
import subprocess

from libqtile import bar
from libqtile.config import Screen

from .theme import colors
from .widgets import primary_widgets, secondary_widgets, build_widgets

BAR_BACKGROUND = colors["dark"]
BAR_BORDER = colors["grey"]


def monitor_count():
    try:
        process = subprocess.run(
            ["xrandr", "--listmonitors"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if process.returncode == 0:
            match = re.search(r"^Monitors:\s*(\d+)", process.stdout, re.M)
            if match:
                return max(1, int(match.group(1)))
    except (OSError, subprocess.TimeoutExpired):
        pass
    return 1


def status_bar(widgets):
    return bar.Bar(
        widgets,
        38,
        background=BAR_BACKGROUND,
        opacity=1.0,
        margin=[9, 12, 0, 12],
        border_width=[1, 1, 1, 1],
        border_color=BAR_BORDER,
    )


screens = [Screen(top=status_bar(primary_widgets))]
for index in range(1, monitor_count()):
    widgets = secondary_widgets if index == 1 else build_widgets(primary=False)
    screens.append(Screen(top=status_bar(widgets)))
