"""
Modern Audio Effects & Spatial 7.1 Surround Visualizer for ATK Neptune N9 with i18n support.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QButtonGroup, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from ui.components.toggle_switch import ToggleSwitch
from ui.i18n import I18N


class SurroundSpeakerVisualizer(QWidget):
    """Draws a spatial 7.1 speaker diagram. Speakers glow when virtual surround is active."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.active = False

    def set_active(self, active: bool):
        self.active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())
        cx = w / 2.0
        cy = h / 2.0

        radius = 46.0
        wave_color = QColor(0, 210, 255, 40) if self.active else QColor(40, 44, 58, 40)
        painter.setPen(QPen(wave_color, 1.2, Qt.PenStyle.DashLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), radius + 8, radius + 8)

        painter.setPen(QPen(QColor("#00D2FF") if self.active else QColor("#5A5E72"), 1.5))
        painter.setBrush(QBrush(QColor("#181924")))
        painter.drawEllipse(QPointF(cx, cy), 14, 14)

        painter.setPen(QColor("#FFFFFF") if self.active else QColor("#8E92A4"))
        painter.setFont(QFont("sans-serif", 8, QFont.Weight.Bold))
        painter.drawText(QRectF(cx - 14, cy - 14, 28, 28), Qt.AlignmentFlag.AlignCenter, "🎧")

        speakers = [
            ("FL", cx - 36, cy - 30),
            ("C",  cx,      cy - 40),
            ("FR", cx + 36, cy - 30),
            ("SL", cx - 44, cy),
            ("SR", cx + 44, cy),
            ("RL", cx - 32, cy + 30),
            ("RR", cx + 32, cy + 30),
        ]

        active_fill = QColor("#00D2FF")
        inactive_fill = QColor("#222533")

        for label, sx, sy in speakers:
            painter.setPen(QPen(QColor("#00D2FF") if self.active else QColor("#313648"), 1))
            painter.setBrush(QBrush(active_fill if self.active else inactive_fill))
            painter.drawRoundedRect(QRectF(sx - 9, sy - 7, 18, 14), 3, 3)

            painter.setPen(QColor("#080A0E") if self.active else QColor("#6B7084"))
            painter.setFont(QFont("sans-serif", 6, QFont.Weight.Bold))
            painter.drawText(QRectF(sx - 9, sy - 7, 18, 14), Qt.AlignmentFlag.AlignCenter, label)


class EffectsWidget(QFrame):
    sig_set_surround = pyqtSignal(bool)
    sig_set_effect = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")

        self.surround_enabled = False
        self.active_effect_id = -1

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(16)

        # 1. Section: 7.1 Virtual Surround
        surr_box = QFrame()
        surr_box.setProperty("class", "sub-card")
        surr_layout = QVBoxLayout(surr_box)
        surr_layout.setSpacing(12)

        top_row = QHBoxLayout()
        info_box = QVBoxLayout()
        self.stitle = QLabel(I18N.t("surround_title"))
        self.stitle.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFFFFF;")
        self.sdesc = QLabel(I18N.t("surround_desc"))
        self.sdesc.setStyleSheet("font-size: 11px; color: #72768A;")
        info_box.addWidget(self.stitle)
        info_box.addWidget(self.sdesc)
        top_row.addLayout(info_box)

        top_row.addStretch()

        sw_box = QHBoxLayout()
        sw_box.setSpacing(10)
        self.surr_status_lbl = QLabel(I18N.t("surround_off"))
        self.surr_status_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #6E7284;")
        self.surr_switch = ToggleSwitch(checked=False)
        self.surr_switch.toggled.connect(self._on_surr_toggled)
        sw_box.addWidget(self.surr_status_lbl)
        sw_box.addWidget(self.surr_switch)
        top_row.addLayout(sw_box)

        surr_layout.addLayout(top_row)

        self.speaker_viz = SurroundSpeakerVisualizer()
        surr_layout.addWidget(self.speaker_viz)

        main_layout.addWidget(surr_box)

        # 2. Section: Ses Değiştirici
        vc_box = QFrame()
        vc_box.setProperty("class", "sub-card")
        vc_layout = QVBoxLayout(vc_box)
        vc_layout.setSpacing(12)

        self.vtitle = QLabel(I18N.t("voice_changer_title"))
        self.vtitle.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFFFFF;")
        self.vdesc = QLabel(I18N.t("voice_changer_desc"))
        self.vdesc.setStyleSheet("font-size: 11px; color: #72768A;")
        vc_layout.addWidget(self.vtitle)
        vc_layout.addWidget(self.vdesc)

        effects_grid = QGridLayout()
        effects_grid.setSpacing(10)

        self.effect_group = QButtonGroup(self)
        self.effect_group.setExclusive(True)

        effects = [
            ("vc_normal", -1, 0, 0),
            ("vc_male", 0, 0, 1),
            ("vc_female", 1, 0, 2),
            ("vc_monster", 2, 1, 0),
            ("vc_cartoon", 3, 1, 1),
        ]

        self.effect_buttons = {}
        for key, eff_id, row, col in effects:
            btn = QPushButton(I18N.t(key))
            btn.setProperty("class", "preset-btn")
            btn.setProperty("i18n_key", key)
            btn.setCheckable(True)
            if eff_id == -1:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=eff_id: self._on_effect_clicked(i))
            self.effect_group.addButton(btn)
            effects_grid.addWidget(btn, row, col)
            self.effect_buttons[eff_id] = btn

        vc_layout.addLayout(effects_grid)
        main_layout.addWidget(vc_box)

        main_layout.addStretch()

        I18N.sig_language_changed.connect(lambda: self.retranslate())

    def retranslate(self):
        self.stitle.setText(I18N.t("surround_title"))
        self.sdesc.setText(I18N.t("surround_desc"))
        self._update_surr_style(self.surround_enabled)

        self.vtitle.setText(I18N.t("voice_changer_title"))
        self.vdesc.setText(I18N.t("voice_changer_desc"))

        for eff_id, btn in self.effect_buttons.items():
            key = btn.property("i18n_key")
            if key:
                btn.setText(I18N.t(key))

    def _on_surr_toggled(self, checked: bool):
        self.surround_enabled = checked
        self._update_surr_style(checked)
        self.sig_set_surround.emit(checked)

    def _update_surr_style(self, enabled: bool):
        self.speaker_viz.set_active(enabled)
        if enabled:
            self.surr_status_lbl.setText(I18N.t("surround_on"))
            self.surr_status_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #00D2FF;")
        else:
            self.surr_status_lbl.setText(I18N.t("surround_off"))
            self.surr_status_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #6E7284;")

    def _on_effect_clicked(self, eff_id: int):
        self.active_effect_id = eff_id
        self.sig_set_effect.emit(eff_id)

    def update_state(self, surround_en: bool = None, effect_en: bool = None, effect_id: int = None):
        if surround_en is not None and surround_en != self.surround_enabled:
            self.surround_enabled = surround_en
            self.surr_switch.blockSignals(True)
            self.surr_switch.setChecked(surround_en)
            self._update_surr_style(surround_en)
            self.surr_switch.blockSignals(False)

        if effect_en is False:
            self.active_effect_id = -1
            btn = self.effect_buttons.get(-1)
            if btn:
                btn.blockSignals(True)
                btn.setChecked(True)
                btn.blockSignals(False)
        elif effect_id is not None and effect_en is True:
            self.active_effect_id = effect_id
            btn = self.effect_buttons.get(effect_id)
            if btn:
                btn.blockSignals(True)
                btn.setChecked(True)
                btn.blockSignals(False)
