"""Static checks for Operator HUD integration without a running X11 session."""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".config" / "qtile"
SETTINGS = ROOT / "settings"


class OperatorHUDTests(unittest.TestCase):
    def test_python_syntax(self):
        for path in [ROOT / "config.py", *SETTINGS.glob("*.py")]:
            with self.subTest(file=str(path)):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_semantic_groups_and_scratchpad(self):
        groups = (SETTINGS / "groups.py").read_text(encoding="utf-8")
        self.assertIn('ScratchPad(', groups)
        self.assertIn('DropDown(', groups)
        self.assertIn('name, label=label', groups)
        self.assertIn('"terminal"', groups)
        self.assertIn('"monitor"', groups)
        self.assertIn('single=True', groups)
        self.assertIn('range(1, 9)', (SETTINGS / "widgets.py").read_text())

    def test_per_screen_widget_instances(self):
        screens = (SETTINGS / "screens.py").read_text(encoding="utf-8")
        widgets = (SETTINGS / "widgets.py").read_text(encoding="utf-8")
        self.assertIn("build_widgets(primary=primary, compact=compact)", screens)
        self.assertIn("def build_widgets(primary=False, compact=False):", widgets)
        self.assertIn("widget.TaskList(", widgets)
        self.assertIn("widget.GroupBox(", widgets)
        self.assertIn("widget.CurrentLayout(", widgets)

    def test_keyboard_first_controls(self):
        keys = (SETTINGS / "keys.py").read_text(encoding="utf-8")
        self.assertIn('lazy.window.toggle_fullscreen()', keys)
        self.assertIn('lazy.window.toggle_floating()', keys)
        self.assertIn('lazy.screen.toggle_group()', keys)
        self.assertIn('operator-menu.sh', keys)
        self.assertNotIn('/bin/sh ~/.config', keys)

    def test_operator_menu_is_allowlisted(self):
        script = (ROOT / "scripts" / "operator-menu.sh").read_text(encoding="utf-8")
        self.assertIn('case "$choice" in', script)
        self.assertIn('-no-custom', script)
        self.assertNotIn('eval ', script)
        self.assertIn("btop", script)


if __name__ == "__main__":
    unittest.main()
