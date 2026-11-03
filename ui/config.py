"""
Configuration and settings manager for ATK Neptune N9 Linux Control Center.
Manages persistent user preferences stored in ~/.config/atk-n9/settings.json.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_SETTINGS: Dict[str, Any] = {
    "language": "tr",
    "minimize_to_tray": True,
    "autostart": False,
}


def get_autostart_desktop_path() -> Path:
    """Return path to autostart desktop entry file."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg_config) if xdg_config else Path.home() / ".config"
    return base / "autostart" / "atk-neptune-n9.desktop"


def is_autostart_enabled() -> bool:
    """Check if autostart desktop entry is present."""
    return get_autostart_desktop_path().exists()


def set_autostart(enable: bool, run_script_path: Path | None = None):
    """Enable or disable autostart by managing the desktop file."""
    desktop_file = get_autostart_desktop_path()
    if enable:
        desktop_file.parent.mkdir(parents=True, exist_ok=True)
        if run_script_path is None:
            script_candidate = (Path(__file__).parent.parent / "run_gui.sh").resolve()
        else:
            script_candidate = Path(run_script_path).resolve()

        content = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=ATK Neptune N9\n"
            "Comment=ATK Neptune N9 Headset Linux Control Center\n"
            f"Exec={script_candidate} --minimized\n"
            "Icon=audio-headset\n"
            "Terminal=false\n"
            "Categories=AudioVideo;Audio;Settings;\n"
            "X-GNOME-Autostart-enabled=true\n"
        )
        desktop_file.write_text(content, encoding="utf-8")
    else:
        if desktop_file.exists() or desktop_file.is_symlink():
            try:
                desktop_file.unlink()
            except Exception:
                pass
    CONFIG.set("autostart", enable)


def resolve_config_dir() -> Path:
    """Return the configuration directory path, respecting XDG_CONFIG_HOME."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    config_dir = base / "atk-n9"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Convenience alias: ~/.config/atk-neptune-n9 -> ~/.config/atk-n9
    alias_dir = base / "atk-neptune-n9"
    try:
        if not alias_dir.exists() and not alias_dir.is_symlink():
            alias_dir.symlink_to(config_dir.name)
    except Exception:
        pass

    return config_dir


class ConfigManager:
    def __init__(self, config_dir: Path | None = None):
        self.config_dir = config_dir if config_dir is not None else resolve_config_dir()
        self.config_file = self.config_dir / "settings.json"
        self._settings: Dict[str, Any] = dict(DEFAULT_SETTINGS)
        self.load()

    def reload(self, config_dir: Path | None = None):
        """Reload configuration from disk."""
        if config_dir is not None:
            self.config_dir = config_dir
        else:
            self.config_dir = resolve_config_dir()
        self.config_file = self.config_dir / "settings.json"
        self._settings = dict(DEFAULT_SETTINGS)
        self.load()

    def load(self):
        """Load settings from JSON file."""
        if self.config_file.exists():
            try:
                content = self.config_file.read_text(encoding="utf-8").strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        self._settings.update(data)
            except Exception as e:
                print(f"[Config] Warning: failed to load settings from {self.config_file}: {e}")

    def save(self):
        """Save settings to JSON file atomically."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            temp_file = self.config_file.with_suffix(".tmp")
            data_str = json.dumps(self._settings, indent=2, ensure_ascii=False)
            temp_file.write_text(data_str + "\n", encoding="utf-8")
            temp_file.replace(self.config_file)
        except Exception as e:
            print(f"[Config] Error: failed to save settings to {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value with fallback to default."""
        return self._settings.get(key, default if default is not None else DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any):
        """Set a setting value and persist immediately."""
        self._settings[key] = value
        self.save()

    def all(self) -> Dict[str, Any]:
        """Return a copy of all current settings."""
        return dict(self._settings)


# Global singleton instance
CONFIG = ConfigManager()
