"""
Nordic Precision Industrial Battery & Telemetry Widget for ATK Neptune N9.
Displays discrete stepped segment levels, technical status indicators, and monospace readouts.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from ui.i18n import I18N


class BatteryIconWidget(QWidget):
    """Draws an industrial 5-segment discrete battery gauge."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(54, 18)
        self.level = 0
        self.charging = False
        self.connected = False

    def update_state(self, level: int, charging: bool, connected: bool):
        self.level = max(0, min(100, level))
        self.charging = charging
        self.connected = connected
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Body & Cap
        body_rect = QRectF(1.0, 1.0, 46.0, 16.0)
        cap_rect = QRectF(48.0, 5.0, 3.0, 8.0)

        border_color = QColor("#38384A") if self.connected else QColor("#282834")
        painter.setPen(QPen(border_color, 1.0))
        painter.setBrush(QBrush(QColor("#14141A")))
        painter.drawRoundedRect(body_rect, 1.5, 1.5)
        painter.drawRoundedRect(cap_rect, 1.0, 1.0)

        if not self.connected:
            return

        # Discrete 5 segments
        # 1-20%: 1, 21-40%: 2, 41-60%: 3, 61-80%: 4, 81-100%: 5
        num_active = max(1 if self.level > 0 else 0, min(5, (self.level + 19) // 20))

        if self.charging:
            active_color = QColor("#FF5500")
        elif self.level > 35:
            active_color = QColor("#FFFFFF")
        elif self.level > 15:
            active_color = QColor("#FF5500")
        else:
            active_color = QColor("#FF3344")

        seg_width = 7.0
        seg_height = 10.0
        seg_y = 4.0

        for i in range(5):
            seg_x = 4.0 + (i * 8.2)
            seg_rect = QRectF(seg_x, seg_y, seg_width, seg_height)
            if i < num_active:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(active_color))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#20202A")))
            painter.drawRoundedRect(seg_rect, 1.0, 1.0)


class BatteryStatusWidget(QFrame):
    """Header status bar component with Industrial Connection Status and Monospace Telemetry."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.connected = False
        self.level = 0
        self.charging = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.latency_lbl = QLabel("RF: 2.4G_OK | 1000Hz")
        self.latency_lbl.setProperty("class", "badge-latency")
        layout.addWidget(self.latency_lbl)

        self.badge_lbl = QLabel(I18N.t("searching_device"))
        self.badge_lbl.setProperty("class", "badge-disconnected")
        layout.addWidget(self.badge_lbl)

        self.icon_widget = BatteryIconWidget()
        layout.addWidget(self.icon_widget)

        self.text_lbl = QLabel("--%")
        self.text_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #FFFFFF; min-width: 44px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        layout.addWidget(self.text_lbl)

        I18N.sig_language_changed.connect(lambda: self.retranslate())

    def set_status(self, connected: bool, level: int = 0, charging: bool = False):
        self.connected = connected
        self.level = level
        self.charging = charging
        self.icon_widget.update_state(level, charging, connected)
        self.retranslate()

    def retranslate(self):
        if self.connected:
            self.badge_lbl.setText(I18N.t("connected_badge"))
            self.badge_lbl.setProperty("class", "badge-connected")
            self.badge_lbl.setStyleSheet(
                "background-color: #1A1A24; color: #00F5A0; "
                "border: 1px solid #282838; border-radius: 2px; "
                "padding: 3px 8px; font-size: 10px; font-weight: 700; "
                "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
            )
            self.latency_lbl.show()
            chg_str = I18N.t("charging_tag") if self.charging else ""
            self.text_lbl.setText(f"{self.level}%{chg_str}")
        else:
            self.badge_lbl.setText(I18N.t("disconnected_badge"))
            self.badge_lbl.setProperty("class", "badge-disconnected")
            self.badge_lbl.setStyleSheet(
                "background-color: #1A1A24; color: #FF4B5C; "
                "border: 1px solid #282838; border-radius: 2px; "
                "padding: 3px 8px; font-size: 10px; font-weight: 700; "
                "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
            )
            self.latency_lbl.hide()
            self.text_lbl.setText("--%")
