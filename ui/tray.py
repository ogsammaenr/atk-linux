"""
System Tray Manager for ATK Neptune N9 Linux Driver.
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import pyqtSignal, QObject


def create_tray_pixmap(level: int = 100, connected: bool = True) -> QPixmap:
    """Generates an icon with battery color accent and level."""
    pix = QPixmap(32, 32)
    pix.fill(QColor(0, 0, 0, 0)) # transparent

    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Base circle / headset indicator
    bg_color = QColor("#18191E")
    painter.setBrush(bg_color)
    painter.setPen(QColor("#2C2D35"))
    painter.drawRoundedRect(2, 2, 28, 28, 6, 6)

    if not connected:
        painter.setPen(QColor("#FF4B5C"))
        painter.setFont(QFont("sans-serif", 10, QFont.Weight.Bold))
        painter.drawText(pix.rect(), 0x0084, "✕")
        painter.end()
        return pix

    # Color by level
    if level > 40:
        c = QColor("#00F5A0") # Green
    elif level > 15:
        c = QColor("#FFB800") # Yellow
    else:
        c = QColor("#FF4B5C") # Red

    # Dot in top right
    painter.setBrush(c)
    painter.setPen(QColor("#000000"))
    painter.drawEllipse(20, 4, 8, 8)

    # Headset symbol or percentage in center
    painter.setPen(QColor("#FFFFFF"))
    painter.setFont(QFont("sans-serif", 8, QFont.Weight.Bold))
    txt = f"{level}" if level < 100 else "N9"
    painter.drawText(2, 6, 26, 20, 0x0084, txt)
    painter.end()
    return pix


class TrayManager(QObject):
    sig_show_window = pyqtSignal()
    sig_toggle_sidetone = pyqtSignal()
    sig_quit_app = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray = QSystemTrayIcon(parent)
        self.tray.setIcon(QIcon(create_tray_pixmap(90, True)))
        self.tray.setToolTip("ATK Neptune N9 Kontrol Merkezi")

        # Build context menu
        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #18191E;
                color: #FFFFFF;
                border: 1px solid #2C2D35;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 6px 18px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #00D2FF;
                color: #0B0C0E;
                font-weight: 600;
            }
            QMenu::separator {
                height: 1px;
                background-color: #2C2D35;
                margin: 4px 6px;
            }
        """)

        self.title_action = self.menu.addAction("🎧 ATK Neptune N9")
        self.title_action.setEnabled(False)

        self.battery_action = self.menu.addAction("Pil: --%")
        self.battery_action.setEnabled(False)

        self.menu.addSeparator()

        self.sidetone_action = self.menu.addAction("Yan Tonu Aç / Kapat")
        self.sidetone_action.triggered.connect(self.sig_toggle_sidetone.emit)

        self.menu.addSeparator()

        self.show_action = self.menu.addAction("Arayüzü Göster")
        self.show_action.triggered.connect(self.sig_show_window.emit)

        self.quit_action = self.menu.addAction("Çıkış")
        self.quit_action.triggered.connect(self.sig_quit_app.emit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger: # Left click
            self.sig_show_window.emit()

    def update_status(self, connected: bool, battery: int = 0, charging: bool = False):
        self.tray.setIcon(QIcon(create_tray_pixmap(battery, connected)))
        if connected:
            chg = " (Şarjda)" if charging else ""
            self.battery_action.setText(f"Pil: %{battery}{chg}")
            self.tray.setToolTip(f"ATK Neptune N9 - %{battery}{chg}")
        else:
            self.battery_action.setText("Bağlantı Yok")
            self.tray.setToolTip("ATK Neptune N9 - Bağlantı Yok")

    def show_message(self, title: str, message: str):
        # Notifications disabled per user request
        pass

    def cleanup(self):
        if self.tray:
            self.tray.hide()
            self.tray.setParent(None)

