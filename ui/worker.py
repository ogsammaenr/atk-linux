"""
Background QThread worker for ATK Neptune N9 Headset.
Safely handles all serial communications without blocking the PyQt6 GUI.
"""

import time
import queue
from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from atk_n9 import ATKNeptuneN9, find_serial_port, PRESET_PROFILES


class Command:
    def __init__(self, action: str, **kwargs):
        self.action = action
        self.kwargs = kwargs


class N9Worker(QThread):
    # Signals to GUI
    sig_connection_changed = pyqtSignal(bool, str) # is_connected, port_or_msg
    sig_status_updated = pyqtSignal(dict)          # battery, charging, status
    sig_mic_updated = pyqtSignal(dict)             # mute, volume, sidetone_en, sidetone_vol
    sig_eq_updated = pyqtSignal(dict)              # eq_id, bands
    sig_surround_updated = pyqtSignal(dict)        # enabled
    sig_effect_updated = pyqtSignal(dict)          # enabled, effect_id, effect_name
    sig_notification = pyqtSignal(str, str)        # title, message (for system tray or toast)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._running = True
        self._cmd_queue = queue.Queue()
        self.device: Optional[ATKNeptuneN9] = None
        self.is_connected = False
        self.last_battery = -1

    def run(self):
        """Main worker loop."""
        last_poll_time = 0
        poll_interval = 2.0  # Poll every 2 seconds

        while self._running:
            # 1. Ensure Device Connection
            if not self.device or not self.is_connected:
                port = find_serial_port()
                if port:
                    try:
                        self.device = ATKNeptuneN9(port)
                        self.device.connect()
                        self.is_connected = True
                        self.sig_connection_changed.emit(True, port)
                        # Immediately do a full refresh
                        self._refresh_all()
                    except Exception as e:
                        self.device = None
                        self.is_connected = False
                        self.sig_connection_changed.emit(False, str(e))
                else:
                    self.is_connected = False
                    self.sig_connection_changed.emit(False, "Device not found")
                
                if not self.is_connected:
                    time.sleep(1.0)
                    continue

            # 2. Process Pending User Commands
            while not self._cmd_queue.empty():
                cmd = self._cmd_queue.get_nowait()
                self._execute_command(cmd)

            # 3. Handle Spontaneous / Push Telemetry Events
            try:
                # Read any unsolicited packets (e.g. 0xA1 mic mute, 0xA3 sidetone)
                pkts = self.device._read_packets(0.05)
                for p in pkts:
                    self._handle_async_packet(p)
            except Exception as e:
                self._handle_io_error(e)
                continue

            # 4. Periodic Poll
            now = time.time()
            if now - last_poll_time >= poll_interval:
                last_poll_time = now
                self._poll_status()

            time.sleep(0.05)

        # Cleanup
        if self.device:
            try:
                self.device.disconnect()
            except Exception:
                pass

    def stop(self):
        """Stop worker thread safely."""
        self._running = False
        self.wait(1500)

    def queue_command(self, action: str, **kwargs):
        """Thread-safe method called from GUI."""
        self._cmd_queue.put(Command(action, **kwargs))

    def _execute_command(self, cmd: Command):
        if not self.device:
            return
        try:
            if cmd.action == "set_sidetone":
                cur = self.device.get_microphone_info()
                mute = cur.get("mute", False)
                mic_vol = cur.get("volume", 100)
                en = cmd.kwargs.get("enabled", True)
                vol = cmd.kwargs.get("volume", 100)
                self.device.set_microphone_info(mute, mic_vol, en, vol)
                self.sig_mic_updated.emit({
                    "mute": mute,
                    "volume": mic_vol,
                    "sidetone_enabled": en,
                    "sidetone_volume": vol
                })

            elif cmd.action == "set_mic_mute":
                cur = self.device.get_microphone_info()
                mute = cmd.kwargs.get("mute", False)
                mic_vol = cur.get("volume", 100)
                s_en = cur.get("sidetone_enabled", True)
                s_vol = cur.get("sidetone_volume", 100)
                self.device.set_microphone_info(mute, mic_vol, s_en, s_vol)
                self.sig_mic_updated.emit({
                    "mute": mute,
                    "volume": mic_vol,
                    "sidetone_enabled": s_en,
                    "sidetone_volume": s_vol
                })

            elif cmd.action == "set_mic_volume":
                cur = self.device.get_microphone_info()
                mute = cur.get("mute", False)
                mic_vol = cmd.kwargs.get("volume", 100)
                s_en = cur.get("sidetone_enabled", True)
                s_vol = cur.get("sidetone_volume", 100)
                self.device.set_microphone_info(mute, mic_vol, s_en, s_vol)

            elif cmd.action == "set_eq_bands":
                eq_id = cmd.kwargs.get("eq_id", 5)
                bands = cmd.kwargs.get("bands", [0] * 10)
                self.device.set_eq_bands(eq_id, bands)
                self.sig_eq_updated.emit({"eq_id": eq_id, "bands": bands})

            elif cmd.action == "apply_preset":
                name = cmd.kwargs.get("preset_name", "flat")
                if name in PRESET_PROFILES:
                    bands = PRESET_PROFILES[name]
                    self.device.set_eq_bands(5, bands)
                    self.sig_eq_updated.emit({"eq_id": 5, "bands": bands, "preset_name": name})

            elif cmd.action == "set_surround":
                en = cmd.kwargs.get("enabled", False)
                self.device.set_surround(en)
                self.sig_surround_updated.emit({"enabled": en})

            elif cmd.action == "set_effect":
                eff_id = cmd.kwargs.get("effect_id", 0)
                # If eff_id == -1, reset/disable
                if eff_id == -1:
                    self.device.transfer(0x04, 0x21, [0]) # Reset
                    self.sig_effect_updated.emit({"enabled": False, "effect_id": 0, "effect_name": "Off"})
                else:
                    self.device.transfer(0x04, 0x20, [eff_id]) # Set
                    effects = {0: "Male", 1: "Female", 2: "Monster", 3: "Cartoon"}
                    self.sig_effect_updated.emit({
                        "enabled": True,
                        "effect_id": eff_id,
                        "effect_name": effects.get(eff_id, "Custom")
                    })

            elif cmd.action == "refresh_all":
                self._refresh_all()

        except Exception as e:
            self._handle_io_error(e)

    def _poll_status(self):
        if not self.device:
            return
        try:
            status = self.device.get_status()
            batt = self.device.get_battery()
            combined = {**status, **batt}
            self.sig_status_updated.emit(combined)

            # Battery level check
            lvl = batt.get("level")
            if lvl is not None:
                self.last_battery = lvl

        except Exception as e:
            self._handle_io_error(e)

    def _refresh_all(self):
        if not self.device:
            return
        try:
            self._poll_status()
            mic = self.device.get_microphone_info()
            if "error" not in mic:
                self.sig_mic_updated.emit(mic)

            eq = self.device.get_eq_profile()
            if "error" not in eq:
                self.sig_eq_updated.emit({
                    "eq_id": eq.get("eq_id", 5),
                    "bands": eq.get("bands_raw", [0] * 10)
                })

            surround = self.device.get_surround()
            if "error" not in surround:
                self.sig_surround_updated.emit(surround)

            effect = self.device.get_effect()
            if "error" not in effect:
                self.sig_effect_updated.emit(effect)

        except Exception as e:
            self._handle_io_error(e)

    def _handle_async_packet(self, pkt: bytes):
        if len(pkt) < 3:
            return
        cmd = pkt[1]
        subcmd = pkt[2]

        # 0xA1: Mic Mute physical button/flip
        if subcmd == 0xA1 and len(pkt) >= 4:
            mute_state = (pkt[3] == 1)
            self.sig_mic_updated.emit({"mute": mute_state})

        # 0xA3: Sidetone Monitor Toggle button
        elif subcmd == 0xA3 and len(pkt) >= 4:
            monitor_en = (pkt[3] == 1)
            self.sig_mic_updated.emit({"sidetone_enabled": monitor_en})

        # 0x83: Battery event
        elif subcmd == 0x83 and len(pkt) >= 5:
            r = pkt[4]
            charging = (r >> 7) == 1
            power = r & 127
            self.sig_status_updated.emit({"level": power, "charging": charging, "connected": True})

    def _handle_io_error(self, err: Exception):
        # On disconnection or serial read failure
        self.is_connected = False
        if self.device:
            try:
                self.device.disconnect()
            except Exception:
                pass
            self.device = None
        self.sig_connection_changed.emit(False, str(err))
