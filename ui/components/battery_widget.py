"""
Ultra-Modern Battery and Connection Indicator Badge for ATK Neptune N9 with i18n.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient

from ui.i18n import I18N


class BatteryIconWidget(QWidget):
    """Draws a high-precision, sleek battery pill with glowing level fill and charging bolt."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 22)
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

        body_rect = QRectF(1.5, 3.5, 38, 15)
        cap_rect = QRectF(40.5, 7.5, 2.5, 7)

        border_color = QColor("#313444") if not self.connected else QColor("#454A5E")
        painter.setPen(QPen(border_color, 1.2))
        painter.setBrush(QBrush(QColor("#14151E")))
        painter.drawRoundedRect(body_rect, 4, 4)
        painter.drawRoundedRect(cap_rect, 1.5, 1.5)

        if not self.connected:
            return

        if self.charging:
            c1, c2 = QColor("#00E5FF"), QColor("#0099FF")
        elif self.level > 35:
            c1, c2 = QColor("#00F5A0"), QColor("#00C875")
        elif self.level > 15:
            c1, c2 = QColor("#FFB800"), QColor("#FF8C00")
        else:
            c1, c2 = QColor("#FF3366"), QColor("#D60036")

        avail_width = body_rect.width() - 4.0
        fill_width = max(0.0, avail_width * (self.level / 100.0))
        if fill_width > 0:
            fill_rect = QRectF(3.5, 5.5, fill_width, 11)
            grad = QLinearGradient(fill_rect.topLeft(), fill_rect.bottomRight())
            grad.setColorAt(0.0, c1)
            grad.setColorAt(1.0, c2)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(grad))
            painter.drawRoundedRect(fill_rect, 2.5, 2.5)

        if self.charging:
            painter.setPen(QPen(QColor("#0E1015"), 1.2))
            painter.setFont(QFont("sans-serif", 9, QFont.Weight.Bold))
            painter.drawText(QRectF(11, 2, 16, 16), Qt.AlignmentFlag.AlignCenter, "⚡")


class BatteryStatusWidget(QFrame):
    """Header status bar component with Connection Status, Low Latency Tag, and Battery Info."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.connected = False
        self.level = 0
        self.charging = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.latency_lbl = QLabel("1000Hz • 2.4G")
        self.latency_lbl.setProperty("class", "badge-latency")
        layout.addWidget(self.latency_lbl)

        self.badge_lbl = QLabel(I18N.t("searching_device"))
        self.badge_lbl.setProperty("class", "badge-disconnected")
        layout.addWidget(self.badge_lbl)

        self.icon_widget = BatteryIconWidget()
        layout.addWidget(self.icon_widget)

        self.text_lbl = QLabel("--%")
        self.text_lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFFFFF; min-width: 38px;")
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
                "background-color: rgba(0, 245, 160, 0.12); color: #00F5A0; "
                "border: 1px solid rgba(0, 245, 160, 0.35); border-radius: 12px; "
                "padding: 4px 12px; font-size: 11px; font-weight: 700;"
            )
            self.latency_lbl.show()
            chg_str = I18N.t("charging_tag") if self.charging else ""
            self.text_lbl.setText(f"%{self.level}{chg_str}")
        else:
            self.badge_lbl.setText(I18N.t("disconnected_badge"))
            self.badge_lbl.setProperty("class", "badge-disconnected")
            self.badge_lbl.setStyleSheet(
                "background-color: rgba(255, 51, 102, 0.12); color: #FF3366; "
                "border: 1px solid rgba(255, 51, 102, 0.35); border-radius: 12px; "
                "padding: 4px 12px; font-size: 11px; font-weight: 700;"
            )
            self.latency_lbl.hide()
            self.text_lbl.setText("--%")
