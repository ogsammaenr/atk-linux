"""
Internationalization (i18n) Manager for ATK Neptune N9 Linux Control Center.
Supports Turkish ('tr') and English ('en') with persistent user settings.
"""

import json
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

CONFIG_DIR = Path.home() / ".config" / "atk-n9"
CONFIG_FILE = CONFIG_DIR / "settings.json"

TRANSLATIONS = {
    "tr": {
        # App / Window
        "app_title": "ATK Neptune N9 - Linux Kontrol Merkezi",
        "app_brand": "ATK NEPTUNE N9",
        "version_tag": "ATK Linux Native v1.1",
        
        # Navigation
        "nav_dashboard": "⚡ Genel Bakış",
        "nav_eq": "🎚 Ekolayzır (EQ)",
        "nav_mic": "🎙 Mikrofon & Yan Ton",
        "nav_effects": "✨ Ses Efektleri & 7.1",
        "nav_settings": "⚙ Cihaz & Ayarlar",
        
        # Header Status
        "searching_device": "Bağlantı Aranıyor...",
        "connected_badge": "● Bağlı",
        "disconnected_badge": "○ Bağlantı Yok",
        "charging_tag": " (Şarjda)",
        
        # Dashboard
        "hero_title": "ATK Neptune N9 Pro / Ultra",
        "hero_subtitle": "Çift Modlu (2.4GHz RF / USB-C Kablolu) Ultra Düşük Gecikmeli Espor Oyuncu Kulaklığı",
        "refresh_btn": "Yenile ↻",
        "quick_controls_title": "HIZLI DONANIM KONTROLLERİ",
        
        "quick_sidetone_title": "🎧 Yan Ton (Sidetone)",
        "quick_sidetone_desc": "Kulaklık içi donanım geri beslemesi",
        "sidetone_on": "Açık",
        "sidetone_off": "Kapalı",
        
        "quick_mic_title": "🎙 Mikrofon Durumu",
        "quick_mic_desc": "Fiziksel susturma anahtarı",
        "mic_active": "Aktif",
        "mic_muted": "Sessizde",
        
        "quick_surround_title": "🌐 Sanal 7.1 Surround",
        "quick_surround_desc": "360° uzamsal ses derinliği",
        "surround_on": "7.1 Açık",
        "surround_off": "Kapalı",
        
        # Equalizer
        "eq_title": "10-BANT PARAMETRİK DSP EKOLAYZIR",
        "eq_subtitle": "Kulaklığın dahili donanım DSP çipi üzerinde gerçek zamanlı ses eğrisi işleme",
        "eq_reset_btn": "↺ Sıfırla (Flat)",
        
        # Microphone & Sidetone
        "mic_settings_title": "🎙 MİKROFON GİRİŞ AYARLARI",
        "mic_settings_desc": "Kulaklık mikrofon hassasiyeti ve susturma durumu",
        "mic_input_level": "Giriş Seviyesi:",
        "mic_unmuted_label": "Mikrofon Açık",
        "mic_muted_label": "Sessizde (Muted)",
        
        "sidetone_settings_title": "🎧 YAN TON (SIDETONE / HARDWARE MONITOR)",
        "sidetone_settings_desc": "Kulaklık içinden kendi sesinizi sıfır gecikmeyle duyarak konuşma netliğini artırın",
        "sidetone_level": "Yan Ton Şiddeti:",
        "sidetone_active_label": "Yan Ton: Açık",
        "sidetone_inactive_label": "Yan Ton: Kapalı",
        
        # Effects & 7.1
        "surround_title": "🌐 SANAL 7.1 UZAMSAL ÇEVRESEL SES (VIRTUAL 7.1 SURROUND)",
        "surround_desc": "360° uzamsal ses derinliği ile düşman ayak sesleri ve silah yön tayini",
        "voice_changer_title": "🎭 SES DEĞİŞTİRİCİ DSP EFEKTLERİ (VOICE CHANGER)",
        "voice_changer_desc": "Kulaklığın dahili DSP çipinde gerçek zamanlı modüle edilen ses efektleri",
        "vc_normal": "Normal / Orijinal",
        "vc_male": "👨 Erkek Sesi (Male)",
        "vc_female": "👩 Kadın Sesi (Female)",
        "vc_monster": "👹 Canavar Sesi (Monster)",
        "vc_cartoon": "🦆 Çizgi Film / Ördek",
        
        # Settings & Info
        "info_title": "DONANIM VE PROTOKOL DETAYLARI",
        "info_manufacturer": "Üretici ve Cihaz:",
        "info_vid_pid": "USB VID:PID:",
        "info_port": "Kontrol İletişim Portu:",
        "info_format": "Haberleşme Formatı:",
        "info_framing": "Çerçeve Mimarisi:",
        "info_audio_engine": "Ses Motoru Entegrasyonu:",
        "info_media_keys": "Medya Tuşları:",
        
        "settings_options_title": "UYGULAMA TERCİHLERİ",
        "settings_minimize_tray": "Pencereyi kapatınca uygulamayı sistem tepsisine (Tray) küçült",
        "settings_language": "Arayüz Dili / Language:",
        
        # Status Bar
        "status_searching": "Port: Aranıyor...",
        "status_not_connected": "Port: Bağlı Değil",
        "status_link_active": "2.4GHz RF Bağlantısı: Aktif ●",
        "status_link_none": "Bağlantı Yok ○",
        
        # System Tray
        "tray_title": "🎧 ATK Neptune N9",
        "tray_battery": "Pil: ",
        "tray_disconnected": "Bağlantı Yok",
        "tray_toggle_sidetone": "Yan Tonu Aç / Kapat",
        "tray_show_window": "Arayüzü Göster",
        "tray_quit": "Çıkış"
    },
    
    "en": {
        # App / Window
        "app_title": "ATK Neptune N9 - Linux Control Center",
        "app_brand": "ATK NEPTUNE N9",
        "version_tag": "ATK Linux Native v1.1",
        
        # Navigation
        "nav_dashboard": "⚡ Overview",
        "nav_eq": "🎚 Equalizer (EQ)",
        "nav_mic": "🎙 Mic & Sidetone",
        "nav_effects": "✨ Audio Effects & 7.1",
        "nav_settings": "⚙ Device & Settings",
        
        # Header Status
        "searching_device": "Searching Device...",
        "connected_badge": "● Connected",
        "disconnected_badge": "○ Disconnected",
        "charging_tag": " (Charging)",
        
        # Dashboard
        "hero_title": "ATK Neptune N9 Pro / Ultra",
        "hero_subtitle": "Dual-Mode (2.4GHz RF / USB-C Wired) Ultra-Low Latency Esports Gaming Headset",
        "refresh_btn": "Refresh ↻",
        "quick_controls_title": "QUICK HARDWARE CONTROLS",
        
        "quick_sidetone_title": "🎧 Sidetone (Monitor)",
        "quick_sidetone_desc": "Zero-latency in-ear hardware feedback",
        "sidetone_on": "On",
        "sidetone_off": "Off",
        
        "quick_mic_title": "🎙 Microphone Status",
        "quick_mic_desc": "Hardware mute switch state",
        "mic_active": "Active",
        "mic_muted": "Muted",
        
        "quick_surround_title": "🌐 Virtual 7.1 Surround",
        "quick_surround_desc": "360° spatial audio depth",
        "surround_on": "7.1 On",
        "surround_off": "Off",
        
        # Equalizer
        "eq_title": "10-BAND PARAMETRIC DSP EQUALIZER",
        "eq_subtitle": "Real-time audio curve processing on internal headset DSP chip",
        "eq_reset_btn": "↺ Reset (Flat)",
        
        # Microphone & Sidetone
        "mic_settings_title": "🎙 MICROPHONE INPUT SETTINGS",
        "mic_settings_desc": "Microphone gain sensitivity and hardware mute toggle",
        "mic_input_level": "Input Level:",
        "mic_unmuted_label": "Microphone Active",
        "mic_muted_label": "Muted",
        
        "sidetone_settings_title": "🎧 SIDETONE (HARDWARE MONITOR)",
        "sidetone_settings_desc": "Hear your own voice with zero latency for clearer communication",
        "sidetone_level": "Sidetone Level:",
        "sidetone_active_label": "Sidetone: On",
        "sidetone_inactive_label": "Sidetone: Off",
        
        # Effects & 7.1
        "surround_title": "🌐 VIRTUAL 7.1 SPATIAL SURROUND AUDIO",
        "surround_desc": "360° spatial depth for enemy footsteps and directional gunfire accuracy",
        "voice_changer_title": "🎭 VOICE CHANGER DSP EFFECTS",
        "voice_changer_desc": "Real-time modulated voice effects powered by internal DSP",
        "vc_normal": "Normal / Original",
        "vc_male": "👨 Male Voice",
        "vc_female": "👩 Female Voice",
        "vc_monster": "👹 Monster Voice",
        "vc_cartoon": "🦆 Cartoon / Duck",
        
        # Settings & Info
        "info_title": "HARDWARE & PROTOCOL DETAILS",
        "info_manufacturer": "Manufacturer & Model:",
        "info_vid_pid": "USB VID:PID:",
        "info_port": "Control Communication Port:",
        "info_format": "Serial Port Configuration:",
        "info_framing": "Packet Framing Architecture:",
        "info_audio_engine": "Audio Engine Integration:",
        "info_media_keys": "Hardware Media Keys:",
        
        "settings_options_title": "APPLICATION PREFERENCES",
        "settings_minimize_tray": "Minimize to system tray on window close",
        "settings_language": "Interface Language / Dil Seçimi:",
        
        # Status Bar
        "status_searching": "Port: Searching...",
        "status_not_connected": "Port: Disconnected",
        "status_link_active": "2.4GHz RF Link: Active ●",
        "status_link_none": "Disconnected ○",
        
        # System Tray
        "tray_title": "🎧 ATK Neptune N9",
        "tray_battery": "Battery: ",
        "tray_disconnected": "Disconnected",
        "tray_toggle_sidetone": "Toggle Sidetone",
        "tray_show_window": "Show Window",
        "tray_quit": "Quit"
    }
}


class I18nManager(QObject):
    sig_language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_language = "tr"
        self._load_settings()

    def t(self, key: str, **kwargs) -> str:
        """Translate a key into the currently active language."""
        lang_dict = TRANSLATIONS.get(self.current_language, TRANSLATIONS["tr"])
        text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def set_language(self, lang: str):
        if lang in ("tr", "en") and lang != self.current_language:
            self.current_language = lang
            self._save_settings()
            self.sig_language_changed.emit(lang)

    def _load_settings(self):
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                lang = data.get("language", "tr")
                if lang in ("tr", "en"):
                    self.current_language = lang
            except Exception:
                self.current_language = "tr"

    def _save_settings(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            data = {}
            if CONFIG_FILE.exists():
                try:
                    data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                except Exception:
                    data = {}
            data["language"] = self.current_language
            CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass


# Global singleton instance
I18N = I18nManager()
