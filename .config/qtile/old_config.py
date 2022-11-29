# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
#terminal = guess_terminal()
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "j", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "j", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Apps
    Key([mod], "a", lazy.spawn("android-studio")),
    Key([mod], "b", lazy.spawn("firefox")),
    Key([mod], "c", lazy.spawn("code")),

    # File Explorer
    Key([mod], 'e', lazy.spawn("Thunar")),

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show run")),
    Key([mod, 'shift'], "m", lazy.spawn("rofi -show")),

    # Screenshot
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),
    #([mod], "s", lazy.spawn("scrot")),
    #([mod, "shift"], "s", lazy.spawn("scrot -s")),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

#groups = [Group(i) for i in "123456789"]
groups = [Group(i) for i in ["  ", "  ", " ", " "]]


for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

#for i in groups:
#    keys.extend(
#        [
#            # mod1 + letter of group = switch to group
#            Key(
#                [mod],
#                i.name,
#                lazy.group[i.name].toscreen(),
#                desc="Switch to group {}".format(i.name),
#            ),
#            # mod1 + shift + letter of group = switch to & move focused window to group
#            Key(
#                [mod, "shift"],
#                i.name,
#                lazy.window.togroup(i.name, switch_group=True),
#                desc="Switch to & move focused window to group {}".format(i.name),
#            ),
#            # Or, use below if you prefer not to switch to that group.
#            # # mod1 + shift + letter of group = move focused window to group
#            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#            #     desc="move focused window to group {}".format(i.name)),
#        ]
#    )

layout_conf = {
    'border_focus': "ff6188",
    'border_width': 1,
    'margin': 4
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='mononoki Nerd Font',
    fontsize=14,
    padding=1,
)
extension_defaults = widget_defaults.copy()

