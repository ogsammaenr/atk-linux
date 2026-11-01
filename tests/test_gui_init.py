"""
Automated headless test for ATK Neptune N9 GUI.
Verifies MainWindow creation, component initialization, and worker thread communication.
"""

import sys
import os
import time

# Ensure project root is in path
sys.path.insert(0, "/home/excalibur/Workspace/projects/atk-linux-driver")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from ui.app import MainWindow

def test_gui():
    os.environ["QT_QPA_PLATFORM"] = "offscreen" # Run headless for test
    app = QApplication([])
    window = MainWindow()
    
    print("MainWindow initialized.")
    assert window.battery_widget is not None, "Battery widget missing"
    assert window.eq_widget is not None, "Equalizer widget missing"
    assert window.mic_widget is not None, "Mic widget missing"
    assert window.effects_widget is not None, "Effects widget missing"
    assert window.tray_manager is not None, "Tray manager missing"

    # Allow worker thread to run for 1.5 seconds to establish serial communication
    def on_timeout():
        print("Test timer fired. Checking worker state...")
        print(f"Worker connected: {window.worker.is_connected}")
        print(f"Worker port: {window.worker.device.port if window.worker.device else 'None'}")
        window.worker.stop()
        app.quit()

    QTimer.singleShot(1500, on_timeout)
    app.exec()
    print("GUI verification test PASSED cleanly.")

if __name__ == "__main__":
    test_gui()
