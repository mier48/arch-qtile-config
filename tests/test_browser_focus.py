"""Regression checks for X11 focus and browser input usability."""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".config" / "qtile"


def assignments(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        target.id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
        and target.id in {
            "follow_mouse_focus", "bring_front_click",
            "focus_on_window_activation", "floats_kept_above",
        }
    }


class BrowserFocusTests(unittest.TestCase):
    def test_browser_activation_is_not_relegated_to_urgent(self):
        conf = assignments(ROOT / "config.py")
        self.assertEqual(conf["focus_on_window_activation"], "smart")
        self.assertTrue(conf["follow_mouse_focus"])
        self.assertEqual(conf["bring_front_click"], "floating_only")
        self.assertTrue(conf["floats_kept_above"])

    def test_no_firefox_float_or_forced_group(self):
        layouts = (ROOT / "settings" / "layouts.py").read_text().lower()
        groups = (ROOT / "settings" / "groups.py").read_text().lower()
        self.assertNotIn('wm_class="firefox"', layouts)
        self.assertNotIn('"firefox"', groups)


if __name__ == "__main__":
    unittest.main()
