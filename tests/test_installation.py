"""Behavioural tests for the user-only dotfile installer.

Tests use isolated temporary repositories and HOME directories and never
touch the running desktop. GitHub Actions runs them as an unprivileged user.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-dotfiles.sh"
COMPONENTS = ("qtile", "fish", "alacritty", "fastfetch", "rofi", "dunst", "picom")


@unittest.skipIf(os.geteuid() == 0, "Installer deliberately rejects root")
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.repo = root / "repo"
        self.home = root / "home"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "tests").mkdir()
        (self.home / ".config" / "qtile").mkdir(parents=True)
        shutil.copy2(INSTALLER, self.repo / "scripts" / "install-dotfiles.sh")
        (self.repo / "tests" / "test_smoke.py").write_text(
            "import unittest\n"
            "class Smoke(unittest.TestCase):\n"
            "    def test_pass(self): self.assertTrue(True)\n"
        )
        for name in COMPONENTS:
            path = self.repo / ".config" / name
            path.mkdir(parents=True)
            (path / "marker").write_text("new")
        (self.repo / ".config" / "qtile" / "scripts").mkdir()

    def run_installer(self, *args):
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        result = subprocess.run(
            ["sh", str(self.repo / "scripts" / "install-dotfiles.sh"), *args],
            env=env, capture_output=True, text=True, timeout=30,
        )
        return result

    def test_preserves_existing_theme_and_backups(self):
        (self.home / ".config" / "qtile" / "config.json").write_text(
            '{"theme":"cyberpunk"}'
        )
        (self.repo / ".config" / "qtile" / "scripts" / "theme-switch.py").write_text(
            "import json,sys,pathlib\n"
            "p=pathlib.Path.home()/'.config/qtile/config.json'\n"
            "p.write_text(json.dumps({'theme':sys.argv[1]}))\n"
        )
        result = self.run_installer("--apply")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(
            json.loads((self.home / ".config" / "qtile" / "config.json").read_text())["theme"],
            "cyberpunk",
        )
        self.assertEqual(len(list((self.home / ".config").glob("qtile.backup.*"))), 1)
        for component in COMPONENTS:
            self.assertEqual((self.home / ".config" / component / "marker").read_text(), "new")

    def test_rolls_back_when_theme_switch_fails(self):
        (self.home / ".config" / "qtile" / "marker").write_text("original")
        (self.repo / ".config" / "qtile" / "scripts" / "theme-switch.py").write_text(
            "raise SystemExit(23)\n"
        )
        result = self.run_installer("--apply", "--theme", "darcula")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.home / ".config" / "qtile" / "marker").read_text(), "original")
        self.assertFalse(list((self.home / ".config").glob(".operator-stage.*")))

    def test_rejects_invalid_theme(self):
        result = self.run_installer("--apply", "--theme", "unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.home / ".config" / "fish").exists())


if __name__ == "__main__":
    unittest.main()
