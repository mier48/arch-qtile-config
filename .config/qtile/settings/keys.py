"""Qtile Operator HUD shortcuts: keyboard-first window control."""

import shlex
import sys
from pathlib import Path

from libqtile.config import Key
from libqtile.lazy import lazy

mod = "mod4"

SCRIPTS = Path.home() / ".config" / "qtile" / "scripts"


def script(name):
    return f"/bin/sh {shlex.quote(str(SCRIPTS / name))}"


keys = [
    # Focus and cycle through windows.
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "space", lazy.layout.next()),

    # Reorder windows.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # Resize in supported layouts.
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], "n", lazy.layout.normalize()),

    # Window management and applications.
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawn("rofi -show run")),

    Key([mod], "a", lazy.spawn("android-studio")),
    Key([mod], "b", lazy.spawn("firefox")),
    Key([mod], "c", lazy.spawn("code")),
    Key([mod], "i", lazy.spawn("gimp")),
    Key([mod], "g", lazy.spawn("github-desktop")),
    Key([mod], "o", lazy.spawn("libreoffice")),
    Key([mod], "t", lazy.spawn("qbittorrent")),

    # Operator HUD / window state / navigation.
    Key([mod], "p", lazy.spawn(script("operator-menu.sh"))),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    Key([mod], "Escape", lazy.screen.toggle_group()),
    Key([mod], "bracketleft", lazy.screen.prev_group()),
    Key([mod], "bracketright", lazy.screen.next_group()),

    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    Key([mod, "shift"], "t", lazy.spawn(script("theme-menu.sh"))),
    Key([mod, "shift"], "v", lazy.spawn(shlex.join([sys.executable, str(SCRIPTS / "vpn-menu.py")]))),
    Key([mod, "shift"], "p", lazy.spawn(script("power-menu.sh"))),
    Key([mod, "shift"], "n", lazy.spawn("dunstctl history-pop")),
    Key([mod, "shift"], "m", lazy.spawn("rofi -show window")),

    # Screenshots: full and selection (X11).
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),

    # Audio: requires a PulseAudio-compatible server.
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Only works where brightnessctl supports the hardware.
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]
