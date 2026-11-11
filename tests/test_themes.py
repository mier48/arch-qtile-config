"""Static consistency checks for the three built-in desktop themes.

Run: python -m unittest discover -s tests -v
No X11, Qtile, Fish, Rofi, or third-party Python packages required.
"""
import json
import re
import tomllib
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".config"
THEMES = ("obsidian", "cyberpunk", "darcula")
MANDATORY = {
    "dark", "grey", "light", "text", "focus", "active", "inactive",
    "urgent", "color1", "color2", "color3", "color4"
}


class ThemeTests(unittest.TestCase):
    def test_all_profiles_present_and_valid(self):
        for name in THEMES:
            with self.subTest(theme=name):
                palette = json.loads(
                    (ROOT / "qtile" / "themes" / f"{name}.json").read_text()
                )
                self.assertTrue(MANDATORY.issubset(palette))
                for color in palette.values():
                    self.assertRegex(color, r"^#[0-9A-Fa-f]{6}$")

                fastfetch = json.loads(
                    (ROOT / "fastfetch" / "themes" / f"{name}.jsonc").read_text()
                )
                self.assertEqual(fastfetch["logo"]["color"]["1"], palette["focus"])
                self.assertEqual(fastfetch["display"]["color"]["keys"], palette["focus"])

                alacritty = tomllib.loads(
                    (ROOT / "alacritty" / "themes" / f"{name}.toml").read_text()
                )
                self.assertEqual(alacritty["colors"]["primary"]["background"], palette["dark"])
                self.assertEqual(alacritty["colors"]["cursor"]["cursor"], palette["focus"])

                rofi = (ROOT / "rofi" / "themes" / f"{name}.rasi").read_text()
                self.assertIn(f"accent:         {palette['focus']};", rofi)

                fish = (ROOT / "fish" / "themes" / f"{name}.fish").read_text()
                self.assertIn(f"set -g __theme_accent {palette['focus'][1:]}", fish)

                dunst = (ROOT / "dunst" / "themes" / f"{name}.conf").read_text()
                self.assertIn(f'background = "{palette["color1"]}"', dunst)
                self.assertIn(f'highlight = "{palette["focus"]}"', dunst)

                picom = (ROOT / "picom" / "themes" / f"{name}.conf").read_text()
                self.assertIn('backend = "glx";', picom)

                svg = ROOT / "qtile" / "wallpapers" / f"{name}.svg"
                root = ET.parse(svg).getroot()
                self.assertEqual(root.get("width"), "3440")
                self.assertEqual(root.get("height"), "1440")

    def test_default_active_files_exist(self):
        paths = [
            "alacritty/themes/active.toml",
            "rofi/themes/active.rasi",
            "fish/conf.d/theme.fish",
            "fastfetch/config.jsonc",
            "dunst/dunstrc",
            "picom/picom.conf",
            "qtile/config.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

    def test_selected_theme_is_known(self):
        selected = json.loads((ROOT / "qtile" / "config.json").read_text())["theme"]
        self.assertIn(selected, THEMES)

    def test_launcher_points_to_active_theme(self):
        self.assertIn(
            '@theme "themes/active.rasi"',
            (ROOT / "rofi" / "config.rasi").read_text()
        )
        self.assertIn(
            'import = ["themes/active.toml"]',
            (ROOT / "alacritty" / "alacritty.toml").read_text()
        )


if __name__ == "__main__":
    unittest.main()
