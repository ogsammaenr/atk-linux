# ATK Neptune N9 Linux Driver & Control Center

Native Linux userspace driver and modern PyQt6 desktop control center for **ATK Neptune N9 (Pro & Ultra)** wireless gaming headsets.

---

## Features

- **Real-Time Battery & Status:** Dynamic battery gauge with charging indicator and low-battery desktop notifications.
- **System Tray (Tray Icon):** Battery level tooltip, quick sidetone toggle, minimize-to-tray on close.
- **10-Band Parametric Equalizer:**
  - 10 hardware frequency bands: `32Hz`, `64Hz`, `125Hz`, `250Hz`, `500Hz`, `1kHz`, `2kHz`, `4kHz`, `8kHz`, `16kHz` (`-20 dB` to `+20 dB`).
  - Dynamic Bezier curve canvas updating in real time.
  - Official gaming presets (CS2, Valorant 1 & 2, PUBG, Apex Legends, Pop, Delta Force, Flat).
- **Microphone & Sidetone (Hardware Monitor):**
  - Zero-latency hardware sidetone toggle & volume slider (hear your own voice clearly).
  - Microphone gain slider & hardware mute switch (syncs with physical headset mute button/flip).
- **Virtual 7.1 Surround & Voice Changer:**
  - Spatial 7.1 surround sound toggle.
  - Voice Changer DSP effects (Male, Female, Monster, Cartoon).

---

## Quick Start

### 1. Launch GUI
```bash
cd /home/excalibur/Workspace/projects/atk-linux-driver
./run_gui.sh
```

### 2. Desktop Shortcut (Optional)
```bash
cp atk-neptune-n9.desktop ~/.local/share/applications/
```

### 3. CLI Usage (Terminal without GUI)
```bash
python3 atk_n9.py status
python3 atk_n9.py sidetone on 100
python3 atk_n9.py preset cs2
python3 atk_n9.py preset flat
```

---

## Architecture & Protocol Documentation

Detailed technical specification, USB composite topology, packet framing, and reverse engineering notes:
- [ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md](file:///home/excalibur/Workspace/projects/atk-linux-driver/ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md)
