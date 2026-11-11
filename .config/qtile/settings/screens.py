"""Qtile X11 monitor detection and independent Operator HUD bars."""

import re
import subprocess

from libqtile import bar
from libqtile.config import Screen

from .theme import colors
from .widgets import build_widgets

BAR_BACKGROUND = colors["dark"]
BAR_BORDER = colors["grey"]


def monitor_widths():
    """Get logical monitor widths from xrandr; fall back safely if unavailable."""
    try:
        process = subprocess.run(
            ["xrandr", "--listmonitors"],
            capture_output=True, text=True, timeout=3, check=False,
        )
        if process.returncode == 0:
            sizes = []
            for line in process.stdout.splitlines()[1:]:
                match = re.search(r"(\d+)/\d+x\d+/\d+\+\d+\+\d+", line)
                if match:
                    sizes.append(int(match.group(1)))
            if sizes:
                return sizes
    except (OSError, subprocess.TimeoutExpired):
        pass
    return [1920]


def status_bar(*, primary, compact):
    return bar.Bar(
        build_widgets(primary=primary, compact=compact),
        44,
        background=BAR_BACKGROUND,
        opacity=1.0,
        margin=[10, 12, 0, 12],
        border_width=[1, 1, 1, 1],
        border_color=BAR_BORDER,
    )


screens = [
    Screen(top=status_bar(primary=i == 0, compact=width < 1800))
    for i, width in enumerate(monitor_widths())
]
