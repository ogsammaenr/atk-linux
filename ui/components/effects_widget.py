"""
Nordic Precision Audio Effects & Spatial 7.1 Surround Polar Matrix for ATK Neptune N9.
Features technical polar coordinate visualizer, square channel nodes, and monospace voice changer grid.
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
    """Draws an engineering polar matrix 7.1 speaker diagram with crosshairs and square channel nodes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(130)
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

        # Background polar matrix grid
        axis_color = QColor("#282836")
        painter.setPen(QPen(axis_color, 1.0, Qt.PenStyle.SolidLine))
        painter.drawLine(int(cx - 75), int(cy), int(cx + 75), int(cy))
        painter.drawLine(int(cx), int(cy - 52), int(cx), int(cy + 52))

        ring_color = QColor("#FF5500" if self.active else "#22222E")
        painter.setPen(QPen(ring_color, 1.0, Qt.PenStyle.DashLine if not self.active else Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), 52, 45)
        painter.drawEllipse(QPointF(cx, cy), 32, 28)

        # Center Operator Node
        center_rect = QRectF(cx - 10, cy - 10, 20, 20)
        painter.setPen(QPen(QColor("#FF5500") if self.active else QColor("#3B3B4C"), 1.0))
        painter.setBrush(QBrush(QColor("#14141A")))
        painter.drawRect(center_rect)

        painter.setPen(QColor("#FFFFFF") if self.active else QColor("#7A7D8E"))
        painter.setFont(QFont("sans-serif", 8, QFont.Weight.Bold))
        painter.drawText(center_rect, Qt.AlignmentFlag.AlignCenter, "🎧")

        # 8 Channels (FL, C, FR, SL, SR, RL, RR, LFE)
        speakers = [
            ("FL", cx - 40, cy - 32),
            ("C",  cx,      cy - 44),
            ("FR", cx + 40, cy - 32),
            ("SL", cx - 56, cy),
            ("SR", cx + 56, cy),
            ("RL", cx - 38, cy + 32),
            ("RR", cx + 38, cy + 32),
            ("LFE", cx,     cy + 44),
        ]

        active_fill = QColor("#FF5500")
        inactive_fill = QColor("#1A1A24")

        font = QFont("JetBrains Mono", 7)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)

        for label, sx, sy in speakers:
            spk_rect = QRectF(sx - 10, sy - 7, 20, 14)
            if self.active:
                painter.setPen(QPen(QColor("#FFFFFF"), 1.0))
                painter.setBrush(QBrush(active_fill))
                painter.drawRect(spk_rect)
                painter.setPen(QColor("#000000"))
            else:
                painter.setPen(QPen(QColor("#2C2C3C"), 1.0))
                painter.setBrush(QBrush(inactive_fill))
                painter.drawRect(spk_rect)
                painter.setPen(QColor("#787B8E"))

            painter.drawText(spk_rect, Qt.AlignmentFlag.AlignCenter, label)


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
        main_layout.setSpacing(14)

        # 1. Section: 7.1 Virtual Surround
        surr_box = QFrame()
        surr_box.setProperty("class", "sub-card")
        surr_layout = QVBoxLayout(surr_box)
        surr_layout.setSpacing(12)

        top_row = QHBoxLayout()
        info_box = QVBoxLayout()
        self.stitle = QLabel(I18N.t("surround_title"))
        self.stitle.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.8px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.sdesc = QLabel(I18N.t("surround_desc"))
        self.sdesc.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        info_box.addWidget(self.stitle)
        info_box.addWidget(self.sdesc)
        top_row.addLayout(info_box)

        top_row.addStretch()

        sw_box = QHBoxLayout()
        sw_box.setSpacing(8)
        self.surr_status_lbl = QLabel(I18N.t("surround_off"))
        self.surr_status_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #626574; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
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
        self.vtitle.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.8px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.vdesc = QLabel(I18N.t("voice_changer_desc"))
        self.vdesc.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        vc_layout.addWidget(self.vtitle)
        vc_layout.addWidget(self.vdesc)

        effects_grid = QGridLayout()
        effects_grid.setSpacing(8)

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
        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if enabled:
            self.surr_status_lbl.setText(I18N.t("surround_on"))
            self.surr_status_lbl.setStyleSheet(mono_font + "font-size: 11px; font-weight: 800; color: #FF5500;")
        else:
            self.surr_status_lbl.setText(I18N.t("surround_off"))
            self.surr_status_lbl.setStyleSheet(mono_font + "font-size: 11px; font-weight: 600; color: #626574;")

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
