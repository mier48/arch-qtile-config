"""Load the Qtile Obsidian palette without modifying files at runtime."""

import json
from pathlib import Path
from .path import qtile_path


def load_theme():
    root = Path(qtile_path)
    selected = root / "config.json"
    theme = "obsidian"

    if selected.is_file():
        with selected.open(encoding="utf-8") as stream:
            theme = json.load(stream).get("theme", theme)

    if not isinstance(theme, str) or not theme.isidentifier():
        raise ValueError("Invalid Qtile theme name")

    theme_file = root / "themes" / f"{theme}.json"
    with theme_file.open(encoding="utf-8") as stream:
        colors = json.load(stream)

    required = {"dark", "grey", "light", "text", "focus", "active",
                "inactive", "urgent", "color1", "color2", "color3", "color4"}
    if not required.issubset(colors) or not all(
        isinstance(value, str) and value.startswith("#") and len(value) == 7
        for value in colors.values()
    ):
        raise ValueError(f"Invalid Qtile palette: {theme_file}")

    return colors


colors = load_theme()
