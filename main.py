#!/usr/bin/env python3
"""
Entry point for ATK Neptune N9 Linux Control Center.
Enforces a single-instance application using QLocalServer / QLocalSocket IPC.
If an instance is already running, launching again activates and raises the existing window.
"""

import sys
import json
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from ui.app import MainWindow

SOCKET_NAME = "atk_neptune_n9_single_instance_socket"


class SingleInstanceApp(QApplication):
    def __init__(self, argv, socket_name=SOCKET_NAME):
        super().__init__(argv)
        self.socket_name = socket_name
        self._server = None
        self.window = None

    def query_server(self, command: str) -> str | None:
        """Query running primary instance and return response string if connected."""
        socket = QLocalSocket()
        socket.connectToServer(self.socket_name)
        if socket.waitForConnected(500):
            socket.write((command + "\n").encode("utf-8"))
            socket.flush()
            socket.waitForBytesWritten(500)
            
            # Read response
            resp = bytearray()
            while socket.waitForReadyRead(500):
                chunk = socket.readAll().data()
                if not chunk:
                    break
                resp.extend(chunk)
            socket.disconnectFromServer()
            return resp.decode("utf-8", "ignore").strip()
        return None

    def is_already_running(self) -> bool:
        socket = QLocalSocket()
        socket.connectToServer(self.socket_name)
        if socket.waitForConnected(500):
            # Tell the existing instance to show and bring itself to front
            socket.write(b"ACTIVATE\n")
            socket.flush()
            socket.waitForBytesWritten(500)
            socket.disconnectFromServer()
            return True
        return False

    def setup_single_instance_server(self, window: MainWindow):
        self.window = window
        # Remove any stale socket file left from an abrupt system reboot/crash
        QLocalServer.removeServer(self.socket_name)
        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._handle_client_connection)
        self._server.listen(self.socket_name)
        self.aboutToQuit.connect(self.cleanup)

    def cleanup(self):
        if self._server:
            try:
                self._server.close()
            except Exception:
                pass
            self._server = None
        QLocalServer.removeServer(self.socket_name)

    def _handle_client_connection(self):
        client = self._server.nextPendingConnection()
        if client:
            client.readyRead.connect(lambda: self._read_client_message(client))

    def _read_client_message(self, client: QLocalSocket):
        msg = client.readAll().data().decode("utf-8", "ignore").strip()
        if "GET_JSON" in msg and self.window:
            payload = self.window.get_telemetry_json()
            client.write(payload.encode("utf-8"))
            client.flush()
            client.waitForBytesWritten(500)
        elif "ACTIVATE" in msg and self.window:
            self.window.show_and_activate()
        client.disconnectFromServer()


def main():
    # Handle Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = SingleInstanceApp(sys.argv)
    app.setApplicationName("ATK Neptune N9 Control Center")
    app.setApplicationDisplayName("ATK Neptune N9")
    app.setQuitOnLastWindowClosed(False)

    # 1. Handle --json flag (CLI status endpoint)
    if "--json" in sys.argv or (len(sys.argv) > 1 and sys.argv[1].lower() == "json"):
        # If GUI is running, fetch telemetry over IPC socket
        running_json = app.query_server("GET_JSON")
        if running_json:
            print(running_json)
            sys.exit(0)

        # Standalone: read directly from hardware
        from atk_n9 import ATKNeptuneN9, get_device_status_dict
        try:
            with ATKNeptuneN9() as dev:
                data = get_device_status_dict(dev)
                print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({
                "connected": False,
                "error": str(e),
                "text": "N/A",
                "class": "disconnected"
            }))
        sys.exit(0)

    # 2. Check single instance
    start_minimized = "--minimized" in sys.argv or "--tray" in sys.argv
    if app.is_already_running():
        if not start_minimized:
            print("ATK Neptune N9 uygulaması zaten arka planda çalışıyor. Mevcut pencere öne getirildi.")
        sys.exit(0)

    # 3. Create main window
    window = MainWindow()
    app.setup_single_instance_server(window)

    if not start_minimized:
        window.show()

    ret = app.exec()
    app.cleanup()
    sys.exit(ret)


if __name__ == "__main__":
    main()
