#!/usr/bin/env python3
"""
Entry point for ATK Neptune N9 Linux Control Center.
Enforces a single-instance application using QLocalServer / QLocalSocket IPC.
If an instance is already running, launching again activates and raises the existing window.
"""

import sys
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

    def _handle_client_connection(self):
        client = self._server.nextPendingConnection()
        if client:
            client.readyRead.connect(lambda: self._read_client_message(client))

    def _read_client_message(self, client: QLocalSocket):
        msg = client.readAll().data().decode("utf-8", "ignore").strip()
        if "ACTIVATE" in msg and self.window:
            self.window.show_and_activate()
        client.disconnectFromServer()


def main():
    # Handle Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = SingleInstanceApp(sys.argv)
    app.setApplicationName("ATK Neptune N9 Control Center")
    app.setApplicationDisplayName("ATK Neptune N9")
    app.setQuitOnLastWindowClosed(False)

    if app.is_already_running():
        print("ATK Neptune N9 uygulaması zaten arka planda çalışıyor. Mevcut pencere öne getirildi.")
        sys.exit(0)

    window = MainWindow()
    app.setup_single_instance_server(window)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
