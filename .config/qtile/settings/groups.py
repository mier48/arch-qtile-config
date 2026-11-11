"""Semantic workspaces and two native, on-demand scratchpads.

Groups retain numeric names so the existing Super+1..8 bindings remain stable.
The scratchpad group is deliberately hidden from GroupBox.
"""

from libqtile.config import DropDown, Group, Key, ScratchPad
from libqtile.lazy import lazy

from .keys import keys, mod


WORKSPACES = (
    ("1", "01 DEV"),
    ("2", "02 WEB"),
    ("3", "03 DATA"),
    ("4", "04 OPS"),
    ("5", "05 LAB"),
    ("6", "06 COMMS"),
    ("7", "07 DOCS"),
    ("8", "08 MISC"),
)

groups = [Group(name, label=label) for name, label in WORKSPACES]

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "terminal",
                "alacritty",
                x=0.18, y=0.12, width=0.64, height=0.66,
                opacity=1.0, on_focus_lost_hide=True, warp_pointer=False,
            ),
            DropDown(
                "monitor",
                "alacritty -e btop",
                x=0.13, y=0.10, width=0.74, height=0.76,
                opacity=1.0, on_focus_lost_hide=True, warp_pointer=False,
            ),
        ],
        label="",
        single=True,
    )
)

for name, _label in WORKSPACES:
    keys.extend(
        [
            Key([mod], name, lazy.group[name].toscreen(), desc=f"Go to workspace {name}"),
            Key(
                [mod, "shift"], name, lazy.window.togroup(name),
                desc=f"Move window to workspace {name}",
            ),
        ]
    )

keys.extend(
    [
        Key(
            [mod], "grave",
            lazy.group["scratchpad"].dropdown_toggle("terminal"),
            desc="Toggle scratchpad terminal",
        ),
        Key(
            [mod, "shift"], "grave",
            lazy.group["scratchpad"].dropdown_toggle("monitor"),
            desc="Toggle btop system dashboard",
        ),
    ]
)
