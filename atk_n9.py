#!/usr/bin/env python3
"""
ATK Neptune N9 (Pro / Ultra) Linux Native Driver & CLI Utility
Communicates with the ATK N9 headset via USB CDC-ACM Serial Interface (/dev/ttyACM*).
Audio is handled natively by PipeWire/ALSA; Media buttons by Linux hid-generic.
"""

import os
import sys
import glob
import time
import struct
import select
import termios
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

SUPPORTED_DEVICES = {
    (0x373B, 0x11CA): "ATK Neptune N9 Pro (Wired USB-C)",
    (0x373B, 0x11CB): "ATK Neptune N9 Pro (2.4GHz Dongle)",
    (0x373B, 0x1203): "ATK Neptune N9 Ultra (Wired USB-C)",
    (0x373B, 0x1204): "ATK Neptune N9 Ultra (2.4GHz Dongle)",
}

EQ_BANDS = ["32Hz", "64Hz", "125Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz", "16kHz"]

PRESET_PROFILES = {
    "flat": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "pop": [1, -1, 1, 0, -1, 0, 1, -2, -1, 0],
    "cs2": [-4, -4, -1, 0, 2, 5, 4, 1, 0, -2],
    "valorant1": [-3, -3, -1, 0, 2, 2, 4, 3, 1, 1],
    "valorant2": [-2, -1, 0, 5, -2, 1, 3, 2, -3, -1],
    "pubg": [-2, -2, -1, -1, 1, 2, 3, 2, 0, -2],
    "apex": [-1, 0, 0, -1, 1, 3, 4, 2, 1, 0],
    "overwatch": [-2, -2, 0, 1, 2, 3, 4, 2, 0, -1],
    "delta_force": [0, 0, 5, 3, 5, 2, 3, 2, 0, -5],
}

# Command Categories
class Cmd:
    AUTH = 0x00
    SPEAKER = 0x01
    MICROPHONE = 0x02
    EQ = 0x03
    EFFECT = 0x04
    SURROUND = 0x05
    REPORT = 0x80

# Subcommands
class SubCmd:
    # AUTH
    GET_BATTERY = 0x03
    GET_STATUS = 0x04
    
    # MICROPHONE
    MIC_GET_ALL = 0x00
    MIC_SET_ALL = 0x20
    MIC_SET_EN = 0x21
    MIC_SET_VOL = 0x22
    MIC_SET_MONITOR_EN = 0x23
    MIC_SET_MONITOR_VOL = 0x24
    
    # EQ
    EQ_GET_ALL = 0x00
    EQ_GET_ID = 0x01
    EQ_GET_DATA = 0x02
    EQ_SET_ALL = 0x20
    EQ_SET_ID = 0x21
    EQ_SET_DATA = 0x22
    
    # EFFECT (Voice Changer)
    EFFECT_GET_ALL = 0x00
    EFFECT_SET_ALL = 0x20
    EFFECT_SET_RESET = 0x21
    
    # SURROUND (Virtual 7.1)
    SURROUND_GET_ALL = 0x00
    SURROUND_SET_ALL = 0x20
    
    # Telemetry Reports (Async events)
    EVENT_BATTERY = 0x83
    EVENT_MIC_MUTE = 0xA1
    EVENT_MIC_MONITOR = 0xA3


def find_serial_port() -> Optional[str]:
    """Find the /dev/ttyACM* device corresponding to the ATK N9."""
    for p in sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyACM*")):
        real_path = Path(p).resolve()
        # Look up parent USB VID/PID in sysfs
        sys_device = Path("/sys/class/tty") / real_path.name / "device"
        if not sys_device.exists():
            continue
        cur = sys_device.resolve()
        while cur != cur.parent:
            vid_file = cur / "idVendor"
            pid_file = cur / "idProduct"
            if vid_file.exists() and pid_file.exists():
                try:
                    vid = int(vid_file.read_text().strip(), 16)
                    pid = int(pid_file.read_text().strip(), 16)
                    if (vid, pid) in SUPPORTED_DEVICES:
                        return str(real_path)
                except ValueError:
                    pass
                break
            cur = cur.parent
    return None


