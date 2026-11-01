"""
Automated test for Single-Instance IPC functionality.
"""

import sys
import os
import time

sys.path.insert(0, "/home/excalibur/Workspace/projects/atk-linux-driver")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QLocalSocket
from PyQt6.QtCore import QTimer
from main import SingleInstanceApp, MainWindow, SOCKET_NAME

def test_single_instance():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    
    # 1. Start Primary
    app1 = SingleInstanceApp([])
    assert not app1.is_already_running(), "First instance should not detect running server"
    win1 = MainWindow()
    app1.setup_single_instance_server(win1)
    
    # Flag to track activation message
    activated = [False]
    orig_show_and_activate = win1.show_and_activate
    def mock_activate():
        activated[0] = True
        orig_show_and_activate()
    win1.show_and_activate = mock_activate

    # 2. Start Secondary
    app2 = SingleInstanceApp([])
    is_running = app2.is_already_running()
    print("Second instance detected running primary:", is_running)
    assert is_running is True, "Second instance MUST detect primary server!"

    # Process events on app1 to handle the connection
    def check_result():
        print("Checking if primary received ACTIVATE signal:", activated[0])
        assert activated[0] is True, "Primary window should have received ACTIVATE signal!"
        win1.tray_manager.cleanup()
        win1.worker.stop()
        app1.quit()

    QTimer.singleShot(400, check_result)
    app1.exec()
    print("Single instance test PASSED successfully!")

if __name__ == "__main__":
    test_single_instance()
