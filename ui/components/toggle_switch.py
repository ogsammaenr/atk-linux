"""
Nordic Precision Industrial Mechanical Toggle Switch Widget for ATK Neptune N9.
Features sharp rectangular geometry, safety orange track, and tactile slide animation.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, checked: bool = False, parent=None, width=44, height=20):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = checked
        self._thumb_pos = (width - height + 2) if checked else 0.0

        # Animation for mechanical sliding
        self._anim = QPropertyAnimation(self, b"thumb_pos", self)
        self._anim.setDuration(120)

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
            target = (self.width() - self.height() + 2) if checked else 0.0
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

        # Industrial rectangular track with subtle 2px bevel
        track_rect = QRectF(0, 0, w, h)
        if self._checked:
            track_color = QColor("#FF5500")
            border_color = QColor("#FF6E24")
        else:
            track_color = QColor("#1A1A24")
            border_color = QColor("#2E2E3E")

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_rect, 2, 2)

        # Tactile rectangular thumb
        thumb_w = h - 6.0
        thumb_h = h - 6.0
        thumb_x = 3.0 + self._thumb_pos
        thumb_y = 3.0
        thumb_rect = QRectF(thumb_x, thumb_y, thumb_w, thumb_h)

        thumb_color = QColor("#FFFFFF") if self._checked else QColor("#7A7D8E")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(thumb_color))
        painter.drawRoundedRect(thumb_rect, 1, 1)
