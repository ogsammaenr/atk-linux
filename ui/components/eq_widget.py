"""
Nordic Precision 10-Band Parametric DSP Equalizer for ATK Neptune N9.
Features technical gridlines, stepped response polyline, square node markers,
and monospace frequency readouts.
"""

from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFrame, QButtonGroup, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont

from atk_n9 import EQ_BANDS, PRESET_PROFILES
from ui.i18n import I18N


class EQCurveWidget(QWidget):
    """Draws a high-precision engineering DSP response grid with stepped polyline and square nodes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(115)
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

        # Background canvas - flat carbon with sharp border
        bg_rect = QRectF(0, 0, w, h)
        painter.setPen(QPen(QColor("#262634"), 1))
        painter.setBrush(QBrush(QColor("#111114")))
        painter.drawRoundedRect(bg_rect, 2, 2)

        # Technical Grid lines & dB labels
        grid_specs = [
            ("+20", 12.0),
            ("+10", (mid_y + 12.0) / 2.0),
            ("0", mid_y),
            ("-10", (mid_y + h - 12.0) / 2.0),
            ("-20", h - 12.0)
        ]

        font = QFont("JetBrains Mono", 8)
        font.setStyleHint(QFont.StyleHint.Monospace)
        painter.setFont(font)

        for db, y_pos in grid_specs:
            is_zero = (db == "0")
            line_pen = QPen(
                QColor("#3A3A4C") if is_zero else QColor("#1C1C24"),
                1,
                Qt.PenStyle.SolidLine if is_zero else Qt.PenStyle.DashLine
            )
            painter.setPen(line_pen)
            painter.drawLine(42, int(y_pos), int(w - 12), int(y_pos))

            painter.setPen(QColor("#FFFFFF") if is_zero else QColor("#666675"))
            label_text = "0.0 dB" if is_zero else f"{db} dB"
            painter.drawText(QRectF(2, y_pos - 7, 36, 14), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, label_text)

        if len(self.bands) != 10:
            return

        points = []
        plot_left = 50.0
        plot_width = w - 64.0
        step_x = plot_width / 9.0

        for i, val in enumerate(self.bands):
            x = plot_left + (i * step_x)
            norm = (val + 20.0) / 40.0
            y = (h - 14.0) - norm * (h - 28.0)
            points.append(QPointF(x, y))

        # Precision Stepped Polyline Curve
        poly_path = QPainterPath()
        poly_path.moveTo(plot_left, points[0].y())
        for i in range(1, len(points)):
            poly_path.lineTo(points[i].x(), points[i].y())

        # Area under curve - technical hatched / subtle tint
        fill_path = QPainterPath(poly_path)
        fill_path.lineTo(points[-1].x(), mid_y)
        fill_path.lineTo(plot_left, mid_y)
        fill_path.closeSubpath()

        painter.setBrush(QBrush(QColor(255, 85, 0, 24)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(fill_path)

        # Crisp Safety Orange response line
        painter.setPen(QPen(QColor("#FF5500"), 2.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(poly_path)

        # Square Technical Node Markers
        for i, p in enumerate(points):
            val = self.bands[i]
            node_rect = QRectF(p.x() - 3.5, p.y() - 3.5, 7.0, 7.0)
            if val != 0:
                painter.setPen(QPen(QColor("#FFFFFF"), 1.0))
                painter.setBrush(QBrush(QColor("#FF5500")))
            else:
                painter.setPen(QPen(QColor("#777785"), 1.0))
                painter.setBrush(QBrush(QColor("#111114")))
            painter.drawRect(node_rect)


class EQSliderCol(QWidget):
    """A vertical EQ band column with dynamic monospace dB styling and frequency tag."""
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
        self.freq_lbl.setStyleSheet(
            "font-size: 10px; color: #8A8D9C; font-weight: 700; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        layout.addWidget(self.freq_lbl)

    def _update_val_label(self, val: int):
        sign = "+" if val > 0 else ""
        self.val_lbl.setText(f"{sign}{val}")
        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if val > 0:
            self.val_lbl.setStyleSheet(mono_font + "font-size: 10px; font-weight: 800; color: #FF5500;")
        elif val < 0:
            self.val_lbl.setStyleSheet(mono_font + "font-size: 10px; font-weight: 700; color: #FFFFFF;")
        else:
            self.val_lbl.setStyleSheet(mono_font + "font-size: 10px; font-weight: 600; color: #6C6F7E;")

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
        self.title_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 900; color: #FFFFFF; letter-spacing: 1px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.subtitle_lbl = QLabel(I18N.t("eq_subtitle"))
        self.subtitle_lbl.setStyleSheet("font-size: 11px; color: #7D7F8E;")
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
        preset_layout.setSpacing(6)
        self.preset_group = QButtonGroup(self)
        self.preset_group.setExclusive(True)

        presets = [
            ("[DEFAULT_FLAT]", "flat"),
            ("[FPS_CS2]", "cs2"),
            ("[VALORANT_1]", "valorant1"),
            ("[VALORANT_2]", "valorant2"),
            ("[PUBG_COMBAT]", "pubg"),
            ("[APEX_LEGENDS]", "apex"),
            ("[POP_ACOUSTIC]", "pop"),
            ("[DELTA_FORCE]", "delta_force")
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
        sliders_box.setStyleSheet("background-color: #141419; border: 1px solid #242430; border-radius: 2px; padding: 10px 14px;")
        sliders_layout = QHBoxLayout(sliders_box)
        sliders_layout.setContentsMargins(4, 4, 4, 4)
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
