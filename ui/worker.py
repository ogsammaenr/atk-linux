"""
Background QThread worker for ATK Neptune N9 Headset.
Safely handles all serial communications and RF connection state without blocking the PyQt6 GUI.
"""

import time
import queue
from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from atk_n9 import ATKNeptuneN9, find_serial_port, PRESET_PROFILES
from ui.voice_changer import VoiceChangerManager


class Command:
    def __init__(self, action: str, **kwargs):
        self.action = action
        self.kwargs = kwargs


class N9Worker(QThread):
    # Signals to GUI
    sig_connection_changed = pyqtSignal(bool, str) # is_port_open, port_or_msg
    sig_status_updated = pyqtSignal(dict)          # connected (rf), level, charging
    sig_mic_updated = pyqtSignal(dict)             # mute, volume, sidetone_en, sidetone_vol
    sig_eq_updated = pyqtSignal(dict)              # eq_id, bands
    sig_surround_updated = pyqtSignal(dict)        # enabled
    sig_effect_updated = pyqtSignal(dict)          # enabled, effect_id, effect_name
    sig_notification = pyqtSignal(str, str)        # title, message

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._running = True
        self._cmd_queue = queue.Queue()
        self.device: Optional[ATKNeptuneN9] = None
        self.is_port_open = False
        self.is_rf_connected = False
        self._last_rf_connected: Optional[bool] = None
        self.last_battery = -1
        self.voice_changer = VoiceChangerManager()

    @property
    def is_connected(self) -> bool:
        """Backward compatibility for RF connection status."""
        return self.is_rf_connected

    def _interruptible_sleep(self, duration: float, step: float = 0.05):
        end = time.time() + duration
        while self._running and time.time() < end:
            time.sleep(min(step, max(0.0, end - time.time())))

    def run(self):
        """Main worker loop."""
        last_poll_time = 0.0
        poll_interval = 1.5

        while self._running:
            # 1. Ensure Port Connection
            if not self.device or not self.device.is_open or not self.is_port_open:
                port = find_serial_port()
                if port:
                    try:
                        self.device = ATKNeptuneN9(port)
                        self.device.connect()
                        self.is_port_open = True
                        self._last_rf_connected = None
                        self.sig_connection_changed.emit(True, port)
                        # Check status immediately to determine RF link
                        self._poll_status()
                    except Exception as e:
                        self._handle_io_error(e)
                        self._interruptible_sleep(0.8)
                        continue
                else:
                    if self.is_port_open:
                        self._handle_io_error(Exception("Port not found"))
                    self._interruptible_sleep(0.8)
                    continue

            # 2. Process Pending User Commands
            while not self._cmd_queue.empty():
                cmd = self._cmd_queue.get_nowait()
                self._execute_command(cmd)

            # 3. Handle Spontaneous / Push Telemetry Events
            try:
                pkts = self.device._read_packets(0.04)
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

        # Cleanup on thread exit
        try:
            self.voice_changer.cleanup()
        except Exception:
            pass
        if self.device:
            try:
                self.device.disconnect()
            except Exception:
                pass
            self.device = None

    def stop(self):
        """Stop worker thread safely."""
        self._running = False
        try:
            self.voice_changer.cleanup()
        except Exception:
            pass
        if not self.wait(1000):
            self.terminate()
            self.wait(500)

    def queue_command(self, action: str, **kwargs):
        """Thread-safe method called from GUI."""
        self._cmd_queue.put(Command(action, **kwargs))

    def _execute_command(self, cmd: Command):
        if not self.device or not self.device.is_open:
            return

        # If RF is not connected, only allow refresh_all
        if not self.is_rf_connected and cmd.action != "refresh_all":
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
                eff_id = cmd.kwargs.get("effect_id", -1)
                self.device.set_effect(eff_id)
                self.voice_changer.set_effect(eff_id)
                if eff_id == -1:
                    self.sig_effect_updated.emit({"enabled": False, "effect_id": -1, "effect_name": "Off"})
                else:
                    effects = {0: "Male", 1: "Female", 2: "Monster", 3: "Cartoon"}
                    self.sig_effect_updated.emit({
                        "enabled": True,
                        "effect_id": eff_id,
                        "effect_name": effects.get(eff_id, "Custom")
                    })

            elif cmd.action == "refresh_all":
                self._last_rf_connected = None
                self._poll_status()

        except Exception as e:
            self._handle_io_error(e)

    def _poll_status(self):
        if not self.device or not self.device.is_open:
            return
        try:
            status = self.device.get_status()
            rf_connected = status.get("connected", False)

            if rf_connected != self._last_rf_connected:
                self._last_rf_connected = rf_connected
                self.is_rf_connected = rf_connected

                if rf_connected:
                    # Headset has just connected / turned on
                    batt = self.device.get_battery()
                    lvl = batt.get("level", 0)
                    chg = batt.get("charging", False)
                    self.sig_status_updated.emit({
                        "connected": True,
                        "level": lvl,
                        "charging": chg
                    })
                    # Fetch all hardware parameters from the active headset
                    self._sync_headset_settings()
                else:
                    # Headset has just disconnected / turned off
                    self.sig_status_updated.emit({
                        "connected": False,
                        "level": 0,
                        "charging": False
                    })
            elif rf_connected:
                # Routine battery update while connected
                batt = self.device.get_battery()
                lvl = batt.get("level", 0)
                chg = batt.get("charging", False)
                self.sig_status_updated.emit({
                    "connected": True,
                    "level": lvl,
                    "charging": chg
                })

        except Exception as e:
            self._handle_io_error(e)

    def _sync_headset_settings(self):
        if not self.device or not self.device.is_open or not self.is_rf_connected:
            return
        try:
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
                if self.voice_changer.current_effect_id != -1:
                    effects = {0: "Male", 1: "Female", 2: "Monster", 3: "Cartoon"}
                    eff_id = self.voice_changer.current_effect_id
                    self.sig_effect_updated.emit({
                        "enabled": True,
                        "effect_id": eff_id,
                        "effect_name": effects.get(eff_id, "Custom")
                    })
                else:
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
        try:
            self.voice_changer.cleanup()
        except Exception:
            pass
        self.is_port_open = False
        self.is_rf_connected = False
        self._last_rf_connected = None
        if self.device:
            try:
                self.device.disconnect()
            except Exception:
                pass
            self.device = None
        self.sig_connection_changed.emit(False, str(err))
        self.sig_status_updated.emit({"connected": False, "level": 0, "charging": False})
