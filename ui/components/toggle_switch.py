"""
Modern Animated Toggle Switch Widget for ATK Neptune N9.
Mimics modern iOS / macOS / Gaming Software (G-Hub, Sonar) sliding pill switches.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, checked: bool = False, parent=None, width=46, height=24):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = checked
        self._thumb_pos = (height - 4) if checked else 0.0

        # Animation for smooth sliding
        self._anim = QPropertyAnimation(self, b"thumb_pos", self)
        self._anim.setDuration(160)

    @pyqtProperty(float)
    def thumb_pos(self):
        return self._thumb_pos

    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        if self._checked != checked:
            self._checked = checked
            target = (self.width() - self.height()) if checked else 0.0
            self._anim.stop()
            self._anim.setStartValue(self._thumb_pos)
            self._anim.setEndValue(target)
            self._anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._checked)
            self.toggled.emit(self._checked)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())
        radius = h / 2.0

        # Background track
        track_rect = QRectF(0, 0, w, h)
        if self._checked:
            track_color = QColor("#00D2FF") # Vibrant Cyan when Active
            border_color = QColor("#33DBFF")
        else:
            track_color = QColor("#222530") # Deep charcoal when Inactive
            border_color = QColor("#313646")

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_rect, radius, radius)

        # Sliding circular thumb
        thumb_size = h - 6.0
        thumb_x = 3.0 + self._thumb_pos
        thumb_y = 3.0
        thumb_rect = QRectF(thumb_x, thumb_y, thumb_size, thumb_size)

        thumb_color = QColor("#0E1015") if self._checked else QColor("#A0A5B8")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(thumb_rect)
