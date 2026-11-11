"""Regression tests for the NetworkManager VPN picker (no VPN connection needed)."""
import importlib.util
import pathlib
import sys
import unittest
from subprocess import CompletedProcess
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / ".config/qtile/scripts/vpn-menu.py"
spec = importlib.util.spec_from_file_location("qtile_vpn_menu", SCRIPT)
vpn = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = vpn
spec.loader.exec_module(vpn)

A = "12345678-aaaa-4444-bbbb-123456789abc"
B = "12345678-bbbb-4444-cccc-222222222222"


class VPNMenuTests(unittest.TestCase):
    def test_parses_uuid_and_type_only(self):
        with patch.object(vpn, "command", return_value=CompletedProcess([], 0,
                f"{A}:vpn\n{B}:wireguard\n00000000-aaaa-4444-bbbb-123456789abc:802-3-ethernet\ninvalid:vpn\n", "")):
            self.assertEqual(vpn.ids(), {A: "vpn", B: "wireguard"})

    def test_profile_names_not_used_as_shell_commands(self):
        calls = []
        def fake(*args, **kwargs):
            calls.append(args)
            if "--active" in args:
                return CompletedProcess([], 0, f"{B}:wireguard\n", "")
            if "-g" in args:
                return CompletedProcess([], 0, "My VPN;$(touch /tmp/not-executed)\n", "")
            return CompletedProcess([], 0, f"{A}:vpn\n{B}:wireguard\n", "")

        with patch.object(vpn, "command", side_effect=fake):
            profiles = vpn.profiles()
        self.assertEqual(len(profiles), 2)
        self.assertTrue(profiles[0].active)
        self.assertIn("$(touch", profiles[0].name)
        self.assertTrue(all("uuid" in args for args in calls if "-g" in args))

    def test_selected_profile_by_full_uuid_and_no_shell(self):
        available = [
            vpn.Profile(A, "VPN; rm -rf ~", "vpn", False),
            vpn.Profile(B, "VPN; rm -rf ~", "wireguard", True),
        ]
        with patch.object(vpn, "profiles", return_value=available), \
             patch.object(vpn, "rofi", side_effect=lambda opts: opts[0]), \
             patch.object(vpn, "command", return_value=CompletedProcess([], 0, "", "")) as call, \
             patch.object(vpn, "notify"), \
             patch.object(vpn.shutil, "which", return_value="/usr/bin/ok"):
            self.assertEqual(vpn.menu(), 0)
        args = call.call_args.args
        self.assertEqual(args[:4], ("--wait", "30", "connection", "up"))
        self.assertEqual(args[4:], ("uuid", A))
        self.assertNotIn("rm -rf", " ".join(args))

    def test_status_active_and_unavailable(self):
        with patch.object(vpn, "ids", return_value={A: "vpn"}):
            self.assertEqual(vpn.status(), "VPN  ON (1)")
        with patch.object(vpn, "ids", return_value={}):
            self.assertEqual(vpn.status(), "VPN  OFF")
        with patch.object(vpn, "ids", side_effect=RuntimeError()):
            self.assertEqual(vpn.status(), "VPN  ?")

    def test_qtile_integration(self):
        root = SCRIPT.parents[1]
        widgets = (root / "settings/widgets.py").read_text()
        keys = (root / "settings/keys.py").read_text()
        operator = (root / "scripts/operator-menu.sh").read_text()
        self.assertIn("widget.GenPollCommand(", widgets)
        self.assertIn('"--status"', widgets)
        self.assertIn('vpn_widget()', widgets)
        self.assertIn('vpn-menu.py', keys)
        self.assertIn("'07  VPN'", operator)


if __name__ == "__main__":
    unittest.main()
