"""
Internationalization (i18n) Manager for ATK Neptune N9 Linux Control Center.
Supports Turkish ('tr') and English ('en') with persistent user settings.
"""

import json
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from ui.config import CONFIG

CONFIG_DIR = CONFIG.config_dir
CONFIG_FILE = CONFIG.config_file

TRANSLATIONS = {
    "tr": {
        # App / Window
        "app_title": "ATK Neptune N9 - Linux Kontrol Merkezi",
        "app_brand": "ATK // NEPTUNE_N9",
        "version_tag": "[REV. PRO_ULTRA]",
        
        # Navigation (Nordic Numbered)
        "nav_dashboard": "01 GENEL BAKIŞ",
        "nav_eq": "02 EKOLAYZIR (EQ)",
        "nav_mic": "03 MİKROFON & YAN TON",
        "nav_effects": "04 UZAMSAL 7.1 & EFEKT",
        "nav_settings": "05 CİHAZ & AYARLAR",
        
        # Header Status
        "searching_device": "[CİHAZ_ARANIYOR]",
        "connected_badge": "[LINK: 2.4G_OK]",
        "disconnected_badge": "[BAĞLANTI_YOK]",
        "charging_tag": " [ŞARJ]",
        
        # Dashboard
        "hero_title": "ATK // NEPTUNE_N9",
        "hero_subtitle": "Dahili Donanım Parametrik DSP & Ultra Düşük Gecikmeli 2.4GHz RF Ses Mimarisi",
        "refresh_btn": "[YENİLE ↻]",
        "quick_controls_title": "DONANIM KONTROL BLOĞU",
        
        "quick_sidetone_title": "YAN TON // MONITOR",
        "quick_sidetone_desc": "Donanım seviyesi sıfır gecikmeli geri besleme",
        "sidetone_on": "[AKTİF]",
        "sidetone_off": "[KAPALI]",
        
        "quick_mic_title": "GİRİŞ // MİKROFON",
        "quick_mic_desc": "Fiziksel donanım susturma durumu",
        "mic_active": "[AKTİF]",
        "mic_muted": "[SESSİZDE]",
        
        "quick_surround_title": "UZAMSAL // SANAL 7.1",
        "quick_surround_desc": "360° yönsel çevresel ses matrisi",
        "surround_on": "[7.1 AKTİF]",
        "surround_off": "[KAPALI]",
        
        # Equalizer
        "eq_title": "BLOCK_01 // 10-BANT PARAMETRİK DSP MATRİSİ",
        "eq_subtitle": "Dahili donanım DSP işlemcisi üzerinde alt-milisaniye parametrik frekans eğrisi",
        "eq_reset_btn": "[SIFIRLA (FLAT)]",
        
        # Microphone & Sidetone
        "mic_settings_title": "BLOCK_02 // SES GİRİŞİ VE MİKROFON KONTROLÜ",
        "mic_settings_desc": "Giriş kazancı, donanım susturma ve sıfır gecikmeli yan ton döngüsü",
        "mic_input_level": "ANALOG KAZANÇ:",
        "mic_unmuted_label": "[MİKROFON AÇIK]",
        "mic_muted_label": "[SUSTURULDU]",
        "mic_vu_title": "GİRİŞ SİNYAL SEVİYESİ (PEAK dBFS)",
        "mic_vu_desc": "Gerçek zamanlı PipeWire tepe seviye monitörü (-60 ... 0 dBFS)",
        "mic_vu_muted": "[MİKROFON SUSTURULDU]",
        
        "sidetone_settings_title": "DONANIM YAN TON (HARDWARE SIDETONE)",
        "sidetone_settings_desc": "Kulaklık içine kendi sesinizin sıfır gecikmeyle karıştırılması",
        "sidetone_level": "MONİTÖR ŞİDDETİ:",
        "sidetone_active_label": "YAN TON: [AÇIK]",
        "sidetone_inactive_label": "YAN TON: [KAPALI]",
        
        # Effects & 7.1
        "surround_title": "BLOCK_03 // UZAMSAL 7.1 ÇEVRESEL SES MATRİSİ",
        "surround_desc": "360° kutupsal koordinat ses sahnemesi ile hassas yön tayini",
        "voice_changer_title": "DSP SES DEĞİŞTİRİCİ MATRİSİ (VOICE FX)",
        "voice_changer_desc": "Kulaklık donanım DSP çipinde gerçek zamanlı modülasyon",
        "vc_normal": "[01_ORİJİNAL]",
        "vc_male": "[02_ERKEK_SESİ]",
        "vc_female": "[03_KADIN_SESİ]",
        "vc_monster": "[04_CANAVAR]",
        "vc_cartoon": "[05_ÇİZGİ_FİLM]",
        
        # Settings & Info
        "info_title": "DONANIM TELEMETRİSİ VE PROTOKOL DETAYLARI",
        "info_manufacturer": "CİHAZ TANIMI:",
        "info_vid_pid": "USB VID:PID:",
        "info_port": "SERİ PORT:",
        "info_format": "PROTOKOL FORMATI:",
        "info_framing": "ÇERÇEVE BOYUTU:",
        "info_audio_engine": "SES ENTEGRASYONU:",
        "info_media_keys": "MEDYA ANAHTARLARI:",
        
        "settings_options_title": "SİSTEM TERCİHLERİ",
        "settings_minimize_tray": "Pencere kapatıldığında sistem tepsisinde (Tray) çalışmaya devam et",
        "settings_autostart": "Sistem açılışında arka planda otomatik başlat",
        "settings_language": "ARAYÜZ DİLİ / LANGUAGE:",
        
        # Status Bar
        "status_searching": "PORT: TARANIYOR...",
        "status_not_connected": "PORT: BAĞLANTI YOK",
        "status_link_active": "LINK: 2.4G_STABLE // 1000Hz ●",
        "status_link_none": "LINK: OFFLINE ○",
        
        # System Tray
        "tray_title": "ATK // NEPTUNE_N9",
        "tray_battery": "BATT: ",
        "tray_disconnected": "[BAĞLANTI YOK]",
        "tray_toggle_sidetone": "Yan Tonu Aç / Kapat",
        "tray_show_window": "Kontrol Merkezini Aç",
        "tray_quit": "Çıkış"
    },
    
    "en": {
        # App / Window
        "app_title": "ATK Neptune N9 - Linux Control Center",
        "app_brand": "ATK // NEPTUNE_N9",
        "version_tag": "[REV. PRO_ULTRA]",
        
        # Navigation (Nordic Numbered)
        "nav_dashboard": "01 DASHBOARD",
        "nav_eq": "02 EQ MATRIX",
        "nav_mic": "03 AUDIO INPUT",
        "nav_effects": "04 SPATIAL 7.1",
        "nav_settings": "05 SYS SETTINGS",
        
        # Header Status
        "searching_device": "[SEARCHING_DEV]",
        "connected_badge": "[LINK: 2.4G_OK]",
        "disconnected_badge": "[NO_LINK]",
        "charging_tag": " [CHG]",
        
        # Dashboard
        "hero_title": "ATK // NEPTUNE_N9",
        "hero_subtitle": "Hardware Parametric DSP & Ultra-Low Latency 2.4GHz RF Architecture",
        "refresh_btn": "[REFRESH ↻]",
        "quick_controls_title": "HARDWARE CONTROL BLOCK",
        
        "quick_sidetone_title": "SIDETONE // MONITOR",
        "quick_sidetone_desc": "Hardware zero-latency mic feedback loop",
        "sidetone_on": "[ACTIVE]",
        "sidetone_off": "[OFF]",
        
        "quick_mic_title": "INPUT // MICROPHONE",
        "quick_mic_desc": "Physical hardware mute switch state",
        "mic_active": "[ACTIVE]",
        "mic_muted": "[MUTED]",
        
        "quick_surround_title": "SPATIAL // VIRTUAL 7.1",
        "quick_surround_desc": "360° directional sound stage matrix",
        "surround_on": "[7.1 ACTIVE]",
        "surround_off": "[OFF]",
        
        # Equalizer
        "eq_title": "BLOCK_01 // 10-BAND PARAMETRIC DSP MATRIX",
        "eq_subtitle": "Sub-millisecond parametric response curve processed on-device",
        "eq_reset_btn": "[RESET (FLAT)]",
        
        # Microphone & Sidetone
        "mic_settings_title": "BLOCK_02 // AUDIO INPUT & MIC CONTROLS",
        "mic_settings_desc": "Input gain, hardware mute and zero-latency monitoring loop",
        "mic_input_level": "ANALOG GAIN:",
        "mic_unmuted_label": "[MIC UNMUTED]",
        "mic_muted_label": "[HARDWARE MUTED]",
        "mic_vu_title": "INPUT SIGNAL ACTIVITY (PEAK dBFS)",
        "mic_vu_desc": "Real-time PipeWire audio monitor scale (-60 ... 0 dBFS)",
        "mic_vu_muted": "[MIC MUTED]",
        
        "sidetone_settings_title": "HARDWARE SIDETONE MONITOR",
        "sidetone_settings_desc": "Zero-latency real-time voice monitoring loopback to headset",
        "sidetone_level": "MONITOR GAIN:",
        "sidetone_active_label": "SIDETONE: [ENGAGED]",
        "sidetone_inactive_label": "SIDETONE: [DISABLED]",
        
        # Effects & 7.1
        "surround_title": "BLOCK_03 // SPATIAL 7.1 SURROUND MATRIX",
        "surround_desc": "360° polar coordinate acoustic stage for tactical positioning",
        "voice_changer_title": "DSP VOICE CHANGER MATRIX (VOICE FX)",
        "voice_changer_desc": "Real-time hardware voice transformation running on headset DSP",
        "vc_normal": "[01_ORIGINAL]",
        "vc_male": "[02_MALE_VOICE]",
        "vc_female": "[03_FEMALE_VOICE]",
        "vc_monster": "[04_MONSTER_VOICE]",
        "vc_cartoon": "[05_CARTOON_DUCK]",
        
        # Settings & Info
        "info_title": "HARDWARE TELEMETRY & PROTOCOL SPECS",
        "info_manufacturer": "DEVICE IDENTIFIER:",
        "info_vid_pid": "USB VID:PID:",
        "info_port": "SERIAL PORT:",
        "info_format": "PROTOCOL FORMAT:",
        "info_framing": "PACKET FRAMING:",
        "info_audio_engine": "AUDIO ENGINE:",
        "info_media_keys": "HARDWARE CONTROLS:",
        
        "settings_options_title": "SYSTEM PREFERENCES",
        "settings_minimize_tray": "Minimize to system tray when closing the window",
        "settings_autostart": "Start automatically in background on system startup",
        "settings_language": "LANGUAGE / ARAYÜZ DİLİ:",
        
        # Status Bar
        "status_searching": "PORT: SCANNING...",
        "status_not_connected": "PORT: DISCONNECTED",
        "status_link_active": "LINK: 2.4G_STABLE // 1000Hz ●",
        "status_link_none": "LINK: OFFLINE ○",
        
        # System Tray
        "tray_title": "ATK // NEPTUNE_N9",
        "tray_battery": "BATT: ",
        "tray_disconnected": "[NO_LINK]",
        "tray_toggle_sidetone": "Toggle Sidetone Loop",
        "tray_show_window": "Open Control Center",
        "tray_quit": "Exit"
    }
}


class I18nManager(QObject):
    sig_language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_language = CONFIG.get("language", "tr")
        if self.current_language not in TRANSLATIONS:
            self.current_language = "tr"

    def set_language(self, lang_code: str):
        if lang_code in TRANSLATIONS and lang_code != self.current_language:
            self.current_language = lang_code
            CONFIG.set("language", lang_code)
            self.sig_language_changed.emit(lang_code)

    def t(self, key: str, **kwargs) -> str:
        lang_dict = TRANSLATIONS.get(self.current_language, TRANSLATIONS["tr"])
        text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text


# Global Singleton
I18N = I18nManager()
