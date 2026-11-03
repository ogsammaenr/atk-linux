"""
Automated tests for settings persistence and application exit behavior.
"""

import sys
import os
import json
import shutil
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, "/home/excalibur/Workspace/projects/atk-linux-driver")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QCloseEvent
from ui.config import ConfigManager, resolve_config_dir
from ui.app import MainWindow


def test_config_manager(tmp_path: Path):
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    cfg = ConfigManager()

    assert cfg.config_dir.exists(), "Config directory was not created"
    assert (tmp_path / "atk-neptune-n9").exists(), "Alias symlink atk-neptune-n9 missing"

    # Default values
    assert cfg.get("language") == "tr"
    assert cfg.get("minimize_to_tray") is True

    # Modify and check persistence
    cfg.set("minimize_to_tray", False)
    cfg.set("language", "en")

    # Reload from disk
    cfg2 = ConfigManager()
    assert cfg2.get("minimize_to_tray") is False
    assert cfg2.get("language") == "en"

    # Verify JSON file structure
    raw = json.loads(cfg2.config_file.read_text(encoding="utf-8"))
    assert raw["minimize_to_tray"] is False
    assert raw["language"] == "en"


def test_main_window_settings_and_exit(tmp_path: Path):
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)

    from ui.config import CONFIG
    CONFIG.reload()

    app = QApplication.instance() or QApplication([])

    # 1. Start with minimize_to_tray = False saved in config
    CONFIG.set("minimize_to_tray", False)

    win = MainWindow()
    assert win.minimize_to_tray is False, "MainWindow did not load minimize_to_tray=False from config"
    assert win.tray_check.isChecked() is False, "Checkbox is not unchecked"

    # 2. Toggle checkbox back to True
    win.tray_check.setChecked(True)
    assert win.minimize_to_tray is True
    assert CONFIG.get("minimize_to_tray") is True

    # 3. Test close when minimize_to_tray is True (should ignore close and remain open/hidden)
    close_ev = QCloseEvent()
    win.closeEvent(close_ev)
    assert not close_ev.isAccepted(), "closeEvent should be ignored when minimize_to_tray is True"

    # 4. Toggle back to False
    win.tray_check.setChecked(False)
    assert win.minimize_to_tray is False
    assert CONFIG.get("minimize_to_tray") is False

    # 5. Test close when minimize_to_tray is False (should accept and quit)
    close_ev2 = QCloseEvent()
    win.closeEvent(close_ev2)
    assert close_ev2.isAccepted(), "closeEvent should be accepted when minimize_to_tray is False"

    # Worker thread should be stopped
    assert not win.worker.isRunning(), "Worker thread should be stopped after exit"

    # 6. Test autostart toggle
    win2 = MainWindow()
    assert hasattr(win2, "autostart_check"), "Autostart checkbox missing"
    win2.autostart_check.setChecked(True)
    assert (tmp_path / "autostart" / "atk-neptune-n9.desktop").exists()
    win2.autostart_check.setChecked(False)
    assert not (tmp_path / "autostart" / "atk-neptune-n9.desktop").exists()

    # 7. Test Telemetry JSON output
    t_json = win2.get_telemetry_json()
    t_data = json.loads(t_json)
    assert "battery" in t_data
    assert "mic" in t_data
    assert "audio" in t_data

    # 8. Test VU meter page change activation
    assert hasattr(win2.mic_widget, "vu_meter"), "VU meter missing in mic widget"
    win2.pages_stack.setCurrentIndex(2) # Mic page
    assert win2.mic_widget.vu_meter._monitoring is True, "VU meter should monitor on mic page"
    win2.pages_stack.setCurrentIndex(0) # Dashboard
    assert win2.mic_widget.vu_meter._monitoring is False, "VU meter should sleep on other pages"

    win2.close()


if __name__ == "__main__":
    tmp = Path("/tmp/atk_test_config")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    
    print("Running test_config_manager...")
    test_config_manager(tmp)
    print("test_config_manager PASSED.")

    print("Running test_main_window_settings_and_exit...")
    test_main_window_settings_and_exit(tmp)
    print("test_main_window_settings_and_exit PASSED.")

    if tmp.exists():
        shutil.rmtree(tmp)
    print("ALL TESTS PASSED.")
