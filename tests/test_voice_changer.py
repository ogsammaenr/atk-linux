"""
Unit test for VoiceChangerManager DSP filter and PipeWire routing.
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui.voice_changer import VoiceChangerManager, EFFECT_PRESETS

def test_voice_changer_lifecycle():
    print("Initializing VoiceChangerManager...")
    vc = VoiceChangerManager()
    
    # 1. Test config generation
    for eff_id, preset in EFFECT_PRESETS.items():
        conf = vc._generate_config(preset["pitch"], preset["buffer_size"])
        assert "libpipewire-module-filter-chain" in conf
        assert f'"Pitch shift" = {preset["pitch"]}' in conf
        print(f"Verified config generation for effect {eff_id} ({preset['name']})")

    # 2. Test enabling an effect
    print("Testing effect activation...")
    vc.set_effect(0) # Male
    assert vc.current_effect_id == 0
    time.sleep(0.5)

    # 3. Test switching effect
    print("Testing effect switch to Monster...")
    vc.set_effect(2) # Monster
    assert vc.current_effect_id == 2
    time.sleep(0.5)

    # 4. Test disabling effect
    print("Testing disabling effect...")
    vc.set_effect(-1)
    assert vc.current_effect_id == -1
    assert vc.process is None

    # 5. Cleanup
    vc.cleanup()
    print("VoiceChangerManager lifecycle test PASSED.")

if __name__ == "__main__":
    test_voice_changer_lifecycle()
