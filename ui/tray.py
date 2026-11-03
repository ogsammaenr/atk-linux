"""
System Tray Manager for ATK Neptune N9 Linux Driver.
Features Nordic Precision industrial square icon and monochrome/orange telemetry.
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from ui.i18n import I18N


def create_tray_pixmap(level: int = 100, connected: bool = True) -> QPixmap:
    """Generates an industrial square icon with level and status."""
    pix = QPixmap(32, 32)
    pix.fill(QColor(0, 0, 0, 0))

    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Base square indicator
    bg_color = QColor("#14141A")
    painter.setBrush(bg_color)
    painter.setPen(QColor("#2C2C3C"))
    painter.drawRoundedRect(2, 2, 28, 28, 2, 2)

    if not connected:
        painter.setPen(QColor("#FF4B5C"))
        font = QFont("JetBrains Mono", 10, QFont.Weight.Bold)
        font.setStyleHint(QFont.StyleHint.Monospace)
        painter.setFont(font)
        painter.drawText(pix.rect(), 0x0084, "✕")
        painter.end()
        return pix

    # Color by level
    if level > 35:
        c = QColor("#FFFFFF")
    elif level > 15:
        c = QColor("#FF5500")
    else:
        c = QColor("#FF3344")

    # Top-right indicator
    painter.setBrush(c)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRect(20, 4, 7, 7)

    # Monospace percentage / N9
    painter.setPen(QColor("#FFFFFF"))
    font = QFont("JetBrains Mono", 8, QFont.Weight.Bold)
    font.setStyleHint(QFont.StyleHint.Monospace)
    painter.setFont(font)
    txt = f"{level}" if level < 100 else "N9"
    painter.drawText(2, 7, 26, 20, 0x0084, txt)
    painter.end()
    return pix


class TrayManager(QObject):
    sig_show_window = pyqtSignal()
    sig_toggle_sidetone = pyqtSignal()
    sig_quit_app = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_connected = False
        self._last_battery = 0
        self._last_charging = False

        self.tray = QSystemTrayIcon(parent)
        self.tray.setIcon(QIcon(create_tray_pixmap(90, True)))
        self.tray.setToolTip(I18N.t("app_title"))

        # Build context menu with Nordic styling
        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #16161D;
                color: #FFFFFF;
                border: 1px solid #2A2A38;
                border-radius: 2px;
                padding: 4px;
                font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
                font-size: 11px;
            }
            QMenu::item {
                padding: 6px 16px;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: #FF5500;
                color: #000000;
                font-weight: 700;
            }
            QMenu::separator {
                height: 1px;
                background-color: #282834;
                margin: 4px 4px;
            }
        """)

        self.title_action = self.menu.addAction(I18N.t("tray_title"))
        self.title_action.setEnabled(False)

        self.battery_action = self.menu.addAction(f"{I18N.t('tray_battery')}--%")
        self.battery_action.setEnabled(False)

        self.menu.addSeparator()

        self.sidetone_action = self.menu.addAction(I18N.t("tray_toggle_sidetone"))
        self.sidetone_action.triggered.connect(self.sig_toggle_sidetone.emit)

        self.menu.addSeparator()

        self.show_action = self.menu.addAction(I18N.t("tray_show_window"))
        self.show_action.triggered.connect(self.sig_show_window.emit)

        self.quit_action = self.menu.addAction(I18N.t("tray_quit"))
        self.quit_action.triggered.connect(self.sig_quit_app.emit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        I18N.sig_language_changed.connect(self.retranslate)

    def retranslate(self, lang=None):
        self.title_action.setText(I18N.t("tray_title"))
        self.sidetone_action.setText(I18N.t("tray_toggle_sidetone"))
        self.show_action.setText(I18N.t("tray_show_window"))
        self.quit_action.setText(I18N.t("tray_quit"))
        self.update_status(self._last_connected, self._last_battery, self._last_charging)

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.sig_show_window.emit()

    def update_status(self, connected: bool, battery: int = 0, charging: bool = False):
        self._last_connected = connected
        self._last_battery = battery
        self._last_charging = charging
        self.tray.setIcon(QIcon(create_tray_pixmap(battery, connected)))
        if connected:
            chg = I18N.t("charging_tag") if charging else ""
            self.battery_action.setText(f"{I18N.t('tray_battery')}{battery}%{chg}")
            self.tray.setToolTip(f"ATK Neptune N9 - {battery}%{chg}")
        else:
            self.battery_action.setText(I18N.t("tray_disconnected"))
            self.tray.setToolTip(f"ATK Neptune N9 - {I18N.t('tray_disconnected')}")

    def show_message(self, title: str, message: str):
        pass

    def cleanup(self):
        if self.tray:
            self.tray.hide()