#screens = [Screen(top=status_bar(primary_widgets))]
#xrandr = "xrandr | grep -w 'connected' | cut -d ' ' -f 2 | wc -l"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground="#f1ffff",
                    background="#0f101a",
                    font='mononoki Nerd Font',
                    fontsize=20,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active="#f1ffff",
                    inactive="#f1ffff",
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border="#F07178",
                    this_current_screen_border="#a151d3",
                    this_screen_border="#353c4a",
                    other_current_screen_border="#0f101a",
                    other_screen_border="#0f101a",
                    disable_drag=True
                ),
                widget.Sep(
                    background=["#0f101a", "#0f101a"],
                    linewidth=0,
                    padding=5,
                ),
                widget.WindowName(
                    background=["#0f101a", "#0f101a"],
                    foreground=["#F07178", "#F07178"],
                    fontsize=14,
                    font='UbuntuMono Nerd Font Bold',
                ),
                widget.Sep(
                    background=["#0f101a", "#0f101a"],
                    linewidth=0,
                    padding=5,
                ),
                widget.TextBox(
                    foreground=["#ab9df2", "#ab9df2"],
                    text="",
                    fontsize=37,
                    padding=-4
                ),
                widget.TextBox(
                    text=" ",
                    background=["#ab9df2", "#ab9df2"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=5,
                ),
                widget.CheckUpdates(
                    background=["#ab9df2", "#ab9df2"],
                    colour_no_updates=["#0f101a", "#0f101a"],
                    colour_have_updates=["#0f101a", "#0f101a"],
                    no_update_string='0',
                    display_format='{updates}',
                    update_interval=1800,
                    custom_command='checkupdates',
                ),
                widget.Sep(
                    background=["#ab9df2", "#ab9df2"],
                    linewidth=0,
                    padding=5,
                ),
                widget.TextBox(
                    foreground=["#ff6188", "#ff6188"],
                    text="",
                    fontsize=37,
                    padding=-4
                ),
                widget.TextBox(
                    text=" ",
                    background=["#ff6188", "#ff6188"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=5,
                ),
                widget.Net(
                    background=["#ff6188", "#ff6188"],
                    foreground=["#0f101a", "#0f101a"],
                ),
                widget.Sep(
                    background=["#ff6188", "#ff6188"],
                    linewidth=0,
                    padding=5,
                ),
                widget.TextBox(
                    foreground=["#ffd866", "#ffd866"],
                    text="",
                    fontsize=37,
                    padding=-4
                ),
                widget.CurrentLayoutIcon(
                    background=["#ffd866", "#ffd866"],
                    foreground=["#0f101a", "#0f101a"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    background=["#ffd866", "#ffd866"],
                    foreground=["#0f101a", "#0f101a"],
                ),
                widget.Sep(
                    background=["#ffd866", "#ffd866"],
                    linewidth=0,
                    padding=5,
                ),
                widget.TextBox(
                    foreground=["#a9dc76", "#a9dc76"],
                    text="",
                    fontsize=37,
                    padding=-4
                ),
                widget.TextBox(
                    text="'",
                    background=["#a9dc76", "#a9dc76"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=5,
                ),
                widget.Clock(
                    background=["#a9dc76", "#a9dc76"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=5,
                    format='%d/%m/%Y - %H:%M',
                ),
                widget.TextBox(
                    foreground=["#0f101a", "#0f101a"],
                    text="",
                    fontsize=37,
                    padding=-3
                ),
                widget.Systray(
                    background=["#0f101a", "#0f101a"],
                ),
                #widget.GroupBox(
                #    foreground="#f1ffff",
                #    background="#0f101a",
                #    fontsize=20,
                #    margin_y=3,
                #    margin_x=0,
                #    padding_y=8,
                #    padding_x=5,
                #    borderwidth=1,
                #    active="#f1ffff",
                #    inactive="#f1ffff",
                #    rounded=False,
                #    highlight_method='block',
                #    urgent_alert_method='block',
                #    urgent_border="#F07178",
                #    this_current_screen_border="#a151d3",
                #    this_screen_border="#353c4a",
                #    other_current_screen_border="#0f101a",
                #    other_screen_border="#0f101a",
                #    disable_drag=True
                #),
                #widget.Sep(
                #    linewidth=0,
                #    padding=5,
                #),
                #widget.WindowName(
                #    fontsize=14,
                #),
                #widget.Sep(
                #    linewidth=0,
                #    padding=5,
                #),
                #widget.KhalCalendar(),
                #widget.CapsNumLockIndicator(),
                #widget.CheckUpdates(
                #    colour_no_updates=["#ffffff", "#ffffff"],
                #    colour_have_updates=["#ffffff", "#ffffff"],
                #    no_update_string='0',
                #    display_format='{updates}',
                #    update_interval=1800,
                #    custom_command='checkupdates',
                #),
                #widget.Sep(
                #    linewidth=0,
                #    padding=5,
                #),
                #widget.Net(
                #),
                #widget.Sep(
                #    linewidth=0,
                #    padding=5,
                #),
                #widget.CurrentLayoutIcon(
                #    scale=0.65
                #),
                #widget.CurrentLayout(
                #),
                #widget.Clock(format='%d/%m/%Y - %H:%M'),
                #widget.Sep(
                #    linewidth=0,
                #    padding=5,
                #),
                #widget.ThermalSensor(
                #    format='{temp:.0f}{unit}', 
                #),
                #widget.Memory(measure_mem='G'),
                #widget.CPU(),
                #widget.Bluetooth(),
                #widget.Volume(
                #    emoji=True,
                #    fmt='Vol: {}'
                #),
                #widget.Battery(format='{percent:2.0%}'),
                #widget.Systray(),
            ],
            26,
            opacity=0.95
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
#floating_layout = layout.Floating(
#    float_rules=[
#        # Run the utility of `xprop` to see the wm class and name of an X client.
#        *layout.Floating.default_float_rules,
#        Match(wm_class="confirmreset"),  # gitk
#        Match(wm_class="makebranch"),  # gitk
#        Match(wm_class="maketag"),  # gitk
#        Match(wm_class="ssh-askpass"),  # ssh-askpass
#        Match(title="branchdialog"),  # gitk
#        Match(title="pinentry"),  # GPG key password entry
#    ]
#)
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),
    ],
    border_focus='#a151d3'
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
