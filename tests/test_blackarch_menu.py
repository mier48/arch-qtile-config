"""BlackArch Tool Center regression checks without BlackArch or X11 installed."""
import importlib.util
import os
import pathlib
import sys
import tempfile
import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".config/qtile/scripts/blackarch-menu.py"
spec = importlib.util.spec_from_file_location("blackarch_tool_center", SCRIPT)
blackarch = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = blackarch
spec.loader.exec_module(blackarch)


class BlackArchMenuTests(unittest.TestCase):
    def test_installed_categories_are_dynamic(self):
        groups = (
            "blackarch-recon nmap\n"
            "blackarch-recon dnsrecon\n"
            "blackarch-webapp sqlmap\n"
            "blackarch sqlmap\n"
            "blackarch misc-tool\n"
            "other-group unrelated\n"
            "blackarch-recon dangerous;command\n"
        )
        with patch.object(blackarch, "run", return_value=CompletedProcess([], 0, groups, "")) as call:
            result = blackarch.installed_groups()
        self.assertEqual(result, {
            "recon": {"nmap", "dnsrecon"},
            "webapp": {"sqlmap"},
            "otros": {"misc-tool"},
        })
        self.assertEqual(call.call_args.args, ("pacman", "-Qg"))

    def test_no_groups(self):
        with patch.object(blackarch, "run", return_value=CompletedProcess([], 0, "", "")):
            self.assertEqual(blackarch.installed_groups(), {})

    def test_errors_if_pacman_fails(self):
        with patch.object(blackarch, "run", return_value=CompletedProcess([], 1, "", "error")):
            with self.assertRaises(RuntimeError):
                blackarch.installed_groups()

    def test_only_real_packaged_executables_in_allowlisted_directories(self):
        # No execution or invoking an arbitrary binary: inspect its location.
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            executable = root / "app"
            executable.write_text("#!/bin/sh\nexit 0\n")
            executable.chmod(0o755)
            with patch.object(blackarch, "package_files", return_value=[
                str(executable), "/etc/passwd", "/usr/share/blackarch/wordlist"
            ]):
                self.assertEqual(blackarch.executables("nmap"), [])
        with patch.object(blackarch, "package_files", return_value=[]):
            self.assertEqual(blackarch.executables("nmap"), [])

    def test_invalid_package_names_not_passed_to_pacman(self):
        with patch.object(blackarch, "run") as call:
            self.assertEqual(blackarch.package_files("a; sudo evil"), [])
            call.assert_not_called()

    def test_rofi_requires_exact_returned_choice(self):
        output = CompletedProcess([], 0, "injected selection\n", "")
        with patch.object(blackarch.subprocess, "run", return_value=output):
            self.assertIsNone(blackarch.choose("TEST", ["safe"]))

    def test_launch_checks_binary_membership(self):
        with patch.object(blackarch, "executables", return_value=["/usr/bin/known"]), \
             patch.object(blackarch.subprocess, "run") as run:
            self.assertEqual(blackarch.launch("nmap", "/usr/bin/unknown"), 2)
            run.assert_not_called()

    def test_launch_is_not_shell_or_sudo(self):
        with patch.object(blackarch, "executables", return_value=["/usr/bin/known"]), \
             patch.object(blackarch.subprocess, "run", return_value=CompletedProcess([], 0, "", "")) as run, \
             patch("builtins.input", return_value=""):
            self.assertEqual(blackarch.launch("nmap", "/usr/bin/known"), 0)
            self.assertEqual(run.call_args.args, (["/usr/bin/known"],))
            self.assertFalse(run.call_args.kwargs.get("shell", False))

    def test_qtile_toolbar_and_operator_menu(self):
        widgets = (ROOT / ".config/qtile/settings/widgets.py").read_text()
        keys = (ROOT / ".config/qtile/settings/keys.py").read_text()
        operator = (ROOT / ".config/qtile/scripts/operator-menu.sh").read_text()
        self.assertIn('action("󰒃", BLACKARCH', widgets)
        self.assertIn('"blackarch-menu.py"', widgets)
        self.assertIn('"blackarch-menu.py"', keys)
        self.assertIn("'08  BlackArch')", operator)


if __name__ == "__main__":
    unittest.main()
