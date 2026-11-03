# ATK Neptune N9 Hardware & Protocol Specification

This document provides a concise protocol reference for AI agents working on device communication in `atk_n9.py` and `ui/worker.py`. For the full reverse engineering disassembly, refer to [ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md](../ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md).

---

## 1. Supported Devices & USB Identifiers

| Model | Mode | USB VID:PID | Linux Interface | Endpoint |
|---|---|---|---|---|
| **ATK Neptune N9 Pro** | Wired USB-C | `373B:11CA` | USB CDC-ACM | `/dev/ttyACM*` |
| **ATK Neptune N9 Pro** | 2.4GHz Wireless Dongle | `373B:11CB` | USB CDC-ACM | `/dev/ttyACM*` |
| **ATK Neptune N9 Ultra**| Wired USB-C | `373B:1203` | USB CDC-ACM | `/dev/ttyACM*` |
| **ATK Neptune N9 Ultra**| 2.4GHz Wireless Dongle | `373B:1204` | USB CDC-ACM | `/dev/ttyACM*` |

> [!NOTE]
> Audio playback and recording are standard USB Audio Class 1.0 (PipeWire / ALSA driver: `snd-usb-audio`). Hardware multimedia buttons (Volume, Play/Pause) are handled by the Linux kernel HID subsystem (`hid-generic`). Serial CDC-ACM controls DSP parameters and telemetry.

---

## 2. Serial Port Configuration

- **Baud Rate:** 9600 Baud
- **Data Bits:** 8
- **Stop Bits:** 1
- **Parity:** None (8N1)
- **Flow Control:** None (No RTS/CTS, No XON/XOFF)
- **Port Discovery:** `find_serial_port()` resolves `/dev/serial/by-id/*` and `/dev/ttyACM*` devices and reads `idVendor` / `idProduct` via sysfs (`/sys/class/tty/<device>/device/idVendor`).

---

## 3. Packet Framing Architecture

All requests and responses use **fixed 64-byte packets**:

```
+-----------+------------+---------------+-------------------------------------+
| Byte 0    | Byte 1     | Byte 2        | Bytes 3 .. 63                       |
| Length    | Command ID | Subcommand ID | Data Payload & Zero-Padding         |
+-----------+------------+---------------+-------------------------------------+
```

- **Byte 0:** Payload length (typically `len(data) + 2` or command header size).
- **Byte 1:** Primary command category (`Cmd`).
- **Byte 2:** Subcommand action (`SubCmd`).
- **Bytes 3..63:** Payload parameters, padded with `0x00` to exactly 64 bytes.

---

## 4. Command & Subcommand Reference

### 4.1 Authentication & Status (`Cmd.AUTH = 0x01`)

| Action | Cmd | SubCmd | Request Payload | Response Meaning |
|---|---|---|---|---|
| **Handshake / Init** | `0x01` | `0x01` | `[]` | Dongle acknowledgment |
| **Wireless Link Status** | `0x01` | `0x02` | `[]` | `res[4] == 1`: Headset linked via RF; `res[4] == 0`: Disconnected |
| **Battery & Charging** | `0x01` | `0x03` | `[]` | `res[4] & 0x7F`: Battery (0-100%); `(res[4] >> 7) == 1`: Charging |

### 4.2 Microphone & Sidetone (`Cmd.MIC = 0x02`)

| Action | Cmd | SubCmd | Payload Structure | Notes |
|---|---|---|---|---|
| **Get Microphone Info** | `0x02` | `0x10` | `[]` | `res[3]`: Mute (`1`=muted), `res[4]`: Mic Vol (0-100), `res[5]`: Sidetone En (`1`=on), `res[6]`: Sidetone Vol (0-100) |
| **Set Microphone Info** | `0x02` | `0x10` | `[mute, mic_vol, sidetone_en, sidetone_vol]` | Writes complete microphone state |
| **Set Sidetone** | `0x02` | `0x13` | `[enabled (0/1), volume (0-100)]` | Zero-latency hardware audio loopback |
| **Set Mic Mute** | `0x02` | `0x11` | `[mute (0/1)]` | Hardware mic muting |
| **Set Mic Volume** | `0x02` | `0x12` | `[volume (0-100)]` | Hardware mic preamp gain |

### 4.3 Equalizer DSP (`Cmd.EQ = 0x03`)

- **Bands (10 Hz frequencies):** `32Hz`, `64Hz`, `125Hz`, `250Hz`, `500Hz`, `1kHz`, `2kHz`, `4kHz`, `8kHz`, `16kHz`.
- **Value Range:** `-20 dB` to `+20 dB` (signed integers).

| Action | Cmd | SubCmd | Payload Structure |
|---|---|---|---|
| **Get EQ Profile** | `0x03` | `0x11` | `[]` -> `res[3]`: active EQ ID, `res[4..13]`: signed 8-bit band values |
| **Set EQ Profile** | `0x03` | `0x10` | `[eq_id, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9]` |

### 4.4 Spatial 7.1 Surround & Voice Changer (`Cmd.AUDIO = 0x04`)

| Action | Cmd | SubCmd | Payload Structure | Notes |
|---|---|---|---|---|
| **Get 7.1 Surround** | `0x04` | `0x10` | `[]` | `res[3] == 1`: Enabled, `0`: Disabled |
| **Set 7.1 Surround** | `0x04` | `0x10` | `[0x01]` (on) / `[0x00]` (off) | Internal hardware 7.1 virtual spatializer |
| **Get Voice Effect** | `0x04` | `0x20` | `[]` | `res[3] == 1`: Active; `res[4]`: Effect ID |
| **Set Voice Effect** | `0x04` | `0x20` | `[effect_id]` | `0`: Male, `1`: Female, `2`: Monster, `3`: Cartoon |
| **Disable Voice Effect**| `0x04` | `0x20` | `[0xFF]` | Normal voice (DSP bypass) |

---

## 5. Serial Port Concurrency Rule

> [!CAUTION]
> **Serial Bus Ownership Rule:**
> In Linux, only **one** process should actively read/write to `/dev/ttyACM0` at any time. When the GUI is active, [ui/worker.py](../ui/worker.py) holds the open file descriptor.
>
> Any CLI command querying telemetry (e.g. `run_gui.sh --json` or `main.py --json`) **must first check the IPC socket** (`SingleInstanceApp.query_server("GET_JSON")`). Only if the GUI is not running may a process open `/dev/ttyACM0` directly.
