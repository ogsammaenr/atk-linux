"""
Modern Microphone & Hardware Sidetone (Monitor) Controls for ATK Neptune N9 with i18n support.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from ui.components.toggle_switch import ToggleSwitch
from ui.i18n import I18N


class MicControlWidget(QFrame):
    sig_set_mic_mute = pyqtSignal(bool)
    sig_set_mic_volume = pyqtSignal(int)
    sig_set_sidetone = pyqtSignal(bool, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")

        self.is_muted = False
        self.mic_volume = 100
        self.sidetone_enabled = True
        self.sidetone_volume = 100

        self.mic_vol_timer = QTimer(self)
        self.mic_vol_timer.setSingleShot(True)
        self.mic_vol_timer.setInterval(80)
        self.mic_vol_timer.timeout.connect(lambda: self.sig_set_mic_volume.emit(self.mic_volume))

        self.sidetone_timer = QTimer(self)
        self.sidetone_timer.setSingleShot(True)
        self.sidetone_timer.setInterval(80)
        self.sidetone_timer.timeout.connect(lambda: self.sig_set_sidetone.emit(self.sidetone_enabled, self.sidetone_volume))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(16)

        # 1. Section: Mikrofon
        mic_box = QFrame()
        mic_box.setProperty("class", "sub-card")
        mic_layout = QVBoxLayout(mic_box)
        mic_layout.setSpacing(14)

        mic_header = QHBoxLayout()
        mic_title_box = QVBoxLayout()
        self.mic_title = QLabel(I18N.t("mic_settings_title"))
        self.mic_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFFFFF;")
        self.mic_desc = QLabel(I18N.t("mic_settings_desc"))
        self.mic_desc.setStyleSheet("font-size: 11px; color: #72768A;")
        mic_title_box.addWidget(self.mic_title)
        mic_title_box.addWidget(self.mic_desc)
        mic_header.addLayout(mic_title_box)

        mic_header.addStretch()

        mute_box = QHBoxLayout()
        mute_box.setSpacing(10)
        self.mute_status_lbl = QLabel(I18N.t("mic_unmuted_label"))
        self.mute_status_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00F5A0;")
        self.mute_switch = ToggleSwitch(checked=False)
        self.mute_switch.toggled.connect(self._on_mute_toggled)
        mute_box.addWidget(self.mute_status_lbl)
        mute_box.addWidget(self.mute_switch)
        mic_header.addLayout(mute_box)

        mic_layout.addLayout(mic_header)

        # Mic Volume Slider Row
        mic_slider_row = QHBoxLayout()
        mic_slider_row.setSpacing(12)
        self.mic_slider_lbl = QLabel(I18N.t("mic_input_level"))
        self.mic_slider_lbl.setStyleSheet("color: #9A9EA6; font-weight: 600; min-width: 90px;")
        mic_slider_row.addWidget(self.mic_slider_lbl)

        self.mic_slider = QSlider(Qt.Orientation.Horizontal)
        self.mic_slider.setRange(0, 100)
        self.mic_slider.setValue(100)
        self.mic_slider.valueChanged.connect(self._on_mic_slider_moved)
        mic_slider_row.addWidget(self.mic_slider)

        self.mic_val_lbl = QLabel("%100")
        self.mic_val_lbl.setFixedWidth(45)
        self.mic_val_lbl.setStyleSheet("color: #00D2FF; font-weight: 800;")
        mic_slider_row.addWidget(self.mic_val_lbl)

        mic_layout.addLayout(mic_slider_row)
        main_layout.addWidget(mic_box)

        # 2. Section: Sidetone (Yan Ton)
        side_box = QFrame()
        side_box.setProperty("class", "sub-card")
        side_layout = QVBoxLayout(side_box)
        side_layout.setSpacing(14)

        side_header = QHBoxLayout()
        side_title_box = QVBoxLayout()
        self.side_title = QLabel(I18N.t("sidetone_settings_title"))
        self.side_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #FFFFFF;")
        self.side_desc = QLabel(I18N.t("sidetone_settings_desc"))
        self.side_desc.setStyleSheet("font-size: 11px; color: #72768A;")
        side_title_box.addWidget(self.side_title)
        side_title_box.addWidget(self.side_desc)
        side_header.addLayout(side_title_box)

        side_header.addStretch()

        side_toggle_box = QHBoxLayout()
        side_toggle_box.setSpacing(10)
        self.side_status_lbl = QLabel(I18N.t("sidetone_active_label"))
        self.side_status_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00D2FF;")
        self.sidetone_switch = ToggleSwitch(checked=True)
        self.sidetone_switch.toggled.connect(self._on_sidetone_toggled)
        side_toggle_box.addWidget(self.side_status_lbl)
        side_toggle_box.addWidget(self.sidetone_switch)
        side_header.addLayout(side_toggle_box)

        side_layout.addLayout(side_header)

        # Sidetone Volume Slider Row
        side_slider_row = QHBoxLayout()
        side_slider_row.setSpacing(12)
        self.side_slider_lbl = QLabel(I18N.t("sidetone_level"))
        self.side_slider_lbl.setStyleSheet("color: #9A9EA6; font-weight: 600; min-width: 90px;")
        side_slider_row.addWidget(self.side_slider_lbl)

        self.sidetone_slider = QSlider(Qt.Orientation.Horizontal)
        self.sidetone_slider.setRange(0, 100)
        self.sidetone_slider.setValue(100)
        self.sidetone_slider.valueChanged.connect(self._on_sidetone_slider_moved)
        side_slider_row.addWidget(self.sidetone_slider)

        self.side_val_lbl = QLabel("%100")
        self.side_val_lbl.setFixedWidth(45)
        self.side_val_lbl.setStyleSheet("color: #00D2FF; font-weight: 800;")
        side_slider_row.addWidget(self.side_val_lbl)

        side_layout.addLayout(side_slider_row)
        main_layout.addWidget(side_box)

        main_layout.addStretch()

        I18N.sig_language_changed.connect(lambda: self.retranslate())

    def retranslate(self):
        self.mic_title.setText(I18N.t("mic_settings_title"))
        self.mic_desc.setText(I18N.t("mic_settings_desc"))
        self.mic_slider_lbl.setText(I18N.t("mic_input_level"))
        self._update_mute_style(self.is_muted)

        self.side_title.setText(I18N.t("sidetone_settings_title"))
        self.side_desc.setText(I18N.t("sidetone_settings_desc"))
        self.side_slider_lbl.setText(I18N.t("sidetone_level"))
        self._update_sidetone_style(self.sidetone_enabled)

    def _on_mute_toggled(self, checked: bool):
        self.is_muted = checked
        self._update_mute_style(checked)
        self.sig_set_mic_mute.emit(checked)

    def _update_mute_style(self, muted: bool):
        if muted:
            self.mute_status_lbl.setText(I18N.t("mic_muted_label"))
            self.mute_status_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #FF3366;")
        else:
            self.mute_status_lbl.setText(I18N.t("mic_unmuted_label"))
            self.mute_status_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00F5A0;")

    def _on_mic_slider_moved(self, val: int):
        self.mic_volume = val
        self.mic_val_lbl.setText(f"%{val}")
        self.mic_vol_timer.start()

    def _on_sidetone_toggled(self, checked: bool):
        self.sidetone_enabled = checked
        self._update_sidetone_style(checked)
        self.sidetone_slider.setEnabled(checked)
        self.sidetone_timer.start()

    def _update_sidetone_style(self, enabled: bool):
        if enabled:
            self.side_status_lbl.setText(I18N.t("sidetone_active_label"))
            self.side_status_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00D2FF;")
        else:
            self.side_status_lbl.setText(I18N.t("sidetone_inactive_label"))
            self.side_status_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #6E7284;")

    def _on_sidetone_slider_moved(self, val: int):
        self.sidetone_volume = val
        self.side_val_lbl.setText(f"%{val}")
        self.sidetone_timer.start()

    def update_state(self, mute: bool = None, volume: int = None, sidetone_en: bool = None, sidetone_vol: int = None):
        if mute is not None and mute != self.is_muted:
            self.is_muted = mute
            self.mute_switch.blockSignals(True)
            self.mute_switch.setChecked(mute)
            self._update_mute_style(mute)
            self.mute_switch.blockSignals(False)

        if volume is not None and volume != self.mic_volume:
            self.mic_volume = volume
            self.mic_slider.blockSignals(True)
            self.mic_slider.setValue(volume)
            self.mic_val_lbl.setText(f"%{volume}")
            self.mic_slider.blockSignals(False)

        if sidetone_en is not None and sidetone_en != self.sidetone_enabled:
            self.sidetone_enabled = sidetone_en
            self.sidetone_switch.blockSignals(True)
            self.sidetone_switch.setChecked(sidetone_en)
            self._update_sidetone_style(sidetone_en)
            self.sidetone_slider.setEnabled(sidetone_en)
            self.sidetone_switch.blockSignals(False)

        if sidetone_vol is not None and sidetone_vol != self.sidetone_volume:
            self.sidetone_volume = sidetone_vol
            self.sidetone_slider.blockSignals(True)
            self.sidetone_slider.setValue(sidetone_vol)
            self.side_val_lbl.setText(f"%{sidetone_vol}")
            self.sidetone_slider.blockSignals(False)
