# Qtile keybindings

from libqtile.config import Key
from libqtile.command import lazy

mod = "mod4"

keys = [Key(key[0], key[1], *key[2:]) for key in [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),
    ([mod], "k", lazy.layout.down()),
    ([mod], "j", lazy.layout.up()),
    ([mod], "space", lazy.layout.next()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    ([mod, "shift"], "h", lazy.layout.shuffle_left()),
    ([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ([mod, "shift"], "k", lazy.layout.shuffle_down()),
    ([mod, "shift"], "j", lazy.layout.shuffle_up()),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    ([mod, "control"], "h", lazy.layout.grow_left()),
    ([mod, "control"], "l", lazy.layout.grow_right()),
    ([mod, "control"], "k", lazy.layout.grow_down()),
    ([mod, "control"], "j", lazy.layout.grow_up()),
    ([mod], "n", lazy.layout.normalize()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    ([mod], "Return", lazy.spawn("alacritty")),
    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod], "w", lazy.window.kill()),
    ([mod, "control"], "r", lazy.reload_config()),
    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),

    # Apps
    ([mod], "a", lazy.spawn("android-studio")),
    ([mod], "b", lazy.spawn("firefox")),
    ([mod], "c", lazy.spawn("code")),
    ([mod], "i", lazy.spawn("gimp")),
    ([mod], "g", lazy.spawn("github-desktop")),
    ([mod], "o", lazy.spawn("libreoffice")),
    ([mod], "t", lazy.spawn("qbittorrent")),

    # File Explorer
    ([mod], 'e', lazy.spawn("Thunar")),

    # Menu
    ([mod], "m", lazy.spawn("ulauncher -show run")),
    ([mod, 'shift'], "m", lazy.spawn("ulauncher -show")),

    # Screenshot
    ([mod], "s", lazy.spawn("scrot")),
    ([mod, "shift"], "s", lazy.spawn("scrot -s")),

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]]