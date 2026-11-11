"""Security-oriented static tests for the X11 lock and Qt6 SDDM greeter."""
import configparser
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QTILE = ROOT / ".config" / "qtile"
SDDM = ROOT / "sddm" / "operator-hud"


class SecureSessionTests(unittest.TestCase):
    def test_lockscreen_assets(self):
        for name in ("obsidian", "cyberpunk", "darcula"):
            with self.subTest(name=name):
                svg = QTILE / "lockscreen" / (name + ".svg")
                root = ET.parse(svg).getroot()
                self.assertEqual(root.attrib["width"], "3440")
                self.assertEqual(root.attrib["height"], "1440")

    def test_lock_is_foreground_and_has_no_screenshots(self):
        script = (QTILE / "scripts" / "lock.sh").read_text()
        self.assertIn("exec i3lock -n", script)
        self.assertIn('exec i3lock -n -c "$bg"', script)
        self.assertNotIn("scrot", script)
        self.assertNotIn("import -window", script)
        self.assertNotIn("eval ", script)

    def test_logind_sleep_lock_chain(self):
        autostart = (QTILE / "autostart.sh").read_text()
        self.assertIn("xss-lock --transfer-sleep-lock", autostart)
        self.assertIn("scripts/lock.sh", autostart)
        self.assertIn("xset s 600 600", autostart)
        power = (QTILE / "scripts" / "power-menu.sh").read_text()
        self.assertIn("lock-preflight.sh", power)
        self.assertIn("systemctl suspend", power)

    def test_sddm_greeter_security_contract(self):
        qml = (SDDM / "Main.qml").read_text()
        self.assertIn("sddm.login(", qml)
        self.assertIn("TextInput.Password", qml)
        self.assertIn('password.text = ""', qml)
        self.assertIn("sessionModel", qml)
        self.assertNotIn("userModel", qml)
        self.assertNotIn("autoLogin", qml)

    def test_sddm_metadata_and_palettes(self):
        p = configparser.ConfigParser()
        p.read(SDDM / "metadata.desktop")
        self.assertEqual(p["SddmGreeterTheme"]["QtVersion"], "6")
        self.assertEqual(p["SddmGreeterTheme"]["MainScript"], "Main.qml")
        for name in ("obsidian", "cyberpunk", "darcula"):
            path = SDDM / "themes" / (name + ".conf")
            self.assertTrue(path.is_file())
            palette = configparser.ConfigParser()
            palette.read(path)
            self.assertIn("General", palette)
            values = dict(palette["General"])
            self.assertEqual(set(values), {
                "background", "panel", "foreground", "accent",
                "muted", "border", "error"
            })
            for value in values.values():
                self.assertRegex(value, r"^#[0-9A-Fa-f]{6}$")

    def test_sddm_cyberpunk_accent_and_fish_autostart(self):
        palette = configparser.ConfigParser()
        palette.read(SDDM / "themes" / "cyberpunk.conf")
        self.assertEqual(palette["General"]["accent"], "#FF4FA3")
        fish = (ROOT / ".config" / "fish" / "config.fish").read_text()
        self.assertIn("command fastfetch", fish)
        self.assertIn("FASTFETCH_AUTOSTART", fish)
        self.assertIn("status is-interactive", fish)
        self.assertIn("SSH_CONNECTION", fish)

    def test_installer_does_not_change_pam_or_enable_services(self):
        script = (ROOT / "sddm" / "install-theme.sh").read_text()
        self.assertNotIn("/etc/pam.d/", script)
        self.assertNotIn("systemctl enable", script)
        self.assertNotIn("systemctl restart", script)
        self.assertIn("/etc/sddm.conf.d/90-operator-hud.conf", script)
        self.assertIn("operator-$theme", script)


if __name__ == "__main__":
    unittest.main()
