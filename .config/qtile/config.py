"""Qtile Obsidian — modular X11 configuration."""

from pathlib import Path
import subprocess
from libqtile import hook
from settings.keys import mod, keys
from settings.groups import groups
from settings.layouts import layouts, floating_layout
from settings.widgets import widget_defaults, extension_defaults
from settings.screens import screens
from settings.mouse import mouse
from settings.path import qtile_path

@hook.subscribe.startup_once
def autostart():
    script = Path(qtile_path) / "autostart.sh"
    if script.is_file():
        subprocess.Popen(["/bin/sh", str(script)], start_new_session=True)

main = None
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "urgent"
wmname = "LG3D"
