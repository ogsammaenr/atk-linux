"""
Nordic Precision Linux Control Center Main Window for ATK Neptune N9 with i18n Support.
Inspired by Teenage Engineering (TX-6 / OP-1) and Wooting (Wootility v5).
"""

import sys
import json
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget, QButtonGroup, QCheckBox,
    QApplication, QGridLayout, QComboBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QCloseEvent

from ui.styles import MAIN_STYLESHEET
from ui.worker import N9Worker
from ui.tray import TrayManager
from ui.components.toggle_switch import ToggleSwitch
from ui.components.battery_widget import BatteryStatusWidget
from ui.components.eq_widget import EqualizerWidget
from ui.components.mic_widget import MicControlWidget
from ui.components.effects_widget import EffectsWidget
from ui.i18n import I18N
from ui.config import CONFIG, is_autostart_enabled, set_autostart


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(I18N.t("app_title"))
        self.resize(960, 640)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(MAIN_STYLESHEET)

        self.minimize_to_tray = bool(CONFIG.get("minimize_to_tray", True))
        self._is_quitting = False
        self._is_port_open = False
        self._is_rf_connected = False
        self._last_port_msg = ""
        self._last_mute = False
        self._last_sidetone = True
        self._last_surround = False

        # 1. Initialize Worker Thread
        self.worker = N9Worker()

        # 2. Setup Central Widget and Main Layout
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 3. Header Top Bar
        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(50)
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(20, 0, 20, 0)

        # Brand / Logo (Nordic Industrial Header)
        brand_box = QHBoxLayout()
        brand_box.setSpacing(10)

        self.brand_badge = QLabel("N9")
        self.brand_badge.setStyleSheet(
            "background-color: #FF5500; color: #000000; font-size: 11px; font-weight: 900; "
            "border-radius: 2px; padding: 2px 6px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )

        self.brand_title = QLabel(I18N.t("app_brand"))
        self.brand_title.setStyleSheet(
            "font-size: 13px; font-weight: 800; letter-spacing: 1.5px; color: #FFFFFF; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )

        self.brand_sub = QLabel(I18N.t("version_tag"))
        self.brand_sub.setStyleSheet(
            "font-size: 10px; font-weight: 700; color: #727485; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )

        brand_box.addWidget(self.brand_badge)
        brand_box.addWidget(self.brand_title)
        brand_box.addWidget(self.brand_sub)
        topbar_layout.addLayout(brand_box)

        topbar_layout.addStretch()

        # Top Battery & Status Widget
        self.battery_widget = BatteryStatusWidget()
        topbar_layout.addWidget(self.battery_widget)

        root_layout.addWidget(topbar)

        # 4. Body Area: Sidebar + Stacked Content Pages
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # 4.1. Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(215)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 14, 12, 14)
        sidebar_layout.setSpacing(4)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        nav_items = [
            ("nav_dashboard", 0),
            ("nav_eq", 1),
            ("nav_mic", 2),
            ("nav_effects", 3),
            ("nav_settings", 4)
        ]

        self.nav_buttons = []
        for key, idx in nav_items:
            btn = QPushButton(I18N.t(key))
            btn.setProperty("class", "nav-btn")
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=idx: self.pages_stack.setCurrentIndex(i))
            self.nav_group.addButton(btn, idx)
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append((btn, key))

        sidebar_layout.addStretch()

        # Technical Spec Card Bottom Sidebar
        spec_card = QFrame()
        spec_card.setStyleSheet(
            "background-color: #16161B; border: 1px solid #242430; border-radius: 2px; padding: 6px 8px;"
        )
        sc_layout = QVBoxLayout(spec_card)
        sc_layout.setSpacing(2)
        sc_layout.setContentsMargins(4, 4, 4, 4)

        self.spec_l1 = QLabel("DEVICE: ATK_N9_ULTRA")
        self.spec_l1.setStyleSheet("color: #FFFFFF; font-size: 9px; font-weight: 800; font-family: 'JetBrains Mono', monospace;")
        self.spec_l2 = QLabel("ENDPOINT: /dev/ttyACM0")
        self.spec_l2.setStyleSheet("color: #727485; font-size: 9px; font-family: 'JetBrains Mono', monospace;")
        self.spec_l3 = QLabel("DSP: 10-BAND PARAMETRIC")
        self.spec_l3.setStyleSheet("color: #727485; font-size: 9px; font-family: 'JetBrains Mono', monospace;")
        self.spec_l4 = QLabel("[STATUS: SYNCED]")
        self.spec_l4.setStyleSheet("color: #FF5500; font-size: 9px; font-weight: 800; font-family: 'JetBrains Mono', monospace;")

        sc_layout.addWidget(self.spec_l1)
        sc_layout.addWidget(self.spec_l2)
        sc_layout.addWidget(self.spec_l3)
        sc_layout.addWidget(self.spec_l4)
        sidebar_layout.addWidget(spec_card)

        body_layout.addWidget(sidebar)

        # 4.2. Stacked Content Pages
        self.pages_stack = QStackedWidget()
        self.pages_stack.setContentsMargins(16, 14, 16, 14)

        # Page 0: Dashboard
        self.page_dashboard = self._build_dashboard_page()
        self.pages_stack.addWidget(self.page_dashboard)

        # Page 1: Equalizer Widget
        self.eq_widget = EqualizerWidget()
        self.pages_stack.addWidget(self.eq_widget)

        # Page 2: Microphone & Sidetone Widget
        self.mic_widget = MicControlWidget()
        self.pages_stack.addWidget(self.mic_widget)

        # Page 3: Effects & Surround Widget
        self.effects_widget = EffectsWidget()
        self.pages_stack.addWidget(self.effects_widget)

        # Page 4: Info & Settings
        self.page_info = self._build_info_page()
        self.pages_stack.addWidget(self.page_info)
        self.pages_stack.currentChanged.connect(self._on_page_changed)

        body_layout.addWidget(self.pages_stack)
        root_layout.addWidget(body_widget)

        # 5. Bottom Status Bar
        statusbar = QFrame()
        statusbar.setObjectName("statusbar")
        statusbar.setFixedHeight(26)
        statusbar_layout = QHBoxLayout(statusbar)
        statusbar_layout.setContentsMargins(16, 0, 16, 0)

        self.status_port_lbl = QLabel(I18N.t("status_searching"))
        self.status_port_lbl.setStyleSheet(
            "color: #727485; font-size: 10px; font-weight: 600; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        statusbar_layout.addWidget(self.status_port_lbl)

        statusbar_layout.addStretch()

        self.status_link_lbl = QLabel(I18N.t("status_link_active"))
        self.status_link_lbl.setStyleSheet(
            "color: #00F5A0; font-size: 10px; font-weight: 700; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        statusbar_layout.addWidget(self.status_link_lbl)

        root_layout.addWidget(statusbar)

        # 6. Setup System Tray
        self.tray_manager = TrayManager(self)
        self.tray_manager.sig_show_window.connect(self.show_and_activate)
        self.tray_manager.sig_toggle_sidetone.connect(self._toggle_sidetone_from_tray)
        self.tray_manager.sig_quit_app.connect(self._quit_application)

        # 7. Connect Worker Signals
        self._connect_signals()

        # 8. Connect i18n dynamic updates
        I18N.sig_language_changed.connect(self.retranslate)

        # 9. Start Worker Thread
        self.worker.start()

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Showcase Hero Card - Industrial Header
        hero_card = QFrame()
        hero_card.setProperty("class", "card")
        hero_layout = QHBoxLayout(hero_card)
        hero_layout.setContentsMargins(18, 16, 18, 16)

        info_box = QVBoxLayout()
        info_box.setSpacing(6)
        self.hero_title = QLabel(I18N.t("hero_title"))
        self.hero_title.setStyleSheet(
            "font-size: 16px; font-weight: 900; color: #FFFFFF; letter-spacing: 1px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.hero_desc = QLabel(I18N.t("hero_subtitle"))
        self.hero_desc.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        info_box.addWidget(self.hero_title)
        info_box.addWidget(self.hero_desc)

        # Spec chips - Monospace badges
        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)
        for label in ["[1000Hz_POLLING]", "[48kHz_24BIT_STUDIO]", "[10-BAND_PARAMETRIC_DSP]", "[<1.8ms_RF_LATENCY]"]:
            chip = QLabel(label)
            chip.setStyleSheet(
                "background-color: #16161E; color: #8F92A2; border: 1px solid #282836; "
                "border-radius: 2px; padding: 3px 8px; font-size: 9px; font-weight: 700; "
                "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
            )
            chips_row.addWidget(chip)
        chips_row.addStretch()
        info_box.addLayout(chips_row)

        hero_layout.addLayout(info_box)
        hero_layout.addStretch()

        self.hero_refresh_btn = QPushButton(I18N.t("refresh_btn"))
        self.hero_refresh_btn.setProperty("class", "action-btn")
        self.hero_refresh_btn.clicked.connect(lambda: self.worker.queue_command("refresh_all"))
        hero_layout.addWidget(self.hero_refresh_btn)

        layout.addWidget(hero_card)

        # Quick Control Cards Grid
        grid_card = QFrame()
        grid_card.setProperty("class", "card")
        grid_layout = QVBoxLayout(grid_card)
        grid_layout.setSpacing(12)

        self.dash_grid_title = QLabel(I18N.t("quick_controls_title"))
        self.dash_grid_title.setStyleSheet(
            "font-size: 11px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.8px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        grid_layout.addWidget(self.dash_grid_title)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(10)

        # Card A: Sidetone
        c_side = QFrame()
        c_side.setProperty("class", "sub-card")
        cs_layout = QVBoxLayout(c_side)
        cs_layout.setSpacing(8)
        self.dash_cs_title = QLabel(I18N.t("quick_sidetone_title"))
        self.dash_cs_title.setStyleSheet(
            "font-weight: 800; color: #FFFFFF; font-size: 11px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_cs_sub = QLabel(I18N.t("quick_sidetone_desc"))
        self.dash_cs_sub.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        cs_layout.addWidget(self.dash_cs_title)
        cs_layout.addWidget(self.dash_cs_sub)

        cs_bottom = QHBoxLayout()
        self.dash_side_lbl = QLabel(I18N.t("sidetone_on"))
        self.dash_side_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #FF5500; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_side_sw = ToggleSwitch(checked=True)
        self.dash_side_sw.toggled.connect(
            lambda chk: self.worker.queue_command("set_sidetone", enabled=chk, volume=100)
        )
        cs_bottom.addWidget(self.dash_side_lbl)
        cs_bottom.addStretch()
        cs_bottom.addWidget(self.dash_side_sw)
        cs_layout.addLayout(cs_bottom)
        cards_row.addWidget(c_side)

        # Card B: Mic Mute
        c_mic = QFrame()
        c_mic.setProperty("class", "sub-card")
        cm_layout = QVBoxLayout(c_mic)
        cm_layout.setSpacing(8)
        self.dash_cm_title = QLabel(I18N.t("quick_mic_title"))
        self.dash_cm_title.setStyleSheet(
            "font-weight: 800; color: #FFFFFF; font-size: 11px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_cm_sub = QLabel(I18N.t("quick_mic_desc"))
        self.dash_cm_sub.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        cm_layout.addWidget(self.dash_cm_title)
        cm_layout.addWidget(self.dash_cm_sub)

        cm_bottom = QHBoxLayout()
        self.dash_mute_lbl = QLabel(I18N.t("mic_active"))
        self.dash_mute_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #00F5A0; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_mute_sw = ToggleSwitch(checked=False)
        self.dash_mute_sw.toggled.connect(
            lambda chk: self.worker.queue_command("set_mic_mute", mute=chk)
        )
        cm_bottom.addWidget(self.dash_mute_lbl)
        cm_bottom.addStretch()
        cm_bottom.addWidget(self.dash_mute_sw)
        cm_layout.addLayout(cm_bottom)
        cards_row.addWidget(c_mic)

        # Card C: 7.1 Surround
        c_surr = QFrame()
        c_surr.setProperty("class", "sub-card")
        cr_layout = QVBoxLayout(c_surr)
        cr_layout.setSpacing(8)
        self.dash_cr_title = QLabel(I18N.t("quick_surround_title"))
        self.dash_cr_title.setStyleSheet(
            "font-weight: 800; color: #FFFFFF; font-size: 11px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_cr_sub = QLabel(I18N.t("quick_surround_desc"))
        self.dash_cr_sub.setStyleSheet("font-size: 11px; color: #7D7F8E;")
        cr_layout.addWidget(self.dash_cr_title)
        cr_layout.addWidget(self.dash_cr_sub)

        cr_bottom = QHBoxLayout()
        self.dash_surr_lbl = QLabel(I18N.t("surround_off"))
        self.dash_surr_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #626574; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        self.dash_surr_sw = ToggleSwitch(checked=False)
        self.dash_surr_sw.toggled.connect(
            lambda chk: self.worker.queue_command("set_surround", enabled=chk)
        )
        cr_bottom.addWidget(self.dash_surr_lbl)
        cr_bottom.addStretch()
        cr_bottom.addWidget(self.dash_surr_sw)
        cr_layout.addLayout(cr_bottom)
        cards_row.addWidget(c_surr)

        grid_layout.addLayout(cards_row)
        layout.addWidget(grid_card)

        layout.addStretch()
        return page

    def _build_info_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        card = QFrame()
        card.setProperty("class", "card")
        c_layout = QVBoxLayout(card)
        c_layout.setSpacing(12)

        self.info_title = QLabel(I18N.t("info_title"))
        self.info_title.setStyleSheet(
            "font-size: 12px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.8px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        c_layout.addWidget(self.info_title)

        info_items = [
            ("info_manufacturer", "Beibinghe Technology ATK N9 PRO / Ultra"),
            ("info_vid_pid", "373B:11CB (2.4G Dongle) / 373B:11CA (Kablolu)"),
            ("info_port", "USB CDC-ACM Seri Port (/dev/ttyACM0)"),
            ("info_format", "9600 Baud, 8 Data Bit, 1 Stop Bit, No Parity (8N1)"),
            ("info_framing", "Sabit 64-Bayt Çift Yönlü DSP Kontrol & Telemetri"),
            ("info_audio_engine", "USB Audio Class 1.0 (PipeWire / ALSA Native)"),
            ("info_media_keys", "Linux Input Subsystem (hid-generic Consumer Controls)")
        ]

        self.info_labels = {}
        for key, val in info_items:
            row = QHBoxLayout()
            lbl_k = QLabel(I18N.t(key))
            lbl_k.setStyleSheet(
                "color: #7D7F8E; font-weight: 700; min-width: 190px; font-size: 10px; "
                "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
            )
            self.info_labels[key] = lbl_k

            lbl_v = QLabel(val)
            lbl_v.setStyleSheet(
                "color: #FFFFFF; font-weight: 700; font-size: 10px; "
                "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
            )
            row.addWidget(lbl_k)
            row.addWidget(lbl_v)
            row.addStretch()
            c_layout.addLayout(row)

        c_layout.addSpacing(10)

        # Application Preferences Box
        opt_box = QFrame()
        opt_box.setProperty("class", "sub-card")
        ob_layout = QVBoxLayout(opt_box)
        ob_layout.setSpacing(12)

        self.opt_title = QLabel(I18N.t("settings_options_title"))
        self.opt_title.setStyleSheet(
            "font-size: 11px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.8px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        ob_layout.addWidget(self.opt_title)

        # Language Selection Row
        lang_row = QHBoxLayout()
        self.lang_label = QLabel(I18N.t("settings_language"))
        self.lang_label.setStyleSheet(
            "color: #9A9EAE; font-weight: 700; font-size: 11px; "
            "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;"
        )
        lang_row.addWidget(self.lang_label)
        lang_row.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("🇹🇷 Türkçe (TR)", "tr")
        self.lang_combo.addItem("🇬🇧 English (EN)", "en")
        curr_idx = 0 if I18N.current_language == "tr" else 1
        self.lang_combo.setCurrentIndex(curr_idx)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        lang_row.addWidget(self.lang_combo)
        ob_layout.addLayout(lang_row)

        # Tray minimize Checkbox
        self.tray_check = QCheckBox(I18N.t("settings_minimize_tray"))
        self.tray_check.setChecked(self.minimize_to_tray)
        self.tray_check.toggled.connect(self._on_tray_toggle)
        self.tray_check.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 12px;")
        ob_layout.addWidget(self.tray_check)

        # Autostart Checkbox
        self.autostart_check = QCheckBox(I18N.t("settings_autostart"))
        self.autostart_check.setChecked(is_autostart_enabled())
        self.autostart_check.toggled.connect(self._on_autostart_toggle)
        self.autostart_check.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 12px;")
        ob_layout.addWidget(self.autostart_check)

        c_layout.addWidget(opt_box)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def _on_page_changed(self, index: int):
        if index == 2:
            self.mic_widget.start_monitoring()
        else:
            self.mic_widget.stop_monitoring()

    def _on_tray_toggle(self, checked: bool):
        self.minimize_to_tray = bool(checked)
        CONFIG.set("minimize_to_tray", self.minimize_to_tray)

    def _on_autostart_toggle(self, checked: bool):
        set_autostart(bool(checked))

    def _on_language_changed(self, index: int):
        lang = self.lang_combo.itemData(index)
        if lang:
            I18N.set_language(lang)

    def retranslate(self, lang=None):
        self.setWindowTitle(I18N.t("app_title"))
        self.brand_title.setText(I18N.t("app_brand"))
        self.brand_sub.setText(I18N.t("version_tag"))

        # Sidebar navigation buttons
        for btn, key in self.nav_buttons:
            btn.setText(I18N.t(key))

        # Dashboard hero
        self.hero_title.setText(I18N.t("hero_title"))
        self.hero_desc.setText(I18N.t("hero_subtitle"))
        self.hero_refresh_btn.setText(I18N.t("refresh_btn"))
        self.dash_grid_title.setText(I18N.t("quick_controls_title"))

        # Dashboard quick controls
        self.dash_cs_title.setText(I18N.t("quick_sidetone_title"))
        self.dash_cs_sub.setText(I18N.t("quick_sidetone_desc"))
        self.dash_side_lbl.setText(I18N.t("sidetone_on") if self._last_sidetone else I18N.t("sidetone_off"))

        self.dash_cm_title.setText(I18N.t("quick_mic_title"))
        self.dash_cm_sub.setText(I18N.t("quick_mic_desc"))
        self.dash_mute_lbl.setText(I18N.t("mic_muted") if self._last_mute else I18N.t("mic_active"))

        self.dash_cr_title.setText(I18N.t("quick_surround_title"))
        self.dash_cr_sub.setText(I18N.t("quick_surround_desc"))
        self.dash_surr_lbl.setText(I18N.t("surround_on") if self._last_surround else I18N.t("surround_off"))

        # Settings & Info page
        self.info_title.setText(I18N.t("info_title"))
        for key, lbl in self.info_labels.items():
            lbl.setText(I18N.t(key))
        self.opt_title.setText(I18N.t("settings_options_title"))
        self.lang_label.setText(I18N.t("settings_language"))
        self.tray_check.setText(I18N.t("settings_minimize_tray"))
        self.autostart_check.setText(I18N.t("settings_autostart"))

        # Sync language combo
        target_idx = 0 if I18N.current_language == "tr" else 1
        if self.lang_combo.currentIndex() != target_idx:
            self.lang_combo.blockSignals(True)
            self.lang_combo.setCurrentIndex(target_idx)
            self.lang_combo.blockSignals(False)

        # Status Bar
        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if self._is_port_open:
            self.status_port_lbl.setText(f"PORT: {self._last_port_msg} (9600 8N1)")
        else:
            p_msg = f" ({self._last_port_msg})" if self._last_port_msg else ""
            self.status_port_lbl.setText(f"{I18N.t('status_not_connected')}{p_msg}")

        if self._is_rf_connected:
            self.status_link_lbl.setText(I18N.t("status_link_active"))
            self.status_link_lbl.setStyleSheet(mono_font + "color: #00F5A0; font-size: 10px; font-weight: 700;")
        else:
            self.status_link_lbl.setText(I18N.t("status_link_none"))
            self.status_link_lbl.setStyleSheet(mono_font + "color: #FF4B5C; font-size: 10px; font-weight: 700;")

    def _connect_signals(self):
        # Worker to UI
        self.worker.sig_connection_changed.connect(self._on_connection_changed)
        self.worker.sig_status_updated.connect(self._on_status_updated)
        self.worker.sig_mic_updated.connect(self._on_mic_updated)
        self.worker.sig_eq_updated.connect(self._on_eq_updated)
        self.worker.sig_surround_updated.connect(self._on_surround_updated)
        self.worker.sig_effect_updated.connect(self._on_effect_updated)

        # UI to Worker Commands
        self.eq_widget.sig_apply_bands.connect(
            lambda bands: self.worker.queue_command("set_eq_bands", eq_id=5, bands=bands)
        )
        self.eq_widget.sig_apply_preset.connect(
            lambda pname: self.worker.queue_command("apply_preset", preset_name=pname)
        )
        self.mic_widget.sig_set_mic_mute.connect(
            lambda mute: self.worker.queue_command("set_mic_mute", mute=mute)
        )
        self.mic_widget.sig_set_mic_volume.connect(
            lambda vol: self.worker.queue_command("set_mic_volume", volume=vol)
        )
        self.mic_widget.sig_set_sidetone.connect(
            lambda en, vol: self.worker.queue_command("set_sidetone", enabled=en, volume=vol)
        )
        self.effects_widget.sig_set_surround.connect(
            lambda en: self.worker.queue_command("set_surround", enabled=en)
        )
        self.effects_widget.sig_set_effect.connect(
            lambda eff: self.worker.queue_command("set_effect", effect_id=eff)
        )

    def _on_connection_changed(self, port_open: bool, msg: str):
        self._is_port_open = port_open
        self._last_port_msg = msg
        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if not port_open:
            self._is_rf_connected = False
            self.battery_widget.set_status(False)
            self.tray_manager.update_status(False)
            self.status_port_lbl.setText(f"{I18N.t('status_not_connected')} ({msg})")
            self.status_link_lbl.setText(I18N.t("status_link_none"))
            self.status_link_lbl.setStyleSheet(mono_font + "color: #FF4B5C; font-size: 10px; font-weight: 700;")
        else:
            self.status_port_lbl.setText(f"PORT: {msg} (9600 8N1)")

    def _on_status_updated(self, data: dict):
        connected = data.get("connected", False)
        self._is_rf_connected = connected
        lvl = data.get("level", 0)
        chg = data.get("charging", False)
        self.battery_widget.set_status(connected, lvl, chg)
        self.tray_manager.update_status(connected, lvl, chg)

        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if connected:
            self.status_link_lbl.setText(I18N.t("status_link_active"))
            self.status_link_lbl.setStyleSheet(mono_font + "color: #00F5A0; font-size: 10px; font-weight: 700;")
        else:
            self.status_link_lbl.setText(I18N.t("status_link_none"))
            self.status_link_lbl.setStyleSheet(mono_font + "color: #FF4B5C; font-size: 10px; font-weight: 700;")

    def _on_mic_updated(self, data: dict):
        mute = data.get("mute")
        vol = data.get("volume")
        s_en = data.get("sidetone_enabled")
        s_vol = data.get("sidetone_volume")
        self.mic_widget.update_state(mute, vol, s_en, s_vol)

        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        if mute is not None:
            self._last_mute = mute
            self.dash_mute_sw.blockSignals(True)
            self.dash_mute_sw.setChecked(mute)
            self.dash_mute_sw.blockSignals(False)
            self.dash_mute_lbl.setText(I18N.t("mic_muted") if mute else I18N.t("mic_active"))
            self.dash_mute_lbl.setStyleSheet(
                mono_font + "font-size: 11px; font-weight: 800; color: #FF5500;" if mute
                else mono_font + "font-size: 11px; font-weight: 700; color: #00F5A0;"
            )

        if s_en is not None:
            self._last_sidetone = s_en
            self.dash_side_sw.blockSignals(True)
            self.dash_side_sw.setChecked(s_en)
            self.dash_side_sw.blockSignals(False)
            self.dash_side_lbl.setText(I18N.t("sidetone_on") if s_en else I18N.t("sidetone_off"))
            self.dash_side_lbl.setStyleSheet(
                mono_font + "font-size: 11px; font-weight: 700; color: #FF5500;" if s_en
                else mono_font + "font-size: 11px; font-weight: 600; color: #626574;"
            )

    def _on_eq_updated(self, data: dict):
        bands = data.get("bands")
        if bands:
            self.eq_widget.update_bands(bands)

    def _on_surround_updated(self, data: dict):
        en = data.get("enabled", False)
        self._last_surround = en
        self.effects_widget.update_state(surround_en=en)
        self.dash_surr_sw.blockSignals(True)
        self.dash_surr_sw.setChecked(en)
        self.dash_surr_sw.blockSignals(False)
        self.dash_surr_lbl.setText(I18N.t("surround_on") if en else I18N.t("surround_off"))
        mono_font = "font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace; "
        self.dash_surr_lbl.setStyleSheet(
            mono_font + "font-size: 11px; font-weight: 700; color: #FF5500;" if en
            else mono_font + "font-size: 11px; font-weight: 600; color: #626574;"
        )

    def _on_effect_updated(self, data: dict):
        en = data.get("enabled", False)
        eff_id = data.get("effect_id", 0)
        self.effects_widget.update_state(effect_en=en, effect_id=eff_id)

    def _toggle_sidetone_from_tray(self):
        cur_en = self.mic_widget.sidetone_enabled
        new_en = not cur_en
        self.worker.queue_command("set_sidetone", enabled=new_en, volume=self.mic_widget.sidetone_volume)

    def show_and_activate(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.raise_()
        self.activateWindow()
        if self.pages_stack.currentIndex() == 2:
            self.mic_widget.start_monitoring()

    def get_telemetry_json(self) -> str:
        """Return live telemetry as a JSON string for IPC and CLI queries."""
        connected = bool(self._is_rf_connected)
        lvl = getattr(self.battery_widget, "level", 0)
        chg = getattr(self.battery_widget, "charging", False)
        chg_tag = " (⚡)" if chg else ""
        text_val = f"{lvl}%{chg_tag}" if connected else "N/A"
        tooltip_val = f"ATK Neptune N9: {lvl}%{chg_tag} ({'Bağlı' if connected else 'Bağlantı Yok'})"
        cls_val = "charging" if chg else ("connected" if connected else "disconnected")

        effect_name = "OFF"
        if hasattr(self, "effects_widget") and getattr(self.effects_widget, "active_effect_id", -1) >= 0:
            eff_map = {0: "Male", 1: "Female", 2: "Monster", 3: "Cartoon"}
            effect_name = eff_map.get(self.effects_widget.active_effect_id, "Custom")

        data = {
            "connected": connected,
            "battery": lvl,
            "charging": chg,
            "mic": {
                "mute": bool(self._last_mute),
                "volume": getattr(self.mic_widget, "mic_volume", 100),
                "sidetone_enabled": bool(self._last_sidetone),
                "sidetone_volume": getattr(self.mic_widget, "sidetone_volume", 100),
            },
            "audio": {
                "surround_7_1": bool(self._last_surround),
                "effect": effect_name
            },
            "port": self._last_port_msg,
            "text": text_val,
            "percentage": lvl if connected else 0,
            "tooltip": tooltip_val,
            "class": cls_val
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _quit_application(self):
        self._is_quitting = True
        self.mic_widget.stop_monitoring()
        self.tray_manager.cleanup()
        self.worker.stop()
        self.close()
        app = QApplication.instance()
        if app:
            app.quit()

    def closeEvent(self, event: QCloseEvent):
        if not self._is_quitting and self.minimize_to_tray:
            self.mic_widget.stop_monitoring()
            event.ignore()
            self.hide()
        else:
            self._is_quitting = True
            self.mic_widget.stop_monitoring()
            self.tray_manager.cleanup()
            self.worker.stop()
            event.accept()
            app = QApplication.instance()
            if app:
                app.quit()
