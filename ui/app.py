"""
Ultra-Modern Linux Control Center Main Window for ATK Neptune N9.
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget, QButtonGroup, QCheckBox,
    QApplication, QGridLayout
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATK Neptune N9 Control Center")
        self.resize(920, 620)
        self.setMinimumSize(880, 580)
        self.setStyleSheet(MAIN_STYLESHEET)

        self.minimize_to_tray = True

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
        topbar.setFixedHeight(58)
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(24, 0, 24, 0)

        # Brand / Logo
        brand_box = QHBoxLayout()
        brand_box.setSpacing(12)
        brand_icon = QLabel("🎧")
        brand_icon.setStyleSheet("font-size: 22px;")
        brand_title = QLabel("ATK NEPTUNE N9")
        brand_title.setStyleSheet("font-size: 15px; font-weight: 900; letter-spacing: 1.2px; color: #FFFFFF;")
        brand_box.addWidget(brand_icon)
        brand_box.addWidget(brand_title)
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
        sidebar.setFixedWidth(210)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 18, 14, 18)
        sidebar_layout.setSpacing(6)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        nav_items = [
            ("⚡ Genel Bakış", 0),
            ("🎚 Ekolayzır (EQ)", 1),
            ("🎙 Mikrofon & Yan Ton", 2),
            ("✨ Ses Efektleri & 7.1", 3),
            ("⚙ Cihaz & Ayarlar", 4)
        ]

        for label, idx in nav_items:
            btn = QPushButton(label)
            btn.setProperty("class", "nav-btn")
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=idx: self.pages_stack.setCurrentIndex(i))
            self.nav_group.addButton(btn, idx)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        ver_lbl = QLabel("ATK Linux Native v1.1")
        ver_lbl.setStyleSheet("color: #4C5064; font-size: 11px; padding-left: 14px; font-weight: 600;")
        sidebar_layout.addWidget(ver_lbl)

        body_layout.addWidget(sidebar)

        # 4.2. Stacked Content Pages
        self.pages_stack = QStackedWidget()
        self.pages_stack.setContentsMargins(20, 18, 20, 18)

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

        body_layout.addWidget(self.pages_stack)
        root_layout.addWidget(body_widget)

        # 5. Bottom Status Bar
        statusbar = QFrame()
        statusbar.setObjectName("statusbar")
        statusbar.setFixedHeight(30)
        statusbar_layout = QHBoxLayout(statusbar)
        statusbar_layout.setContentsMargins(20, 0, 20, 0)

        self.status_port_lbl = QLabel("Port: Aranıyor...")
        self.status_port_lbl.setStyleSheet("color: #65697D; font-size: 11px; font-weight: 600;")
        statusbar_layout.addWidget(self.status_port_lbl)

        statusbar_layout.addStretch()

        self.status_link_lbl = QLabel("2.4GHz RF Bağlantısı: Aktif ●")
        self.status_link_lbl.setStyleSheet("color: #00F5A0; font-size: 11px; font-weight: 700;")
        statusbar_layout.addWidget(self.status_link_lbl)

        root_layout.addWidget(statusbar)

        # 6. Setup System Tray
        self.tray_manager = TrayManager(self)
        self.tray_manager.sig_show_window.connect(self.show_and_activate)
        self.tray_manager.sig_toggle_sidetone.connect(self._toggle_sidetone_from_tray)
        self.tray_manager.sig_quit_app.connect(self._quit_application)

        # 7. Connect Worker Signals
        self._connect_signals()

        # 8. Start Worker Thread
        self.worker.start()

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Showcase Card
        hero_card = QFrame()
        hero_card.setProperty("class", "card")
        hero_layout = QHBoxLayout(hero_card)
        hero_layout.setContentsMargins(22, 22, 22, 22)

        info_box = QVBoxLayout()
        info_box.setSpacing(6)
        m_title = QLabel("ATK Neptune N9 Pro / Ultra")
        m_title.setStyleSheet("font-size: 20px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.5px;")
        m_desc = QLabel("Çift Modlu (2.4GHz RF / USB-C Kablolu) Ultra Düşük Gecikmeli Espor Oyuncu Kulaklığı")
        m_desc.setStyleSheet("font-size: 12px; color: #7F8498;")
        info_box.addWidget(m_title)
        info_box.addWidget(m_desc)

        # Spec chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)
        for label in ["1000Hz Polling", "48kHz 24-Bit Studio Audio", "Parametrik DSP", "< 15ms RF"]:
            chip = QLabel(label)
            chip.setStyleSheet(
                "background-color: #1A1C26; color: #9A9FA8; border: 1px solid #272A38; "
                "border-radius: 6px; padding: 4px 10px; font-size: 11px; font-weight: 600;"
            )
            chips_row.addWidget(chip)
        chips_row.addStretch()
        info_box.addLayout(chips_row)

        hero_layout.addLayout(info_box)
        hero_layout.addStretch()

        refresh_btn = QPushButton("Yenile ↻")
        refresh_btn.setProperty("class", "action-btn")
        refresh_btn.clicked.connect(lambda: self.worker.queue_command("refresh_all"))
        hero_layout.addWidget(refresh_btn)

        layout.addWidget(hero_card)

        # Quick Control Cards Grid
        grid_card = QFrame()
        grid_card.setProperty("class", "card")
        grid_layout = QVBoxLayout(grid_card)
        grid_layout.setSpacing(14)

        grid_title = QLabel("HIZLI DONANIM KONTROLLERİ")
        grid_title.setStyleSheet("font-size: 13px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.5px;")
        grid_layout.addWidget(grid_title)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)

        # Card A: Sidetone
        c_side = QFrame()
        c_side.setProperty("class", "sub-card")
        cs_layout = QVBoxLayout(c_side)
        cs_layout.setSpacing(8)
        cs_title = QLabel("🎧 Yan Ton (Sidetone)")
        cs_title.setStyleSheet("font-weight: 700; color: #FFFFFF;")
        cs_sub = QLabel("Kulaklık içi donanım geri beslemesi")
        cs_sub.setStyleSheet("font-size: 11px; color: #72768A;")
        cs_layout.addWidget(cs_title)
        cs_layout.addWidget(cs_sub)

        cs_bottom = QHBoxLayout()
        self.dash_side_lbl = QLabel("Açık")
        self.dash_side_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00D2FF;")
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
        cm_title = QLabel("🎙 Mikrofon Durumu")
        cm_title.setStyleSheet("font-weight: 700; color: #FFFFFF;")
        cm_sub = QLabel("Fiziksel susturma anahtarı")
        cm_sub.setStyleSheet("font-size: 11px; color: #72768A;")
        cm_layout.addWidget(cm_title)
        cm_layout.addWidget(cm_sub)

        cm_bottom = QHBoxLayout()
        self.dash_mute_lbl = QLabel("Aktif")
        self.dash_mute_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00F5A0;")
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
        cr_title = QLabel("🌐 Sanal 7.1 Surround")
        cr_title.setStyleSheet("font-weight: 700; color: #FFFFFF;")
        cr_sub = QLabel("360° uzamsal ses derinliği")
        cr_sub.setStyleSheet("font-size: 11px; color: #72768A;")
        cr_layout.addWidget(cr_title)
        cr_layout.addWidget(cr_sub)

        cr_bottom = QHBoxLayout()
        self.dash_surr_lbl = QLabel("Kapalı")
        self.dash_surr_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #6E7284;")
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
        layout.setSpacing(16)

        card = QFrame()
        card.setProperty("class", "card")
        c_layout = QVBoxLayout(card)
        c_layout.setSpacing(14)

        title = QLabel("DONANIM VE PROTOKOL DETAYLARI")
        title.setStyleSheet("font-size: 14px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.6px;")
        c_layout.addWidget(title)

        info_items = [
            ("Üretici ve Cihaz:", "Beibinghe Technology ATK N9 PRO / Ultra"),
            ("USB VID:PID:", "373B:11CB (2.4G Dongle) / 373B:11CA (Kablolu)"),
            ("Kontrol İletişim Portu:", "USB CDC-ACM Seri Port (/dev/ttyACM0)"),
            ("Haberleşme Formatı:", "9600 Baud, 8 Data Bit, 1 Stop Bit, No Parity (8N1)"),
            ("Çerçeve Mimarisi:", "Sabit 64-Bayt Çift Yönlü DSP Kontrol & Telemetri"),
            ("Ses Motoru Entegrasyonu:", "USB Audio Class 1.0 (PipeWire / ALSA Native)"),
            ("Medya Tuşları:", "Linux Input Subsystem (hid-generic Consumer Controls)")
        ]

        for k, v in info_items:
            row = QHBoxLayout()
            lbl_k = QLabel(k)
            lbl_k.setStyleSheet("color: #72768A; font-weight: 600; min-width: 180px;")
            lbl_v = QLabel(v)
            lbl_v.setStyleSheet("color: #FFFFFF; font-weight: 700;")
            row.addWidget(lbl_k)
            row.addWidget(lbl_v)
            row.addStretch()
            c_layout.addLayout(row)

        c_layout.addSpacing(8)

        # Options Box
        opt_box = QFrame()
        opt_box.setProperty("class", "sub-card")
        ob_layout = QVBoxLayout(opt_box)
        self.tray_check = QCheckBox("Pencereyi kapatınca uygulamayı sistem tepsisine (Tray) küçült")
        self.tray_check.setChecked(True)
        self.tray_check.toggled.connect(lambda chk: setattr(self, "minimize_to_tray", chk))
        self.tray_check.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 13px;")
        ob_layout.addWidget(self.tray_check)
        c_layout.addWidget(opt_box)

        layout.addWidget(card)
        layout.addStretch()
        return page

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

    def _on_connection_changed(self, connected: bool, msg: str):
        self.battery_widget.set_status(connected)
        self.tray_manager.update_status(connected)
        if connected:
            self.status_port_lbl.setText(f"Port: {msg} (9600 8N1)")
            self.status_link_lbl.setText("2.4GHz RF Bağlantısı: Aktif ●")
            self.status_link_lbl.setStyleSheet("color: #00F5A0; font-size: 11px; font-weight: 700;")
        else:
            self.status_port_lbl.setText(f"Port: Bağlı Değil ({msg})")
            self.status_link_lbl.setText("Bağlantı Yok ○")
            self.status_link_lbl.setStyleSheet("color: #FF3366; font-size: 11px; font-weight: 700;")

    def _on_status_updated(self, data: dict):
        connected = data.get("connected", False)
        lvl = data.get("level", 0)
        chg = data.get("charging", False)
        self.battery_widget.set_status(connected, lvl, chg)
        self.tray_manager.update_status(connected, lvl, chg)

    def _on_mic_updated(self, data: dict):
        mute = data.get("mute")
        vol = data.get("volume")
        s_en = data.get("sidetone_enabled")
        s_vol = data.get("sidetone_volume")
        self.mic_widget.update_state(mute, vol, s_en, s_vol)

        if mute is not None:
            self.dash_mute_sw.blockSignals(True)
            self.dash_mute_sw.setChecked(mute)
            self.dash_mute_sw.blockSignals(False)
            self.dash_mute_lbl.setText("Sessizde" if mute else "Aktif")
            self.dash_mute_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #FF3366;" if mute else "font-size: 12px; font-weight: 700; color: #00F5A0;")

        if s_en is not None:
            self.dash_side_sw.blockSignals(True)
            self.dash_side_sw.setChecked(s_en)
            self.dash_side_sw.blockSignals(False)
            self.dash_side_lbl.setText("Açık" if s_en else "Kapalı")
            self.dash_side_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #00D2FF;" if s_en else "font-size: 12px; font-weight: 600; color: #6E7284;")

    def _on_eq_updated(self, data: dict):
        bands = data.get("bands")
        if bands:
            self.eq_widget.update_bands(bands)

    def _on_surround_updated(self, data: dict):
        en = data.get("enabled", False)
        self.effects_widget.update_state(surround_en=en)
        self.dash_surr_sw.blockSignals(True)
        self.dash_surr_sw.setChecked(en)
        self.dash_surr_sw.blockSignals(False)
        self.dash_surr_lbl.setText("7.1 Açık" if en else "Kapalı")
        self.dash_surr_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #00D2FF;" if en else "font-size: 12px; font-weight: 600; color: #6E7284;")

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
        self.activateWindow()

    def _quit_application(self):
        self.minimize_to_tray = False
        self.tray_manager.cleanup()
        self.worker.stop()
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent):
        if self.minimize_to_tray:
            event.ignore()
            self.hide()
        else:
            self.tray_manager.cleanup()
            self.worker.stop()
            event.accept()
