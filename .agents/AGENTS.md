# AI Agent Developer Guide: ATK Neptune N9 Linux Control Center

Welcome, AI Agent! This document is your comprehensive entry point to navigating, understanding, and modifying the **ATK Neptune N9 Linux Driver & Control Center** codebase.

---

## 1. Project Mission & Overview

This project is a native Linux userspace driver and ultra-modern desktop control center for **ATK Neptune N9 (Pro & Ultra)** 2.4GHz wireless / USB-C wired gaming headsets.

It replaces the proprietary Windows ATK Hub software on Linux by implementing:
- Direct hardware serial control over USB CDC-ACM (`/dev/ttyACM*`).
- Real-time battery telemetry, charging status, and RF wireless link detection.
- 10-band hardware parametric DSP equalizer with gaming presets (CS2, Valorant, Apex, PUBG).
- Zero-latency hardware sidetone (monitor) volume & toggle.
- Hardware microphone gain slider and mute switch synchronization.
- Virtual 7.1 spatial surround sound and DSP voice changer effects (Male, Female, Monster, Cartoon).
- Real-time PipeWire audio VU meter.
- Modern PyQt6 dark esports GUI with system tray, autostart, and i18n (TR/EN).
- High-speed IPC and CLI JSON endpoint (`--json`) for status bars (Waybar, Polybar, etc.).

---

## 2. Quick Navigation for Agents

