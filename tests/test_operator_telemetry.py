"""Regression suite for local network/telemetry and Operator HUD controls."""
from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT / ".config" / "qtile" / "settings"
sys.path.insert(0, str(SETTINGS))
import system_state as state


class LocalStateTests(unittest.TestCase):
    def setUp(self):
        state._CACHE.clear()

    def test_wireguard_connected_only_for_native_nm_profile(self):
        def command(*args, **kwargs):
            if "connection" in args:
                return "1b6c4f79-4125-4f8d-b004-b9da678af2c7:wireguard\n"
            return "enp4s0:ethernet:connected\nwlan0:wifi:disconnected\n"
        with patch.object(state, "_command", side_effect=command):
            status = state._read_network()
        self.assertTrue(status.vpn)
        self.assertTrue(status.connected)
        self.assertEqual(status.interface, "enp4s0")
        self.assertEqual(state.vpn_label(status), "WG/NM ON")

    def test_off_and_unknown_are_distinct(self):
        with patch.object(state, "_command", side_effect=[
            "1b6c4f79-4125-4f8d-b004-b9da678af2c7:ethernet\n",
            "enp4s0:ethernet:connected\n"
        ]):
            off = state._read_network()
        self.assertIs(off.vpn, False)
        self.assertEqual(state.vpn_label(off), "WG/NM OFF")
        with patch.object(state, "_command", return_value=None):
            unknown = state._read_network()
        self.assertIsNone(unknown.vpn)
        self.assertEqual(state.vpn_label(unknown), "WG/NM ?")

    def test_vpn_is_not_inferred_from_ip_or_route(self):
        self.assertNotIn("https://", (SETTINGS / "system_state.py").read_text())
        self.assertNotIn("requests.get", (SETTINGS / "system_state.py").read_text())
        with patch.object(state, "_command", side_effect=["", "enp4s0:ethernet:connected\n"]):
            result = state._read_network()
        self.assertIs(result.vpn, False)

    def test_telemetry_gpu_parsing_and_unavailable_sensors(self):
        with patch.object(state, "_command", return_value="42, 59, 2048\n"):
            with patch.object(state, "_cpu_temperature", return_value=None):
                data = state._read_telemetry()
        self.assertEqual(data.gpu_percent, 42)
        self.assertEqual(data.gpu_temp_c, 59)
        self.assertEqual(data.gpu_memory_mib, 2048)
        self.assertIsNone(data.cpu_temp_c)
        with patch.object(state, "_command", return_value=None):
            data = state._read_telemetry()
        self.assertIsNone(data.gpu_percent)
        self.assertIn("GPU —", state.telemetry_label(data))

    def test_cache_does_not_block_peek_on_slow_producer(self):
        import threading
        from time import sleep
        gate = threading.Event()
        ready = threading.Event()
        def producer():
            ready.set()
            gate.wait(timeout=1)
            return state.NetworkState(vpn=True)
        thread = threading.Thread(target=lambda: state._cached("network", producer), daemon=True)
        thread.start()
        self.assertTrue(ready.wait(timeout=1))
        # peek obtains the mutex while a producer is still executing.
        self.assertIsNone(state._peek("network"))
        gate.set()
        thread.join(timeout=1)
        self.assertTrue(state.peek_network().vpn)


class WidgetIntegrationTests(unittest.TestCase):
    def test_same_icon_and_click_actions(self):
        widgets = (SETTINGS / "widgets.py").read_text()
        self.assertIn("󰖂", widgets)
        self.assertIn('color = C["focus"] if vpn is True else C["inactive"]', widgets)
        self.assertIn('"Button1": lazy.spawn(VPN)', widgets)
        self.assertIn('"Button3": lazy.function(show_network_popup)', widgets)

    def test_context_and_popups_are_optional(self):
        widgets = (SETTINGS / "widgets.py").read_text()
        popups = (SETTINGS / "popups.py").read_text()
        self.assertIn("widget.WidgetBox(", widgets)
        self.assertIn("start_opened=False", widgets)
        self.assertIn("system_button()", widgets)
        self.assertIn("PopupRelativeLayout", popups)
        self.assertIn("PopupWidget(", popups)
        self.assertIn("except ImportError:", popups)
        self.assertIn("state.peek_telemetry()", popups)


if __name__ == "__main__":
    unittest.main()
