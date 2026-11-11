"""Ultrawide-friendly layouts and the Obsidian focus border."""

from libqtile import layout
from libqtile.config import Match

from .theme import colors

layout_conf = {
    "border_focus": colors["focus"],
    "border_normal": colors["grey"],
    "border_width": 2,
    "margin": 10,
}

layouts = [
    layout.MonadTall(ratio=0.56, **layout_conf),
    layout.Bsp(**layout_conf),
    layout.MonadWide(**layout_conf),
    layout.Max(),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus=colors["focus"],
    border_normal=colors["grey"],
    border_width=2,
)