def configure_serial(fd: int):
    """Configure serial port to 9600 Baud, 8N1, Raw mode."""
    attrs = termios.tcgetattr(fd)
    attrs[0] = 0  # iflag
    attrs[1] = 0  # oflag
    attrs[2] &= ~(termios.CSIZE | termios.PARENB | termios.CSTOPB)
    attrs[2] |= termios.CS8 | termios.CREAD | termios.CLOCAL
    if hasattr(termios, "CRTSCTS"):
        attrs[2] &= ~termios.CRTSCTS
    attrs[3] = 0  # lflag
    attrs[4] = termios.B9600  # ispeed
    attrs[5] = termios.B9600  # ospeed
    attrs[6][termios.VMIN] = 0
    attrs[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    termios.tcflush(fd, termios.TCIOFLUSH)


class ATKNeptuneN9:
    def __init__(self, port: Optional[str] = None):
        self.port = port or find_serial_port()
        if not self.port:
            raise FileNotFoundError("ATK Neptune N9 device not found. Make sure dongle or cable is connected.")
        self.fd: Optional[int] = None
        self.rx_buffer = bytearray()

    def connect(self):
        self.fd = os.open(self.port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        configure_serial(self.fd)

    def disconnect(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def _read_packets(self, timeout: float = 0.05) -> List[bytes]:
        packets = []
        start = time.time()
        while time.time() - start < timeout:
            r, _, _ = select.select([self.fd], [], [], 0.02)
            if self.fd in r:
                chunk = os.read(self.fd, 64)
                if chunk:
                    self.rx_buffer.extend(chunk)
                    while len(self.rx_buffer) >= 64:
                        pkt = bytes(self.rx_buffer[:64])
                        del self.rx_buffer[:64]
                        packets.append(pkt)
            else:
                if not self.rx_buffer:
                    break
        return packets

    def transfer(self, cmd: int, subcmd: int, data: Optional[List[int]] = None, expected_len: int = -1, timeout: float = 0.8) -> Tuple[Optional[bytes], List[bytes]]:
        if data is None:
            data = []
        pkt = bytearray(64)
        pkt[0] = (len(data) + 2) if expected_len == -1 else expected_len
        pkt[1] = cmd
        pkt[2] = subcmd
        for i, val in enumerate(data):
            pkt[3 + i] = val & 0xFF
        
        # Flush unhandled packets
        self._read_packets(0.02)
        os.write(self.fd, bytes(pkt))
        
        start = time.time()
        async_events = []
        while time.time() - start < timeout:
            packets = self._read_packets(0.05)
            for p in packets:
                p_len = p[0]
                p_cmd = p[1]
                p_subcmd = p[2]
                if p_cmd == cmd and p_subcmd == subcmd:
                    return p, async_events
                else:
                    async_events.append(p)
        return None, async_events

    def get_status(self) -> Dict[str, Any]:
        """Check connection state between headset and dongle."""
        res, _ = self.transfer(Cmd.AUTH, SubCmd.GET_STATUS)
        if not res:
            return {"connected": False, "error": "Timeout"}
        return {"connected": res[4] == 1}

    def get_battery(self) -> Dict[str, Any]:
        """Read battery level and charging status."""
        res, _ = self.transfer(Cmd.AUTH, SubCmd.GET_BATTERY)
        if not res:
            return {"error": "Timeout"}
        raw_val = res[4]
        is_charging = (raw_val >> 7) == 1
        level = raw_val & 0x7F
        return {
            "level": level,
            "charging": is_charging,
            "connected": True
        }

    def get_microphone_info(self) -> Dict[str, Any]:
        """Read microphone volume, mute state, and sidetone monitor settings."""
        res, _ = self.transfer(Cmd.MICROPHONE, SubCmd.MIC_GET_ALL, [1], expected_len=4)
        if not res:
            return {"error": "Timeout"}
        return {
            "mute": res[3] == 1,
            "volume": res[4],
            "sidetone_enabled": res[5] == 1,
            "sidetone_volume": res[6],
        }

    def set_microphone_info(self, mute: bool, volume: int, sidetone_enabled: bool, sidetone_volume: int) -> bool:
        """Configure microphone parameters and sidetone."""
        data = [
            1 if mute else 0,
            max(0, min(100, volume)),
            1 if sidetone_enabled else 0,
            max(0, min(100, sidetone_volume))
        ]
        res, _ = self.transfer(Cmd.MICROPHONE, SubCmd.MIC_SET_ALL, data)
        return res is not None

    def get_eq_profile(self) -> Dict[str, Any]:
        """Read active EQ ID and the 10 frequency bands for the active profile."""
        res_id, _ = self.transfer(Cmd.EQ, SubCmd.EQ_GET_ID)
        if not res_id:
            return {"error": "Timeout getting EQ ID"}
        eq_id = res_id[3]
        
        res_data, _ = self.transfer(Cmd.EQ, SubCmd.EQ_GET_DATA, [eq_id])
        if not res_data:
            return {"error": "Timeout getting EQ Data", "eq_id": eq_id}
            
        payload_len = res_data[0] - 2
        raw_bands = res_data[3:3+payload_len]
        bands = [b if b < 128 else b - 256 for b in raw_bands]
        bands_dict = {EQ_BANDS[i]: bands[i] for i in range(min(len(EQ_BANDS), len(bands)))}
        return {
            "eq_id": eq_id,
            "bands_raw": bands,
            "bands": bands_dict
        }

    def set_eq_bands(self, eq_id: int, bands: List[int]) -> bool:
        """Set EQ values (-20 dB to +20 dB) for 10 bands."""
        if len(bands) != 10:
            raise ValueError("Exactly 10 frequency bands required.")
        raw_bytes = [b if b >= 0 else (b + 256) for b in bands]
        data = [eq_id] + raw_bytes
        res, _ = self.transfer(Cmd.EQ, SubCmd.EQ_SET_ALL, data)
        return res is not None

    def get_surround(self) -> Dict[str, Any]:
        """Check virtual 7.1 surround sound status."""
        res, _ = self.transfer(Cmd.SURROUND, SubCmd.SURROUND_GET_ALL)
        if not res:
            return {"error": "Timeout"}
        return {
            "enabled": res[3] == 1,
            "params": list(res[4:6])
        }

    def set_surround(self, enable: bool) -> bool:
        """Enable or disable virtual 7.1 surround sound."""
        res, _ = self.transfer(Cmd.SURROUND, SubCmd.SURROUND_SET_ALL, [1 if enable else 0, 0, 0, 0])
        return res is not None

    def get_effect(self) -> Dict[str, Any]:
        """Read voice changer effect state."""
        res, _ = self.transfer(Cmd.EFFECT, SubCmd.EFFECT_GET_ALL)
        if not res:
            return {"error": "Timeout"}
        effects = {0: "Male", 1: "Female", 2: "Monster", 3: "Cartoon"}
        enabled = res[3] == 1
        effect_id = res[4]
        return {
            "enabled": enabled,
            "effect_id": effect_id,
            "effect_name": effects.get(effect_id, "Unknown")
        }


def print_status(dev: ATKNeptuneN9):
    status = dev.get_status()
    batt = dev.get_battery()
    mic = dev.get_microphone_info()
    eq = dev.get_eq_profile()
    surround = dev.get_surround()
    effect = dev.get_effect()

    print("=" * 60)
    print("             ATK NEPTUNE N9 - DEVICE STATUS")
    print("=" * 60)
    print(f"Device Port       : {dev.port}")
    print(f"Wireless Status   : {'Connected' if status.get('connected') else 'Disconnected'}")
    if batt.get("level") is not None:
        charging_str = " (⚡ Charging)" if batt.get("charging") else ""
        print(f"Battery Level     : {batt.get('level')}%{charging_str}")
    
    print("-" * 60)
    print("Microphone & Sidetone:")
    print(f"  Mute            : {'MUTED' if mic.get('mute') else 'ACTIVE'}")
    print(f"  Mic Volume      : {mic.get('volume')}%")
    print(f"  Sidetone        : {'Enabled' if mic.get('sidetone_enabled') else 'Disabled'}")
    print(f"  Sidetone Volume : {mic.get('sidetone_volume')}%")
    
    print("-" * 60)
    print("Audio Enhancements:")
    print(f"  Virtual 7.1     : {'ON' if surround.get('enabled') else 'OFF'}")
    print(f"  Voice Changer   : {effect.get('effect_name') if effect.get('enabled') else 'OFF'}")
    
    print("-" * 60)
    print(f"Equalizer Profile (ID {eq.get('eq_id', '?')}):")
    if "bands" in eq:
        for band, val in eq["bands"].items():
            bar = "#" * max(0, val + 20)
            print(f"  {band:>6} : {val:+3d} dB  |{bar}")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python3 atk_n9.py [status|sidetone on/off [vol]|preset <name>]")
        sys.exit(0)

    try:
        with ATKNeptuneN9() as dev:
            if len(sys.argv) > 1:
                cmd = sys.argv[1].lower()
                if cmd == "status":
                    print_status(dev)
                elif cmd == "sidetone":
                    action = sys.argv[2].lower() if len(sys.argv) > 2 else "on"
                    vol = int(sys.argv[3]) if len(sys.argv) > 3 else 100
                    cur = dev.get_microphone_info()
                    en = (action == "on")
                    dev.set_microphone_info(cur.get("mute", False), cur.get("volume", 100), en, vol)
                    print(f"Sidetone set to {'ON' if en else 'OFF'} at {vol}%.")
                elif cmd == "preset":
                    pname = sys.argv[2].lower() if len(sys.argv) > 2 else "flat"
                    if pname not in PRESET_PROFILES:
                        print(f"Unknown preset. Available: {list(PRESET_PROFILES.keys())}")
                    else:
                        bands = PRESET_PROFILES[pname]
                        dev.set_eq_bands(5, bands)
                        print(f"Applied preset '{pname}': {bands}")
                else:
                    print(f"Unknown command: {cmd}")
            else:
                print_status(dev)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
