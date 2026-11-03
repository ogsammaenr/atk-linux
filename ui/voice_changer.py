"""
Real-time Voice Changer Manager for ATK Neptune N9 on Linux (PipeWire).
Uses LADSPA pitch-shifting DSP plugin and PipeWire filter-chain to alter microphone audio
in real-time for Discord, games, and recording applications.
"""

import os
import re
import time
import signal
import atexit
import subprocess
from pathlib import Path
from typing import Optional, List, Set

PLUGIN_DIR = Path(__file__).resolve().parent.parent / "dsp" / "ladspa"
PLUGIN_FILE = PLUGIN_DIR / "am_pitchshift_1433.so"

# Pitch shift presets for ATK N9 effects:
# 0: Male (deeper, masculine voice)
# 1: Female (elevated pitch, feminine voice)
# 2: Monster (deep, demonic growl)
# 3: Cartoon (high squeaky chipmunk / duck voice)
EFFECT_PRESETS = {
    0: {"name": "Male", "pitch": 0.82, "buffer_size": 4},
    1: {"name": "Female", "pitch": 1.35, "buffer_size": 4},
    2: {"name": "Monster", "pitch": 0.60, "buffer_size": 4},
    3: {"name": "Cartoon", "pitch": 1.68, "buffer_size": 4},
}

RUNTIME_DIR = Path.home() / ".config" / "atk-n9"


