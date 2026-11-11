"""Eight numbered groups; labels are visual, names stay 1–8."""

from libqtile.config import Group, Key
from libqtile.lazy import lazy
from .keys import keys, mod

groups = [Group(str(i), label=f"{i:02d}") for i in range(1, 9)]
for group in groups:
    keys.extend([
        Key([mod], group.name, lazy.group[group.name].toscreen(),
            desc=f"Switch to group {group.name}"),
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name),
            desc=f"Move window to group {group.name}"),
    ])
