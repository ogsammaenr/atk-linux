"""
Modern 10-Band Parametric Equalizer Studio for ATK Neptune N9 with i18n support.
"""

from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFrame, QButtonGroup, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient, QFont

from atk_n9 import EQ_BANDS, PRESET_PROFILES
from ui.i18n import I18N


class EQCurveWidget(QWidget):
    """Draws a professional audio studio curve visualization with dB scale and grid lines."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(110)
        self.bands: List[int] = [0] * 10

    def set_bands(self, bands: List[int]):
        self.bands = list(bands)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())
        mid_y = h / 2.0

        bg_rect = QRectF(0, 0, w, h)
        painter.setPen(QPen(QColor("#1E202B"), 1))
        painter.setBrush(QBrush(QColor("#0E1015")))
        painter.drawRoundedRect(bg_rect, 10, 10)

        for db, y_pos in [("+20", 12.0), ("+10", (mid_y + 12.0) / 2.0), ("0", mid_y), ("-10", (mid_y + h - 12.0) / 2.0), ("-20", h - 12.0)]:
            is_zero = (db == "0")
            line_pen = QPen(QColor("#2C2F40") if is_zero else QColor("#1C1E28"), 1, Qt.PenStyle.DashLine if not is_zero else Qt.PenStyle.SolidLine)
            painter.setPen(line_pen)
            painter.drawLine(35, int(y_pos), int(w - 10), int(y_pos))

            painter.setPen(QColor("#52566C") if not is_zero else QColor("#00D2FF"))
            painter.setFont(QFont("sans-serif", 8, QFont.Weight.Bold if is_zero else QFont.Weight.Normal))
            painter.drawText(QRectF(4, y_pos - 7, 28, 14), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, db)

        if len(self.bands) != 10:
            return

        points = []
        plot_left = 40.0
        plot_width = w - 50.0
        step_x = plot_width / 9.0

        for i, val in enumerate(self.bands):
            x = plot_left + (i * step_x)
            norm = (val + 20.0) / 40.0
            y = (h - 14.0) - norm * (h - 28.0)
            points.append(QPointF(x, y))

        path = QPainterPath()
        path.moveTo(plot_left, mid_y)
        path.lineTo(points[0].x() * 0.7 + plot_left * 0.3, (mid_y + points[0].y()) * 0.5)

        for i in range(len(points) - 1):
            p0 = points[i]
            p1 = points[i + 1]
            c1 = QPointF((p0.x() + p1.x()) / 2.0, p0.y())
            c2 = QPointF((p0.x() + p1.x()) / 2.0, p1.y())
            path.cubicTo(c1, c2, p1)

        last_p = points[-1]
        path.lineTo(w - 10, (mid_y + last_p.y()) * 0.5)
        path.lineTo(w - 10, mid_y)

        fill_path = QPainterPath(path)
        fill_path.lineTo(w - 10, h - 10)
        fill_path.lineTo(plot_left, h - 10)
        fill_path.closeSubpath()

        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor(0, 210, 255, 75))
        grad.setColorAt(0.5, QColor(0, 210, 255, 25))
        grad.setColorAt(1.0, QColor(0, 210, 255, 0))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(fill_path)

        painter.setPen(QPen(QColor("#00D2FF"), 2.2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        for p in points:
            painter.setPen(QPen(QColor("#080A0E"), 1.8))
            painter.setBrush(QBrush(QColor("#00F5A0")))
            painter.drawEllipse(p, 4.0, 4.0)


class EQSliderCol(QWidget):
    """A vertical EQ band column with dynamic dB styling and frequency tag."""
    sig_changed = pyqtSignal(int, int)

    def __init__(self, index: int, freq_label: str, parent=None):
        super().__init__(parent)
        self.index = index
        self.freq_label = freq_label

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.val_lbl = QLabel("+0")
        self.val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_val_label(0)
        layout.addWidget(self.val_lbl)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(-20, 20)
        self.slider.setValue(0)
        self.slider.setFixedHeight(135)
        self.slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)

        self.freq_lbl = QLabel(freq_label)
        self.freq_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.freq_lbl.setStyleSheet("font-size: 11px; color: #7F8498; font-weight: 700;")
        layout.addWidget(self.freq_lbl)

    def _update_val_label(self, val: int):
        sign = "+" if val > 0 else ""
        self.val_lbl.setText(f"{sign}{val}")
        if val > 0:
            self.val_lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #00D2FF;")
        elif val < 0:
            self.val_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #FFB800;")
        else:
            self.val_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #8F94A6;")

    def _on_slider_changed(self, val: int):
        self._update_val_label(val)
        self.sig_changed.emit(self.index, val)

    def set_value_quietly(self, val: int):
        self.slider.blockSignals(True)
        self.slider.setValue(val)
        self._update_val_label(val)
        self.slider.blockSignals(False)


class EqualizerWidget(QFrame):
    """Main Studio Equalizer View."""
    sig_apply_bands = pyqtSignal(list)
    sig_apply_preset = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.current_bands: List[int] = [0] * 10

        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(70)
        self.debounce_timer.timeout.connect(self._emit_bands)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(14)

        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        self.title_lbl = QLabel(I18N.t("eq_title"))
        self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.6px;")
        self.subtitle_lbl = QLabel(I18N.t("eq_subtitle"))
        self.subtitle_lbl.setStyleSheet("font-size: 12px; color: #72768A;")
        title_box.addWidget(self.title_lbl)
        title_box.addWidget(self.subtitle_lbl)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        self.reset_btn = QPushButton(I18N.t("eq_reset_btn"))
        self.reset_btn.setProperty("class", "secondary-btn")
        self.reset_btn.clicked.connect(self.reset_flat)
        header_layout.addWidget(self.reset_btn)

        main_layout.addLayout(header_layout)

        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(8)
        self.preset_group = QButtonGroup(self)
        self.preset_group.setExclusive(True)

        presets = [
            ("🎚 Flat", "flat"),
            ("🎯 CS2", "cs2"),
            ("⚡ Valorant 1", "valorant1"),
            ("⚡ Valorant 2", "valorant2"),
            ("🪂 PUBG", "pubg"),
            ("🏹 Apex", "apex"),
            ("🎵 Pop", "pop"),
            ("🛡 Delta Force", "delta_force")
        ]

        for idx, (label, key) in enumerate(presets):
            btn = QPushButton(label)
            btn.setProperty("class", "preset-btn")
            btn.setCheckable(True)
            if key == "flat":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, k=key: self._on_preset_clicked(k))
            self.preset_group.addButton(btn, idx)
            preset_layout.addWidget(btn)

        preset_layout.addStretch()
        main_layout.addLayout(preset_layout)

        self.curve_canvas = EQCurveWidget()
        main_layout.addWidget(self.curve_canvas)

        sliders_box = QFrame()
        sliders_box.setStyleSheet("background-color: #0E1015; border: 1px solid #1E202B; border-radius: 12px; padding: 10px 14px;")
        sliders_layout = QHBoxLayout(sliders_box)
        sliders_layout.setContentsMargins(6, 6, 6, 6)
        sliders_layout.setSpacing(4)

        self.slider_cols: List[EQSliderCol] = []
        for i, freq in enumerate(EQ_BANDS):
            col = EQSliderCol(i, freq)
            col.sig_changed.connect(self._on_band_slider_moved)
            self.slider_cols.append(col)
            sliders_layout.addWidget(col)

        main_layout.addWidget(sliders_box)

        I18N.sig_language_changed.connect(lambda: self.retranslate())

    def retranslate(self):
        self.title_lbl.setText(I18N.t("eq_title"))
        self.subtitle_lbl.setText(I18N.t("eq_subtitle"))
        self.reset_btn.setText(I18N.t("eq_reset_btn"))

    def _on_band_slider_moved(self, index: int, val: int):
        self.current_bands[index] = val
        self.curve_canvas.set_bands(self.current_bands)
        checked_btn = self.preset_group.checkedButton()
        if checked_btn:
            self.preset_group.setExclusive(False)
            checked_btn.setChecked(False)
            self.preset_group.setExclusive(True)
        self.debounce_timer.start()

    def _emit_bands(self):
        self.sig_apply_bands.emit(list(self.current_bands))

    def _on_preset_clicked(self, preset_name: str):
        if preset_name in PRESET_PROFILES:
            new_bands = PRESET_PROFILES[preset_name]
            self.update_bands(new_bands)
            self.sig_apply_preset.emit(preset_name)

    def reset_flat(self):
        self._on_preset_clicked("flat")
        btn = self.preset_group.button(0)
        if btn:
            btn.setChecked(True)

    def update_bands(self, bands: List[int]):
        self.current_bands = list(bands)
        self.curve_canvas.set_bands(self.current_bands)
        for i, val in enumerate(bands):
            if i < len(self.slider_cols):
                self.slider_cols[i].set_value_quietly(val)
