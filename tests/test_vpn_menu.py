"""Regression tests for native WireGuard connections in NetworkManager."""
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
            self.assertEqual(vpn.ids(), {B: "wireguard"})

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
        self.assertEqual(len(profiles), 1)
        self.assertTrue(profiles[0].active)
        self.assertIn("$(touch", profiles[0].name)
        self.assertEqual(profiles[0].type, "wireguard")
        self.assertTrue(all("uuid" in args for args in calls if "-g" in args))

    def test_selected_profile_by_full_uuid_and_no_shell(self):
        available = [
            vpn.Profile(A, "WG; rm -rf ~", "wireguard", False),
            vpn.Profile(B, "WG; rm -rf ~", "wireguard", True),
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
            self.assertEqual(vpn.status(), "WG/NM  ON (1)")
        with patch.object(vpn, "ids", return_value={}):
            self.assertEqual(vpn.status(), "WG/NM  OFF")
        with patch.object(vpn, "ids", side_effect=RuntimeError()):
            self.assertEqual(vpn.status(), "WG/NM  ?")

    def test_toolbar_contains_only_vpn_icon(self):
        widgets = (SCRIPT.parents[1] / "settings/widgets.py").read_text()
        themes = widgets.index('action("󰔎", THEMES')
        vpn_icon = widgets.index('vpn_indicator(),')
        power = widgets.index('action("⏻", POWER')
        self.assertLess(themes, power)
        self.assertLess(vpn_icon, power)
        self.assertIn('mouse_callbacks={"Button1": lazy.spawn(command)}', widgets)
        self.assertIn('return widget.GenPollText(', widgets)
        self.assertIn('󰖂', widgets)
        self.assertNotIn('GenPollCommand(', widgets)

    def test_qtile_integration(self):
        root = SCRIPT.parents[1]
        widgets = (root / "settings/widgets.py").read_text()
        keys = (root / "settings/keys.py").read_text()
        operator = (root / "scripts/operator-menu.sh").read_text()
        self.assertIn('vpn_indicator()', widgets)
        self.assertNotIn("GenPollCommand(", widgets)
        self.assertIn('vpn-menu.py', keys)
        self.assertIn("'07  WireGuard'", operator)


if __name__ == "__main__":
    unittest.main()