| Document | Purpose |
|---|---|
| [AGENTS.md](file:///home/excalibur/Workspace/projects/atk-linux-driver/.agents/AGENTS.md) | **You are here.** Master guide and navigation index. |
| [ARCHITECTURE.md](file:///home/excalibur/Workspace/projects/atk-linux-driver/.agents/ARCHITECTURE.md) | Threading model, IPC socket, state management, and lifecycle. |
| [HARDWARE_PROTOCOL.md](file:///home/excalibur/Workspace/projects/atk-linux-driver/.agents/HARDWARE_PROTOCOL.md) | 64-byte packet layout, commands, subcommands, and payload tables. |
| [ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md](file:///home/excalibur/Workspace/projects/atk-linux-driver/ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md) | Complete reverse-engineering notes, endpoint dumps, and USB framing. |

---

## 3. Repository File Manifest

```
atk-linux-driver/
├── .agents/
│   ├── AGENTS.md                  # Master developer & AI agent guide (this file)
│   ├── ARCHITECTURE.md            # Concurrency, IPC, and design pattern details
│   └── HARDWARE_PROTOCOL.md       # Packet structure and command quick reference
├── atk_n9.py                      # Core hardware driver, CDC-ACM serial engine, and CLI
├── main.py                        # Single-instance application entry point & IPC server
├── run_gui.sh                     # Launcher bash script (activates .venv and passes args)
├── atk-neptune-n9.desktop         # Standard XDG desktop entry file
├── requirements.txt               # Dependencies (PyQt6)
├── ATK_NEPTUNE_N9_PROTOCOL_ANALYSIS.md # Full hardware disassembly and packet capture logs
├── README.md                      # End-user documentation
├── udev/
│   └── 99-atk-n9.rules            # Udev rules granting non-root access to CDC-ACM and hidraw
├── tests/
│   ├── test_gui_init.py           # Automated test for MainWindow and worker lifecycle
│   ├── test_single_instance.py    # Automated test for single-instance socket and activation
│   └── test_settings_and_exit.py  # Automated test for config, autostart, and exit behavior
└── ui/
    ├── app.py                     # Main window (navigation, cards, statusbar, signal wiring)
    ├── config.py                  # Persistent settings (~/.config/atk-n9/settings.json) & autostart
    ├── i18n.py                    # Multi-language translation engine (TR / EN)
    ├── styles.py                  # Dark esports stylesheet (QSS)
    ├── tray.py                    # System tray manager with battery indicator icon
    ├── worker.py                  # Background QThread handling non-blocking serial communication
    └── components/
        ├── battery_widget.py      # Glowing battery pill and header status badges
        ├── eq_widget.py           # 10-band DSP parametric EQ with interactive Bezier canvas
        ├── mic_widget.py          # Microphone gain, hardware mute toggle, and sidetone controls
        ├── vu_meter.py            # Live PipeWire audio VU meter (QtMultimedia QAudioSource)
        ├── effects_widget.py      # Spatial 7.1 surround visualizer and voice changer buttons
        └── toggle_switch.py       # Custom animated modern pill toggle switch
```

---

## 4. Key Architectural Rules & Gotchas for Agents

> [!CAUTION]
> **Rule 1: Serial Port Concurrency**
> Never attempt to open `/dev/ttyACM*` directly if the GUI application is running. The GUI background thread ([ui/worker.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/worker.py)) maintains an open serial descriptor. If you need telemetry from a CLI script, use `SingleInstanceApp.query_server("GET_JSON")` or invoke `./run_gui.sh --json`.

> [!IMPORTANT]
> **Rule 2: Headless Test Execution**
> When executing tests or verifying Qt components in terminal environments without an active display server, always prefix with `QT_QPA_PLATFORM=offscreen`.
>
> Example:
> ```bash
> QT_QPA_PLATFORM=offscreen .venv/bin/python3 -m unittest ...
> ```

> [!WARNING]
> **Rule 3: One QApplication Per Process**
> In PyQt6, instantiating more than one `QApplication` instance in the same Python process corrupts Qt's internal static pointers and causes `SIGSEGV (139)` on exit. In unit tests, reuse `QApplication.instance() or QApplication([])`.

> [!NOTE]
> **Rule 4: Multi-Language (i18n)**
> Every user-facing string MUST use `I18N.t("key_name")`. Never hardcode user strings in widgets. Add both Turkish (`tr`) and English (`en`) translations in [ui/i18n.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/i18n.py).

> [!NOTE]
> **Rule 5: Atomic Configuration Writes**
> Persistent user settings must be saved through `CONFIG.set(key, value)` in [ui/config.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/config.py). It writes to a temporary file before replacing to prevent corruption.

---

## 5. Development & Testing Workflow

### 5.1 Environment Setup
The project uses a Python 3.14 virtual environment located in `.venv`:
- Python binary: `.venv/bin/python3`
- PIP binary: `.venv/bin/pip`
- GUI Launcher: `./run_gui.sh`

### 5.2 Verification Suite
Whenever you make changes to core drivers, UI components, or settings, run the full automated verification suite:

```bash
# 1. Component initialization and background worker test:
.venv/bin/python3 tests/test_gui_init.py

# 2. Single-instance IPC socket test:
.venv/bin/python3 tests/test_single_instance.py

# 3. Settings persistence, autostart, and clean exit test:
.venv/bin/python3 tests/test_settings_and_exit.py

# 4. CLI JSON telemetry tests (standalone & IPC):
./run_gui.sh --json
.venv/bin/python3 atk_n9.py --json
```

All commands must exit with code `0`.

---

## 6. Common Modification Recipes

### How to add a new hardware parameter
1. Add the command/subcommand IDs to `Cmd` and `SubCmd` in [atk_n9.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/atk_n9.py).
2. Implement getter/setter methods on `ATKNeptuneN9` using `self.transfer(cmd, subcmd, data)`.
3. In [ui/worker.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/worker.py), add a handling branch inside `_execute_command(self, cmd)` and define a Qt signal to emit state to the UI.
4. In [ui/app.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/app.py), connect the widget to call `self.worker.queue_command(...)`.

### How to add a new user setting
1. Define the default value in `DEFAULT_SETTINGS` in [ui/config.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/config.py).
2. In [ui/app.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/app.py) `_build_info_page()`, create the corresponding widget (e.g. `QCheckBox`).
3. Connect the widget to call `CONFIG.set(key, value)`.
4. Add localization keys to both `"tr"` and `"en"` dictionaries in [ui/i18n.py](file:///home/excalibur/Workspace/projects/atk-linux-driver/ui/i18n.py).