class VoiceChangerManager:
    def __init__(self):
        self.current_effect_id: int = -1
        self.process: Optional[subprocess.Popen] = None
        self.mic_node: Optional[str] = None
        self.intercepted_links: Set[str] = set()
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        self.conf_path = RUNTIME_DIR / "voice_changer_filter.conf"
        self._refresh_mic_node()
        atexit.register(self.cleanup)

    def _refresh_mic_node(self) -> Optional[str]:
        """Detect the PipeWire node name of the ATK N9 microphone."""
        try:
            out = subprocess.check_output(["pw-cli", "list-objects", "Node"], text=True, timeout=1.5)
            blocks = out.split("id ")
            for block in blocks:
                if 'media.class = "Audio/Source"' in block:
                    m_name = re.search(r'node\.name = "([^"]+)"', block)
                    m_desc = re.search(r'node\.description = "([^"]+)"', block)
                    name = m_name.group(1) if m_name else ""
                    desc = m_desc.group(1) if m_desc else ""
                    if ("ATK" in name or "ATK" in desc or "N9" in name or "N9" in desc) and "voice_changer" not in name:
                        self.mic_node = name
                        return name
        except Exception:
            pass
        return self.mic_node

    def _get_active_mic_links(self) -> List[str]:
        """Find active application input ports currently capturing from the hardware mic."""
        if not self.mic_node:
            self._refresh_mic_node()
        if not self.mic_node:
            return []

        links = []
        try:
            out = subprocess.check_output(["pw-link", "-l"], text=True, timeout=1.5)
            in_mic_block = False
            for line in out.splitlines():
                if self.mic_node in line and "capture" in line:
                    in_mic_block = True
                    continue
                if in_mic_block:
                    if line.startswith("  |-> "):
                        dest = line.strip().replace("|-> ", "")
                        if "voice_changer" not in dest:
                            links.append(dest)
                    elif not line.startswith("  "):
                        in_mic_block = False
        except Exception:
            pass
        return links

    def _generate_config(self, pitch: float, buffer_size: int = 4) -> str:
        plugin_path = str(PLUGIN_FILE if PLUGIN_FILE.exists() else Path.home() / ".ladspa" / "am_pitchshift_1433.so")
        target_mic = self.mic_node or "alsa_input.usb-Beibinghe_Technology_ATK_N9_PRO_dongle_4150354433333605-00.mono-fallback"

        return f"""context.properties = {{
    log.level = 0
}}

context.spa-libs = {{
    audio.convert.* = audioconvert/libspa-audioconvert
    support.*       = support/libspa-support
}}

context.modules = [
    {{ name = libpipewire-module-protocol-native }}
    {{ name = libpipewire-module-client-node }}
    {{ name = libpipewire-module-adapter }}
    {{ name = libpipewire-module-filter-chain
      flags = [ nofail ]
      args = {{
          node.description = "ATK N9 Voice Changer (Mic)"
          media.name       = "ATK N9 Voice Changer (Mic)"
          filter.graph = {{
              nodes = [
                  {{
                      name    = pitch
                      type    = ladspa
                      plugin  = "{plugin_path}"
                      label   = amPitchshift
                      control = {{
                          "Pitch shift" = {pitch}
                          "Buffer size" = {buffer_size}
                      }}
                  }}
              ]
              inputs  = [ "pitch:Input" ]
              outputs = [ "pitch:Output" ]
          }}
          capture.props = {{
              node.name        = "atk_n9_voice_changer.input"
              node.description = "ATK N9 Voice Changer Input"
              target.object    = "{target_mic}"
              stream.dont-remix = true
              node.passive     = true
          }}
          playback.props = {{
              node.name        = "atk_n9_voice_changer.output"
              node.description = "ATK N9 Voice Changer (Mic)"
              media.class      = "Audio/Source"
          }}
      }}
    }}
]
"""

    def set_effect(self, effect_id: int):
        """
        Switch real-time DSP voice effect:
        -1: Normal / Bypass (Original voice)
         0: Male
         1: Female
         2: Monster
         3: Cartoon
        """
        if effect_id == self.current_effect_id:
            return

        if effect_id == -1 or effect_id not in EFFECT_PRESETS:
            self._disable_effect()
            self.current_effect_id = -1
            return

        preset = EFFECT_PRESETS[effect_id]
        self._enable_effect(preset["pitch"], preset["buffer_size"])
        self.current_effect_id = effect_id

    def _enable_effect(self, pitch: float, buffer_size: int):
        self._refresh_mic_node()
        
        # 1. Query active links from hardware mic BEFORE stopping old process
        active_links = self._get_active_mic_links()
        for link in active_links:
            self.intercepted_links.add(link)

        # 2. Stop any existing voice changer process
        self._stop_process()

        # 3. Write new PipeWire filter-chain configuration
        conf_content = self._generate_config(pitch, buffer_size)
        try:
            self.conf_path.write_text(conf_content)
        except OSError:
            return

        # 4. Spawn PipeWire filter-chain process
        try:
            self.process = subprocess.Popen(
                ["pipewire", "-c", str(self.conf_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except Exception:
            return

        # 5. Wait for the node to register and link active streams
        time.sleep(0.3)
        self._relink_streams_to_filter()

    def _relink_streams_to_filter(self):
        vc_out = "atk_n9_voice_changer.output:capture_MONO"
        mic_cap = f"{self.mic_node}:capture_MONO" if self.mic_node else None

        # Re-link captured applications (e.g. vesktop/Discord, OBS)
        for dest in list(self.intercepted_links):
            if mic_cap:
                subprocess.run(["pw-link", "-d", mic_cap, dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["pw-link", vc_out, dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Set Voice Changer node as the default PipeWire audio source
        try:
            out = subprocess.check_output(["wpctl", "status"], text=True, timeout=1.0)
            for line in out.splitlines():
                if "atk_n9_voice_changer.output" in line:
                    m = re.search(r'(\d+)\.\s+atk_n9_voice_changer\.output', line)
                    if m:
                        node_id = m.group(1)
                        subprocess.run(["wpctl", "set-default", node_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
        except Exception:
            pass

    def _disable_effect(self):
        vc_out = "atk_n9_voice_changer.output:capture_MONO"
        mic_cap = f"{self.mic_node}:capture_MONO" if self.mic_node else None

        # Restore original connections for intercepted applications
        for dest in list(self.intercepted_links):
            subprocess.run(["pw-link", "-d", vc_out, dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if mic_cap:
                subprocess.run(["pw-link", mic_cap, dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.intercepted_links.clear()
        self._stop_process()

        # Restore hardware microphone as default audio source
        if self.mic_node:
            try:
                out = subprocess.check_output(["wpctl", "status"], text=True, timeout=1.0)
                for line in out.splitlines():
                    if "ATK N9" in line and ("Mono" in line or "capture" in line) and "Audio/Source" not in line and "Analog Stereo" not in line:
                        m = re.search(r'(\d+)\.\s+.*ATK N9', line)
                        if m:
                            node_id = m.group(1)
                            subprocess.run(["wpctl", "set-default", node_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            break
            except Exception:
                pass

    def _stop_process(self):
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait(timeout=0.5)
            except Exception:
                try:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                except Exception:
                    pass
            self.process = None

    def cleanup(self):
        """Clean up on application exit."""
        self._disable_effect()
        self.current_effect_id = -1
