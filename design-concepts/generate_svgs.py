#!/usr/bin/env python3
"""
Generates 5 distinct high-fidelity SVG mockups representing 5 UI design languages
for the ATK Neptune N9 Linux Control Center.
"""

import os

OUTPUT_DIR = "/home/excalibur/Workspace/projects/atk-linux-driver/design-concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. APEX PRO STUDIO (Modern Pro-Audio Esports)
# ------------------------------------------------------------------------------
svg_apex = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660" style="background:#08090D; font-family:'Inter', system-ui, sans-serif;">
  <defs>
    <linearGradient id="apex-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0E1017"/>
      <stop offset="100%" stop-color="#090A0F"/>
    </linearGradient>
    <linearGradient id="apex-cyan-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00D2FF"/>
      <stop offset="100%" stop-color="#00F5A0"/>
    </linearGradient>
    <linearGradient id="apex-curve-fill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00D2FF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#00D2FF" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="apex-active-nav" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="rgba(0, 210, 255, 0.22)"/>
      <stop offset="100%" stop-color="rgba(0, 210, 255, 0.02)"/>
    </linearGradient>
    <filter id="apex-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Window Container -->
  <rect x="0" y="0" width="1000" height="660" rx="14" fill="url(#apex-bg)" stroke="#1F2433" stroke-width="1.5"/>

  <!-- Top Bar -->
  <rect x="0" y="0" width="1000" height="58" rx="14" fill="#11131C"/>
  <rect x="0" y="44" width="1000" height="14" fill="#11131C"/>
  <line x1="0" y1="58" x2="1000" y2="58" stroke="#1D2232" stroke-width="1"/>

  <!-- Brand Title -->
  <text x="28" y="36" font-size="18" fill="#00D2FF">🎧</text>
  <text x="56" y="35" font-size="15" font-weight="900" fill="#FFFFFF" letter-spacing="1.5">ATK NEPTUNE N9</text>
  <rect x="200" y="21" width="76" height="20" rx="10" fill="#1A2030" stroke="#00D2FF" stroke-width="0.8"/>
  <text x="212" y="34" font-size="10" font-weight="700" fill="#00D2FF" letter-spacing="1">ESPORTS</text>

  <!-- Top Status / Telemetry -->
  <!-- RF Status Pill -->
  <rect x="730" y="18" width="115" height="26" rx="13" fill="#151824" stroke="#252B3D"/>
  <circle cx="745" cy="31" r="4" fill="#00F5A0" filter="url(#apex-glow)"/>
  <text x="756" y="35" font-size="11" font-weight="700" fill="#C5CADB">2.4G LINKED</text>

  <!-- Battery Pill -->
  <rect x="855" y="18" width="115" height="26" rx="13" fill="#151824" stroke="#252B3D"/>
  <rect x="866" y="24" width="28" height="14" rx="3" fill="#0E1017" stroke="#363E56"/>
  <rect x="868" y="26" width="20" height="10" rx="1.5" fill="url(#apex-cyan-grad)"/>
  <rect x="894" y="28" width="2" height="6" rx="1" fill="#363E56"/>
  <text x="906" y="35" font-size="12" font-weight="800" fill="#FFFFFF">84%</text>

  <!-- Sidebar -->
  <rect x="0" y="58" width="210" height="602" fill="#0F1118"/>
  <line x1="210" y1="58" x2="210" y2="660" stroke="#1D2232" stroke-width="1"/>

  <!-- Nav Items -->
  <!-- Nav 1: Dashboard (Active) -->
  <rect x="14" y="80" width="182" height="42" rx="10" fill="url(#apex-active-nav)"/>
  <rect x="14" y="80" width="3.5" height="42" rx="1.5" fill="#00D2FF"/>
  <text x="32" y="106" font-size="14" fill="#00D2FF">⚡</text>
  <text x="54" y="106" font-size="13" font-weight="700" fill="#00D2FF">Dashboard</text>

  <!-- Nav 2: Equalizer -->
  <text x="32" y="148" font-size="14" fill="#757D94">🎚️</text>
  <text x="54" y="148" font-size="13" font-weight="600" fill="#8890A6">Equalizer Studio</text>

  <!-- Nav 3: Microphone -->
  <text x="32" y="190" font-size="14" fill="#757D94">🎙️</text>
  <text x="54" y="190" font-size="13" font-weight="600" fill="#8890A6">Microphone &amp; Mic</text>

  <!-- Nav 4: Audio FX -->
  <text x="32" y="232" font-size="14" fill="#757D94">🌐</text>
  <text x="54" y="232" font-size="13" font-weight="600" fill="#8890A6">Spatial 7.1 FX</text>

  <!-- Nav 5: Settings -->
  <text x="32" y="274" font-size="14" fill="#757D94">⚙️</text>
  <text x="54" y="274" font-size="13" font-weight="600" fill="#8890A6">App Settings</text>

  <!-- Device Firmware Info at bottom sidebar -->
  <rect x="16" y="580" width="178" height="62" rx="10" fill="#141722" stroke="#1E2333"/>
  <text x="28" y="602" font-size="11" font-weight="700" fill="#FFFFFF">ATK N9 Ultra v1.0.8</text>
  <text x="28" y="622" font-size="10" fill="#6A728A">CDC-ACM: /dev/ttyACM0</text>
  <circle cx="176" cy="611" r="3.5" fill="#00F5A0"/>

  <!-- Main Content Area -->
  <!-- Card 1: 10-Band Parametric EQ Curve Card -->
  <rect x="234" y="78" width="742" height="260" rx="14" fill="#141620" stroke="#1F2538"/>
  <text x="254" y="106" font-size="14" font-weight="800" fill="#FFFFFF" letter-spacing="0.5">10-BAND DSP PARAMETRIC EQUALIZER</text>
  <text x="254" y="124" font-size="11" fill="#757D94">Hardware DSP Studio Engine with Sub-Millisecond Accuracy</text>

  <!-- Presets Pills -->
  <g transform="translate(620, 94)">
    <rect x="0" y="0" width="60" height="24" rx="6" fill="#1A1E2C" stroke="#2B3248"/>
    <text x="14" y="16" font-size="11" font-weight="600" fill="#8890A6">FLAT</text>
    <rect x="68" y="0" width="80" height="24" rx="6" fill="url(#apex-cyan-grad)"/>
    <text x="78" y="16" font-size="11" font-weight="800" fill="#0B0C10">FPS - CS2</text>
    <rect x="156" y="0" width="90" height="24" rx="6" fill="#1A1E2C" stroke="#2B3248"/>
    <text x="166" y="16" font-size="11" font-weight="600" fill="#8890A6">VALORANT</text>
  </g>

  <!-- Curve Canvas Area -->
  <rect x="254" y="140" width="702" height="120" rx="10" fill="#0C0E14" stroke="#1B2030"/>
  <!-- Grid Lines -->
  <line x1="284" y1="160" x2="936" y2="160" stroke="#161B29" stroke-dasharray="3,3"/>
  <text x="264" y="164" font-size="9" fill="#586178">+12dB</text>
  <line x1="284" y1="200" x2="936" y2="200" stroke="#222A3F"/>
  <text x="268" y="204" font-size="9" font-weight="700" fill="#00D2FF">0dB</text>
  <line x1="284" y1="240" x2="936" y2="240" stroke="#161B29" stroke-dasharray="3,3"/>
  <text x="265" y="244" font-size="9" fill="#586178">-12dB</text>

  <!-- Bezier Path Area Fill -->
  <path d="M 290 200 C 340 180, 400 160, 480 185 C 550 210, 620 220, 700 170 C 780 140, 850 155, 930 190 L 930 200 L 290 200 Z" fill="url(#apex-curve-fill)"/>
  <!-- Smooth Bezier Line -->
  <path d="M 290 200 C 340 180, 400 160, 480 185 C 550 210, 620 220, 700 170 C 780 140, 850 155, 930 190" fill="none" stroke="#00D2FF" stroke-width="2.5" filter="url(#apex-glow)"/>

  <!-- Nodes -->
  <circle cx="290" cy="200" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="380" cy="172" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="480" cy="185" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="580" cy="214" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="700" cy="170" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="810" cy="144" r="5" fill="#00F5A0" stroke="#FFFFFF" stroke-width="2" filter="url(#apex-glow)"/>
  <circle cx="930" cy="190" r="4" fill="#00D2FF" stroke="#FFFFFF" stroke-width="1.5"/>

  <!-- Frequency Faders below canvas -->
  <g transform="translate(254, 275)" font-size="9" fill="#757D94" text-anchor="middle">
    <text x="36" y="14">31Hz</text>
    <text x="106" y="14">62Hz</text>
    <text x="176" y="14">125Hz</text>
    <text x="246" y="14">250Hz</text>
    <text x="316" y="14">500Hz</text>
    <text x="386" y="14">1kHz</text>
    <text x="456" y="14">2kHz</text>
    <text x="526" y="14">4kHz</text>
    <text x="596" y="14">8kHz</text>
    <text x="666" y="14">16kHz</text>
  </g>
  <g transform="translate(254, 300)">
    <rect x="16" y="10" width="40" height="20" rx="5" fill="#1C2130"/>
    <text x="36" y="24" font-size="10" font-weight="700" fill="#00D2FF" text-anchor="middle">0dB</text>
    <rect x="86" y="10" width="40" height="20" rx="5" fill="#1C2130"/>
    <text x="106" y="24" font-size="10" font-weight="700" fill="#00D2FF" text-anchor="middle">+3dB</text>
    <rect x="576" y="10" width="40" height="20" rx="5" fill="#1C2130"/>
    <text x="596" y="24" font-size="10" font-weight="700" fill="#00F5A0" text-anchor="middle">+6dB</text>
  </g>

  <!-- Bottom Row: Card 2 (Mic & Sidetone) & Card 3 (Spatial 7.1) -->
  <!-- Card 2: Microphone & Sidetone -->
  <rect x="234" y="356" width="360" height="280" rx="14" fill="#141620" stroke="#1F2538"/>
  <text x="254" y="384" font-size="14" font-weight="800" fill="#FFFFFF">MICROPHONE &amp; SIDETONE</text>
  <text x="254" y="402" font-size="11" fill="#757D94">Hardware Input Gain &amp; Zero-Latency Monitor</text>

  <!-- Mic Gain Slider -->
  <text x="254" y="435" font-size="12" font-weight="600" fill="#C5CADB">Microphone Gain</text>
  <text x="550" y="435" font-size="12" font-weight="800" fill="#00D2FF">85%</text>
  <rect x="254" y="445" width="320" height="8" rx="4" fill="#0E1017"/>
  <rect x="254" y="445" width="272" height="8" rx="4" fill="url(#apex-cyan-grad)"/>
  <circle cx="526" cy="449" r="8" fill="#FFFFFF" filter="url(#apex-glow)"/>

  <!-- VU Meter Bar -->
  <text x="254" y="480" font-size="10" font-weight="700" fill="#6A728A">LIVE PIPEWIRE LEVEL</text>
  <g transform="translate(254, 488)">
    <rect x="0" y="0" width="320" height="10" rx="5" fill="#0E1017"/>
    <!-- LED segments -->
    <rect x="2" y="2" width="160" height="6" rx="2" fill="#00F5A0"/>
    <rect x="164" y="2" width="60" height="6" rx="2" fill="#FFAA00"/>
    <rect x="226" y="2" width="20" height="6" rx="2" fill="#FF3366"/>
  </g>

  <!-- Hardware Sidetone -->
  <line x1="254" y1="520" x2="574" y2="520" stroke="#1B2030"/>
  <text x="254" y="546" font-size="12" font-weight="600" fill="#C5CADB">Zero-Latency Sidetone</text>
  <!-- Pill switch (ON) -->
  <rect x="524" y="534" width="50" height="22" rx="11" fill="#00D2FF"/>
  <circle cx="560" cy="545" r="8" fill="#0B0C10"/>

  <text x="254" y="582" font-size="12" font-weight="600" fill="#C5CADB">Monitor Volume</text>
  <text x="550" y="582" font-size="12" font-weight="800" fill="#00D2FF">60%</text>
  <rect x="254" y="594" width="320" height="6" rx="3" fill="#0E1017"/>
  <rect x="254" y="594" width="192" height="6" rx="3" fill="#00D2FF"/>
  <circle cx="446" cy="597" r="7" fill="#FFFFFF"/>

  <!-- Card 3: 7.1 Virtual Spatial Surround -->
  <rect x="614" y="356" width="362" height="280" rx="14" fill="#141620" stroke="#1F2538"/>
  <text x="634" y="384" font-size="14" font-weight="800" fill="#FFFFFF">7.1 SPATIAL SURROUND</text>
  <text x="634" y="402" font-size="11" fill="#757D94">Hardware 360° Positional Sound Stage</text>

  <!-- Switch -->
  <rect x="906" y="374" width="50" height="22" rx="11" fill="#00F5A0"/>
  <circle cx="942" cy="385" r="8" fill="#0B0C10"/>

  <!-- Radar Graphic -->
  <g transform="translate(795, 515)">
    <!-- Concentric radar circles -->
    <circle cx="0" cy="0" r="75" fill="none" stroke="#1E2538" stroke-width="1"/>
    <circle cx="0" cy="0" r="50" fill="none" stroke="#252F48" stroke-width="1" stroke-dasharray="4,4"/>
    <circle cx="0" cy="0" r="25" fill="#181D2B" stroke="#00D2FF" stroke-width="1.5"/>
    <text x="0" y="5" font-size="14" text-anchor="middle" fill="#FFFFFF">👤</text>

    <!-- 8 Speaker Nodes -->
    <!-- FL --> <circle cx="-42" cy="-42" r="6" fill="#00D2FF" filter="url(#apex-glow)"/><text x="-54" y="-48" font-size="9" fill="#00D2FF">FL</text>
    <!-- C  --> <circle cx="0" cy="-60" r="6" fill="#00F5A0" filter="url(#apex-glow)"/><text x="0" y="-70" font-size="9" fill="#00F5A0" text-anchor="middle">C</text>
    <!-- FR --> <circle cx="42" cy="-42" r="6" fill="#00D2FF" filter="url(#apex-glow)"/><text x="54" y="-48" font-size="9" fill="#00D2FF">FR</text>
    <!-- SL --> <circle cx="-60" cy="0" r="5" fill="#00D2FF"/><text x="-75" y="4" font-size="9" fill="#757D94">SL</text>
    <!-- SR --> <circle cx="60" cy="0" r="5" fill="#00D2FF"/><text x="75" y="4" font-size="9" fill="#757D94">SR</text>
    <!-- RL --> <circle cx="-42" cy="42" r="5" fill="#00D2FF"/><text x="-54" y="56" font-size="9" fill="#757D94">RL</text>
    <!-- RR --> <circle cx="42" cy="42" r="5" fill="#00D2FF"/><text x="54" y="56" font-size="9" fill="#757D94">RR</text>
    <!-- SUB --> <circle cx="0" cy="60" r="7" fill="#FFAA00" filter="url(#apex-glow)"/><text x="0" y="75" font-size="9" fill="#FFAA00" text-anchor="middle">LFE</text>
  </g>
  <text x="795" y="618" font-size="11" font-weight="700" fill="#00F5A0" text-anchor="middle">SPATIAL ENGINE ENGAGED</text>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "1_apex_pro_studio.svg"), "w") as f:
    f.write(svg_apex)

print("Generated 1_apex_pro_studio.svg")

# ------------------------------------------------------------------------------
# 2. NORDIC PRECISION (Teenage Engineering & High-Tech Minimal)
# ------------------------------------------------------------------------------
svg_nordic = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660" style="background:#0F0F12; font-family:'JetBrains Mono', 'Fira Code', 'Courier New', monospace;">
  <!-- Window Container -->
  <rect x="0" y="0" width="1000" height="660" rx="4" fill="#121215" stroke="#25252B" stroke-width="1"/>

  <!-- Top Bar: Industrial Precision Grid Header -->
  <rect x="0" y="0" width="1000" height="52" fill="#17171C"/>
  <line x1="0" y1="52" x2="1000" y2="52" stroke="#282830" stroke-width="1"/>

  <!-- Brand Title -->
  <rect x="24" y="16" width="20" height="20" rx="2" fill="#FF5500"/>
  <text x="34" y="31" font-size="12" font-weight="900" fill="#000000" text-anchor="middle">N9</text>
  <text x="56" y="31" font-size="13" font-weight="800" fill="#FFFFFF" letter-spacing="2">ATK // NEPTUNE_N9</text>
  <text x="230" y="31" font-size="11" fill="#70707D">[REV. PRO_ULTRA]</text>

  <!-- Technical Telemetry Top Right -->
  <g transform="translate(640, 16)" font-size="11">
    <rect x="0" y="0" width="100" height="22" rx="2" fill="#1E1E24" stroke="#33333E"/>
    <text x="10" y="15" fill="#A0A0B0">RF: </text>
    <text x="36" y="15" font-weight="800" fill="#FF5500">2.4G_OK</text>

    <rect x="112" y="0" width="100" height="22" rx="2" fill="#1E1E24" stroke="#33333E"/>
    <text x="122" y="15" fill="#A0A0B0">BATT: </text>
    <text x="162" y="15" font-weight="800" fill="#FFFFFF">84%</text>

    <rect x="224" y="0" width="110" height="22" rx="2" fill="#1E1E24" stroke="#33333E"/>
    <text x="234" y="15" fill="#A0A0B0">RATE: </text>
    <text x="274" y="15" font-weight="800" fill="#FFFFFF">48kHz</text>
  </g>

  <!-- Sidebar -->
  <rect x="0" y="52" width="210" height="608" fill="#141418"/>
  <line x1="210" y1="52" x2="210" y2="660" stroke="#282830" stroke-width="1"/>

  <!-- Nav Items (Numbered, stark, high technical density) -->
  <g transform="translate(14, 76)">
    <!-- 01 DASHBOARD (Active) -->
    <rect x="0" y="0" width="182" height="38" rx="2" fill="#1F1F26" stroke="#FF5500" stroke-width="1"/>
    <text x="12" y="24" font-size="11" font-weight="800" fill="#FF5500">01</text>
    <text x="38" y="24" font-size="11" font-weight="700" fill="#FFFFFF" letter-spacing="1">DASHBOARD</text>

    <!-- 02 EQUALIZER -->
    <rect x="0" y="46" width="182" height="38" rx="2" fill="#17171C" stroke="#25252D"/>
    <text x="12" y="70" font-size="11" font-weight="800" fill="#6A6A78">02</text>
    <text x="38" y="70" font-size="11" font-weight="600" fill="#9090A0" letter-spacing="1">EQ MATRIX</text>

    <!-- 03 MICROPHONE -->
    <rect x="0" y="92" width="182" height="38" rx="2" fill="#17171C" stroke="#25252D"/>
    <text x="12" y="116" font-size="11" font-weight="800" fill="#6A6A78">03</text>
    <text x="38" y="116" font-size="11" font-weight="600" fill="#9090A0" letter-spacing="1">AUDIO INPUT</text>

    <!-- 04 SPATIAL -->
    <rect x="0" y="138" width="182" height="38" rx="2" fill="#17171C" stroke="#25252D"/>
    <text x="12" y="162" font-size="11" font-weight="800" fill="#6A6A78">04</text>
    <text x="38" y="162" font-size="11" font-weight="600" fill="#9090A0" letter-spacing="1">SPATIAL 7.1</text>

    <!-- 05 CONFIG -->
    <rect x="0" y="184" width="182" height="38" rx="2" fill="#17171C" stroke="#25252D"/>
    <text x="12" y="208" font-size="11" font-weight="800" fill="#6A6A78">05</text>
    <text x="38" y="208" font-size="11" font-weight="600" fill="#9090A0" letter-spacing="1">SYS SETTINGS</text>
  </g>

  <!-- Technical Spec Block Bottom Left -->
  <rect x="14" y="550" width="182" height="88" rx="2" fill="#16161B" stroke="#24242C"/>
  <text x="24" y="572" font-size="9" fill="#757585">DEVICE ID: 0x248A</text>
  <text x="24" y="590" font-size="9" fill="#757585">ENDPOINT: /dev/ttyACM0</text>
  <text x="24" y="608" font-size="9" fill="#757585">LATENCY: &lt;1.8 ms</text>
  <text x="24" y="626" font-size="9" font-weight="800" fill="#FF5500">[STATUS: SYNCED]</text>

  <!-- Main Area -->
  <!-- Card 1: 10-Band Stepped Equalizer Grid -->
  <rect x="234" y="74" width="742" height="268" rx="2" fill="#16161B" stroke="#292933"/>
  <text x="254" y="100" font-size="12" font-weight="800" fill="#FFFFFF" letter-spacing="1.5">BLOCK_01 // 10-BAND PARAMETRIC DSP MATRIX</text>
  <text x="690" y="100" font-size="11" fill="#FF5500">[PROFILE: FPS_ESPORTS_V1]</text>

  <!-- Technical Grid Canvas -->
  <rect x="254" y="116" width="702" height="130" fill="#111114" stroke="#262630"/>
  <!-- Grid Dots & Hairlines -->
  <line x1="254" y1="181" x2="956" y2="181" stroke="#353545" stroke-width="1"/>
  <text x="264" y="177" font-size="9" fill="#888898">0.0 dB (REF)</text>
  <line x1="254" y1="140" x2="956" y2="140" stroke="#1D1D26" stroke-dasharray="2,4"/>
  <text x="264" y="136" font-size="9" fill="#555565">+12.0 dB</text>
  <line x1="254" y1="222" x2="956" y2="222" stroke="#1D1D26" stroke-dasharray="2,4"/>
  <text x="264" y="218" font-size="9" fill="#555565">-12.0 dB</text>

  <!-- Stepped Orange Line -->
  <polyline points="290,181 350,165 410,150 470,181 530,205 590,210 650,175 720,135 790,135 880,181" fill="none" stroke="#FF5500" stroke-width="2"/>
  <!-- Square technical nodes -->
  <rect x="286" y="177" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="346" y="161" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="406" y="146" width="8" height="8" fill="#FF5500"/>
  <rect x="466" y="177" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="526" y="201" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="586" y="206" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="646" y="171" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>
  <rect x="716" y="131" width="8" height="8" fill="#FF5500"/>
  <rect x="786" y="131" width="8" height="8" fill="#FF5500"/>
  <rect x="876" y="177" width="8" height="8" fill="#111114" stroke="#FF5500" stroke-width="1.5"/>

  <!-- Fader readouts -->
  <g transform="translate(254, 260)" font-size="10" fill="#FFFFFF">
    <text x="36" y="16" text-anchor="middle" fill="#888898">31</text>
    <text x="36" y="32" text-anchor="middle">0dB</text>

    <text x="106" y="16" text-anchor="middle" fill="#888898">62</text>
    <text x="106" y="32" text-anchor="middle">+2dB</text>

    <text x="176" y="16" text-anchor="middle" fill="#888898">125</text>
    <text x="176" y="32" text-anchor="middle" fill="#FF5500">+4dB</text>

    <text x="246" y="16" text-anchor="middle" fill="#888898">250</text>
    <text x="246" y="32" text-anchor="middle">0dB</text>

    <text x="316" y="16" text-anchor="middle" fill="#888898">500</text>
    <text x="316" y="32" text-anchor="middle">-3dB</text>

    <text x="386" y="16" text-anchor="middle" fill="#888898">1k</text>
    <text x="386" y="32" text-anchor="middle">-4dB</text>

    <text x="456" y="16" text-anchor="middle" fill="#888898">2k</text>
    <text x="456" y="32" text-anchor="middle">+1dB</text>

    <text x="526" y="16" text-anchor="middle" fill="#888898">4k</text>
    <text x="526" y="32" text-anchor="middle" fill="#FF5500">+6dB</text>

    <text x="596" y="16" text-anchor="middle" fill="#888898">8k</text>
    <text x="596" y="32" text-anchor="middle" fill="#FF5500">+6dB</text>

    <text x="666" y="16" text-anchor="middle" fill="#888898">16k</text>
    <text x="666" y="32" text-anchor="middle">0dB</text>
  </g>

  <!-- Bottom Row: Card 2 (Mic Array) & Card 3 (Spatial Matrix) -->
  <!-- Card 2: Audio Input Module -->
  <rect x="234" y="362" width="360" height="274" rx="2" fill="#16161B" stroke="#292933"/>
  <text x="254" y="390" font-size="12" font-weight="800" fill="#FFFFFF" letter-spacing="1">BLOCK_02 // AUDIO_INPUT_MONITOR</text>

  <!-- Technical Stepped Gain Fader -->
  <text x="254" y="424" font-size="11" fill="#888898">ANALOG_GAIN_INDEX: [85 / 100]</text>
  <rect x="254" y="434" width="320" height="4" fill="#242430"/>
  <rect x="254" y="434" width="272" height="4" fill="#FF5500"/>
  <rect x="522" y="428" width="8" height="16" fill="#FFFFFF"/>

  <!-- Raw dBFS Peak Meter -->
  <text x="254" y="474" font-size="10" fill="#888898">PEAK_LEVEL_dBFS [-60 ... 0]</text>
  <rect x="254" y="484" width="320" height="12" fill="#101014" stroke="#252530"/>
  <g transform="translate(256, 486)">
    <!-- Discrete blocks -->
    <rect x="0" y="0" width="8" height="8" fill="#555566"/>
    <rect x="10" y="0" width="8" height="8" fill="#555566"/>
    <rect x="20" y="0" width="8" height="8" fill="#555566"/>
    <rect x="30" y="0" width="8" height="8" fill="#555566"/>
    <rect x="40" y="0" width="8" height="8" fill="#555566"/>
    <rect x="50" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="60" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="70" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="80" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="90" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="100" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="110" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="120" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="130" y="0" width="8" height="8" fill="#FF5500"/>
    <rect x="140" y="0" width="8" height="8" fill="#FF5500"/>
  </g>

  <!-- Hardware Sidetone -->
  <rect x="254" y="520" width="320" height="42" fill="#121216" stroke="#282834"/>
  <text x="268" y="546" font-size="11" fill="#FFFFFF">SIDETONE: [ENGAGED]</text>
  <rect x="490" y="530" width="70" height="22" fill="#FF5500"/>
  <text x="525" y="545" font-size="10" font-weight="900" fill="#000000" text-anchor="middle">ACTIVE</text>

  <text x="254" y="590" font-size="11" fill="#888898">MONITOR_GAIN: 60%</text>
  <rect x="254" y="600" width="320" height="4" fill="#242430"/>
  <rect x="254" y="600" width="192" height="4" fill="#FFFFFF"/>
  <rect x="442" y="594" width="8" height="16" fill="#FF5500"/>

  <!-- Card 3: Spatial Processor Matrix -->
  <rect x="614" y="362" width="362" height="274" rx="2" fill="#16161B" stroke="#292933"/>
  <text x="634" y="390" font-size="12" font-weight="800" fill="#FFFFFF" letter-spacing="1">BLOCK_03 // SPATIAL_DSP_MATRIX</text>

  <!-- Polar Matrix Graph -->
  <g transform="translate(795, 495)">
    <!-- Concentric Technical Rings -->
    <circle cx="0" cy="0" r="70" fill="none" stroke="#292938" stroke-width="1"/>
    <circle cx="0" cy="0" r="45" fill="none" stroke="#20202C" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="-75" y1="0" x2="75" y2="0" stroke="#292938"/>
    <line x1="0" y1="-75" x2="0" y2="75" stroke="#292938"/>

    <!-- Channel Markers -->
    <rect x="-4" y="-4" width="8" height="8" fill="#FFFFFF"/>
    <rect x="-45" y="-45" width="8" height="8" fill="#FF5500"/><text x="-56" y="-50" font-size="8" fill="#FF5500">CH_1</text>
    <rect x="37" y="-45" width="8" height="8" fill="#FF5500"/><text x="48" y="-50" font-size="8" fill="#FF5500">CH_2</text>
    <rect x="-4" y="-64" width="8" height="8" fill="#FF5500"/><text x="8" y="-60" font-size="8" fill="#FF5500">CENTER</text>
    <rect x="-64" y="-4" width="8" height="8" fill="#888898"/><text x="-76" y="16" font-size="8" fill="#888898">SUR_L</text>
    <rect x="56" y="-4" width="8" height="8" fill="#888898"/><text x="66" y="16" font-size="8" fill="#888898">SUR_R</text>
  </g>

  <rect x="634" y="590" width="322" height="30" fill="#111114" stroke="#292935"/>
  <text x="795" y="610" font-size="10" font-weight="800" fill="#FF5500" text-anchor="middle">&gt;&gt; VIRTUAL_7.1_ENGINE: RUNNING &lt;&lt;</text>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "2_nordic_precision.svg"), "w") as f:
    f.write(svg_nordic)

print("Generated 2_nordic_precision.svg")

# ------------------------------------------------------------------------------
# 3. CYBER-HUD (Tactical Cockpit & Sci-Fi Espor)
# ------------------------------------------------------------------------------
svg_cyber = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660" style="background:#05070B; font-family:'Inter', system-ui, sans-serif;">
  <defs>
    <linearGradient id="cyber-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#FF2E63"/>
    </linearGradient>
    <linearGradient id="cyber-glow-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(0, 240, 255, 0.15)"/>
      <stop offset="100%" stop-color="rgba(255, 46, 99, 0.0)"/>
    </linearGradient>
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Chamfered Window Container -->
  <polygon points="0,0 970,0 1000,30 1000,660 30,660 0,630" fill="#090C14" stroke="#1A263D" stroke-width="1.5"/>

  <!-- Top Bar -->
  <polygon points="0,0 970,0 1000,30 1000,56 0,56" fill="#0D121F"/>
  <line x1="0" y1="56" x2="1000" y2="56" stroke="#00F0FF" stroke-width="1.2" stroke-opacity="0.6"/>

  <!-- Chamfered Brand Badge -->
  <polygon points="20,12 180,12 195,44 20,44" fill="#141E33" stroke="#00F0FF" stroke-width="1"/>
  <text x="32" y="32" font-size="13" font-weight="900" fill="#00F0FF" letter-spacing="2">/// ATK NEPTUNE</text>
  <text x="146" y="32" font-size="11" font-weight="900" fill="#FF2E63">N9</text>

  <!-- HUD Telemetry Badges (Hex / Cut) -->
  <g transform="translate(680, 14)">
    <polygon points="0,0 120,0 130,26 10,26" fill="#111A2C" stroke="#00F0FF" stroke-width="1"/>
    <circle cx="22" cy="13" r="4" fill="#00F0FF" filter="url(#neon-glow)"/>
    <text x="34" y="17" font-size="10" font-weight="800" fill="#FFFFFF" letter-spacing="1">LINK: 2.4G SECURE</text>

    <polygon points="145,0 285,0 295,26 155,26" fill="#111A2C" stroke="#FF2E63" stroke-width="1"/>
    <text x="175" y="17" font-size="10" font-weight="900" fill="#FF2E63" letter-spacing="1">PWR: 84% [ONLINE]</text>
  </g>

  <!-- Sidebar -->
  <polygon points="0,56 210,56 210,660 30,660 0,630" fill="#0B0F1A"/>
  <line x1="210" y1="56" x2="210" y2="660" stroke="#162238" stroke-width="1"/>

  <!-- Tactical Nav Buttons -->
  <g transform="translate(14, 76)">
    <!-- Active Nav Tab -->
    <polygon points="0,0 170,0 182,38 0,38" fill="url(#cyber-glow-bg)" stroke="#00F0FF" stroke-width="1.2"/>
    <line x1="0" y1="0" x2="0" y2="38" stroke="#00F0FF" stroke-width="4"/>
    <text x="24" y="24" font-size="11" font-weight="900" fill="#00F0FF" letter-spacing="1.5">&gt; TACTICAL RADAR</text>

    <!-- Nav 2 -->
    <polygon points="0,48 170,48 182,86 0,86" fill="#0F1524" stroke="#1D2A44" stroke-width="1"/>
    <text x="24" y="72" font-size="11" font-weight="700" fill="#889BB8" letter-spacing="1">&gt; FREQ WARPER (EQ)</text>

    <!-- Nav 3 -->
    <polygon points="0,96 170,96 182,134 0,134" fill="#0F1524" stroke="#1D2A44" stroke-width="1"/>
    <text x="24" y="120" font-size="11" font-weight="700" fill="#889BB8" letter-spacing="1">&gt; COMMS ARRAY</text>

    <!-- Nav 4 -->
    <polygon points="0,144 170,144 182,182 0,182" fill="#0F1524" stroke="#1D2A44" stroke-width="1"/>
    <text x="24" y="168" font-size="11" font-weight="700" fill="#889BB8" letter-spacing="1">&gt; DSP EFFECT MATRIX</text>

    <!-- Nav 5 -->
    <polygon points="0,192 170,192 182,230 0,230" fill="#0F1524" stroke="#1D2A44" stroke-width="1"/>
    <text x="24" y="216" font-size="11" font-weight="700" fill="#889BB8" letter-spacing="1">&gt; CORE SYSTEMS</text>
  </g>

  <!-- HUD Corner Crosshairs & Tech Decals -->
  <text x="24" y="580" font-size="9" fill="#00F0FF" letter-spacing="1">TACTICAL AUDIO DRIVER</text>
  <text x="24" y="600" font-size="9" fill="#586E94">SYS://LINUX_NATIVE_ACM0</text>
  <text x="24" y="620" font-size="9" fill="#FF2E63">MODULE ENGAGED</text>

  <!-- Main Area -->
  <!-- Card 1: Freq Warper (EQ) -->
  <polygon points="234,74 960,74 976,90 976,334 234,334" fill="#0E1322" stroke="#1A2845" stroke-width="1.2"/>
  <text x="254" y="104" font-size="13" font-weight="900" fill="#00F0FF" letter-spacing="2">/// HARDWARE FREQUENCY WARPING MATRIX</text>

  <!-- Tactical Presets -->
  <g transform="translate(620, 88)">
    <polygon points="0,0 90,0 100,24 0,24" fill="#FF2E63"/>
    <text x="14" y="16" font-size="10" font-weight="900" fill="#FFFFFF">CS2 COMBAT</text>

    <polygon points="110,0 210,0 220,24 110,24" fill="#141C30" stroke="#00F0FF"/>
    <text x="124" y="16" font-size="10" font-weight="800" fill="#00F0FF">VALORANT</text>
  </g>

  <!-- Neon Grid Canvas -->
  <rect x="254" y="124" width="702" height="130" fill="#070A12" stroke="#17233D"/>
  <line x1="254" y1="189" x2="956" y2="189" stroke="#00F0FF" stroke-opacity="0.3"/>
  <line x1="254" y1="150" x2="956" y2="150" stroke="#141C30" stroke-dasharray="4,4"/>
  <line x1="254" y1="228" x2="956" y2="228" stroke="#141C30" stroke-dasharray="4,4"/>

  <!-- Jagged Tactical Frequency Path -->
  <path d="M 280 189 L 340 160 L 410 145 L 480 190 L 550 220 L 620 225 L 690 170 L 760 130 L 830 135 L 920 189" fill="none" stroke="#FF2E63" stroke-width="2.5" filter="url(#neon-glow)"/>
  <!-- Diamond Points -->
  <polygon points="280,185 284,189 280,193 276,189" fill="#00F0FF"/>
  <polygon points="340,156 344,160 340,164 336,160" fill="#00F0FF"/>
  <polygon points="410,141 414,145 410,149 406,145" fill="#FF2E63"/>
  <polygon points="760,126 764,130 760,134 756,130" fill="#00F0FF" filter="url(#neon-glow)"/>
  <polygon points="830,131 834,135 830,139 826,135" fill="#00F0FF" filter="url(#neon-glow)"/>

  <!-- Frequency Fader readouts -->
  <g transform="translate(254, 270)" font-size="9" font-weight="800" fill="#00F0FF" text-anchor="middle">
    <text x="36" y="14">31HZ</text>
    <text x="106" y="14">62HZ</text>
    <text x="176" y="14">125HZ</text>
    <text x="246" y="14">250HZ</text>
    <text x="316" y="14">500HZ</text>
    <text x="386" y="14">1KHZ</text>
    <text x="456" y="14">2KHZ</text>
    <text x="526" y="14">4KHZ</text>
    <text x="596" y="14">8KHZ</text>
    <text x="666" y="14">16KHZ</text>
  </g>
  <g transform="translate(254, 295)">
    <!-- Small Chamfered Indicators -->
    <polygon points="20,0 52,0 60,18 20,18" fill="#152035"/>
    <text x="38" y="13" font-size="10" font-weight="900" fill="#FFFFFF" text-anchor="middle">0dB</text>

    <polygon points="160,0 192,0 200,18 160,18" fill="#FF2E63"/>
    <text x="178" y="13" font-size="10" font-weight="900" fill="#FFFFFF" text-anchor="middle">+4dB</text>

    <polygon points="510,0 542,0 550,18 510,18" fill="#00F0FF"/>
    <text x="528" y="13" font-size="10" font-weight="900" fill="#05070B" text-anchor="middle">+6dB</text>
  </g>

  <!-- Bottom Row: Card 2 & Card 3 -->
  <!-- Card 2: Tactical Comms -->
  <polygon points="234,354 580,354 594,368 594,636 234,636" fill="#0E1322" stroke="#1A2845" stroke-width="1.2"/>
  <text x="254" y="384" font-size="13" font-weight="900" fill="#00F0FF" letter-spacing="1.5">/// COMMS INPUT CONTROLLER</text>

  <text x="254" y="420" font-size="11" font-weight="700" fill="#889BB8">TRANSMIT GAIN: 85%</text>
  <rect x="254" y="432" width="310" height="6" fill="#070A12"/>
  <rect x="254" y="432" width="263" height="6" fill="url(#cyber-grad)"/>
  <polygon points="517,428 523,435 517,442 511,435" fill="#00F0FF" filter="url(#neon-glow)"/>

  <!-- Audio Waveform / Gate Display -->
  <text x="254" y="470" font-size="10" font-weight="800" fill="#FF2E63">SPECTRAL GATE: OPEN</text>
  <rect x="254" y="480" width="310" height="24" fill="#080C14" stroke="#152136"/>
  <!-- Waveform spikes -->
  <g transform="translate(260, 492)" stroke="#00F0FF" stroke-width="2">
    <line x1="0" y1="-2" x2="0" y2="2"/>
    <line x1="8" y1="-6" x2="8" y2="6"/>
    <line x1="16" y1="-9" x2="16" y2="9" stroke="#FF2E63"/>
    <line x1="24" y1="-4" x2="24" y2="4"/>
    <line x1="32" y1="-1" x2="32" y2="1"/>
    <line x1="40" y1="-7" x2="40" y2="7"/>
    <line x1="48" y1="-10" x2="48" y2="10" stroke="#FF2E63"/>
    <line x1="56" y1="-5" x2="56" y2="5"/>
    <line x1="64" y1="-3" x2="64" y2="3"/>
  </g>

  <!-- Hardware Sidetone -->
  <text x="254" y="540" font-size="11" font-weight="700" fill="#889BB8">SIDETONE RADAR LOOPBACK</text>
  <polygon points="494,526 564,526 574,548 504,548" fill="#00F0FF"/>
  <text x="534" y="542" font-size="10" font-weight="900" fill="#000000" text-anchor="middle">ACTIVE</text>

  <rect x="254" y="574" width="310" height="6" fill="#070A12"/>
  <rect x="254" y="574" width="186" height="6" fill="#00F0FF"/>
  <polygon points="440,570 446,577 440,584 434,577" fill="#FFFFFF"/>

  <!-- Card 3: 360 Tactical Sonar Radar -->
  <polygon points="614,354 960,354 976,368 976,636 614,636" fill="#0E1322" stroke="#1A2845" stroke-width="1.2"/>
  <text x="634" y="384" font-size="13" font-weight="900" fill="#00F0FF" letter-spacing="1.5">/// 360° SONAR SPATIAL RADAR</text>

  <!-- Radar Area -->
  <g transform="translate(795, 510)">
    <!-- Rotating crosshairs & rings -->
    <circle cx="0" cy="0" r="80" fill="none" stroke="#19253D" stroke-width="1"/>
    <circle cx="0" cy="0" r="50" fill="none" stroke="#00F0FF" stroke-opacity="0.2" stroke-dasharray="6,4"/>
    <circle cx="0" cy="0" r="20" fill="#090E17" stroke="#FF2E63" stroke-width="1.5"/>

    <!-- Sonar Sweep Sector -->
    <path d="M 0 0 L 56 -56 A 80 80 0 0 1 80 0 Z" fill="url(#cyber-glow-bg)"/>

    <!-- Target Dots with Rings -->
    <!-- Front Left Enemy -->
    <circle cx="-42" cy="-42" r="5" fill="#FF2E63" filter="url(#neon-glow)"/>
    <circle cx="-42" cy="-42" r="9" fill="none" stroke="#FF2E63" stroke-width="1"/>
    <text x="-56" y="-54" font-size="8" font-weight="900" fill="#FF2E63">TARGET_01</text>

    <!-- Rear Right Sound Blip -->
    <circle cx="48" cy="48" r="4" fill="#00F0FF" filter="url(#neon-glow)"/>
    <text x="56" y="60" font-size="8" font-weight="900" fill="#00F0FF">FOOTSTEPS</text>
  </g>
  <text x="795" y="620" font-size="10" font-weight="900" fill="#00F0FF" text-anchor="middle">&gt; SPATIAL POSITIONING ACTIVE &lt;</text>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "3_cyber_hud.svg"), "w") as f:
    f.write(svg_cyber)

print("Generated 3_cyber_hud.svg")

# ------------------------------------------------------------------------------
# 4. LIQUID GLASS & COSMIC DECK (Translucent, Ambient & Soft Glow)
# ------------------------------------------------------------------------------
svg_glass = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660" style="background:#090B14; font-family:'Inter', system-ui, sans-serif;">
  <defs>
    <!-- Background Ambient Glow Blobs -->
    <radialGradient id="purple-blob" cx="20%" cy="20%" r="40%">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#7C3AED" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="cyan-blob" cx="80%" cy="70%" r="50%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="glass-card-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="rgba(30, 38, 64, 0.65)"/>
      <stop offset="100%" stop-color="rgba(15, 20, 36, 0.45)"/>
    </linearGradient>
    <linearGradient id="cosmic-pill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <filter id="soft-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Ambient Light Orbs -->
  <rect x="0" y="0" width="1000" height="660" fill="#090B14"/>
  <rect x="0" y="0" width="1000" height="660" fill="url(#purple-blob)"/>
  <rect x="0" y="0" width="1000" height="660" fill="url(#cyan-blob)"/>

  <!-- Window Container with frosted rim -->
  <rect x="0" y="0" width="1000" height="660" rx="20" fill="none" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5"/>

  <!-- Top Floating Header Bar -->
  <rect x="20" y="16" width="960" height="54" rx="18" fill="url(#glass-card-bg)" stroke="rgba(255, 255, 255, 0.15)"/>

  <!-- Brand -->
  <text x="44" y="48" font-size="18">🎧</text>
  <text x="74" y="48" font-size="15" font-weight="800" fill="#FFFFFF" letter-spacing="1">ATK Neptune N9</text>
  <rect x="210" y="32" width="70" height="22" rx="11" fill="rgba(139, 92, 246, 0.25)" stroke="#8B5CF6" stroke-width="0.8"/>
  <text x="224" y="47" font-size="10" font-weight="700" fill="#C4B5FD">STUDIO</text>

  <!-- Top Status Glass Badges -->
  <rect x="715" y="28" width="120" height="30" rx="15" fill="rgba(255, 255, 255, 0.08)" stroke="rgba(255, 255, 255, 0.15)"/>
  <circle cx="732" cy="43" r="4.5" fill="#10B981" filter="url(#soft-glow)"/>
  <text x="744" y="47" font-size="11" font-weight="600" fill="#E2E8F0">2.4GHz Link</text>

  <rect x="846" y="28" width="114" height="30" rx="15" fill="rgba(255, 255, 255, 0.08)" stroke="rgba(255, 255, 255, 0.15)"/>
  <rect x="858" y="36" width="24" height="13" rx="3" fill="none" stroke="#A78BFA"/>
  <rect x="860" y="38" width="16" height="9" rx="1.5" fill="url(#cosmic-pill)"/>
  <text x="890" y="47" font-size="12" font-weight="700" fill="#FFFFFF">84%</text>

  <!-- Left Floating Dock Sidebar -->
  <rect x="20" y="86" width="190" height="554" rx="18" fill="url(#glass-card-bg)" stroke="rgba(255, 255, 255, 0.12)"/>

  <!-- Dock Nav Items -->
  <g transform="translate(32, 106)">
    <!-- Active Item with Cosmic Pill -->
    <rect x="0" y="0" width="166" height="44" rx="14" fill="url(#cosmic-pill)" filter="url(#soft-glow)"/>
    <text x="18" y="28" font-size="14" fill="#FFFFFF">✨</text>
    <text x="42" y="27" font-size="13" font-weight="700" fill="#FFFFFF">Dashboard</text>

    <!-- Nav 2 -->
    <rect x="0" y="56" width="166" height="44" rx="14" fill="rgba(255, 255, 255, 0.04)"/>
    <text x="18" y="84" font-size="14" fill="#A1A1AA">🎛️</text>
    <text x="42" y="83" font-size="13" font-weight="500" fill="#D4D4D8">Equalizer</text>

    <!-- Nav 3 -->
    <rect x="0" y="112" width="166" height="44" rx="14" fill="rgba(255, 255, 255, 0.04)"/>
    <text x="18" y="140" font-size="14" fill="#A1A1AA">🎙️</text>
    <text x="42" y="139" font-size="13" font-weight="500" fill="#D4D4D8">Microphone</text>

    <!-- Nav 4 -->
    <rect x="0" y="168" width="166" height="44" rx="14" fill="rgba(255, 255, 255, 0.04)"/>
    <text x="18" y="196" font-size="14" fill="#A1A1AA">🌌</text>
    <text x="42" y="195" font-size="13" font-weight="500" fill="#D4D4D8">Cosmic 7.1</text>

    <!-- Nav 5 -->
    <rect x="0" y="224" width="166" height="44" rx="14" fill="rgba(255, 255, 255, 0.04)"/>
    <text x="18" y="252" font-size="14" fill="#A1A1AA">⚙️</text>
    <text x="42" y="251" font-size="13" font-weight="500" fill="#D4D4D8">Preferences</text>
  </g>

  <!-- Main Content Cards -->
  <!-- Card 1: Liquid EQ Curve -->
  <rect x="226" y="86" width="754" height="260" rx="18" fill="url(#glass-card-bg)" stroke="rgba(255, 255, 255, 0.14)"/>
  <text x="250" y="116" font-size="15" font-weight="700" fill="#FFFFFF">Acoustic Equalizer</text>
  <text x="250" y="134" font-size="12" fill="#94A3B8">Liquid 10-band DSP parametric response curve</text>

  <!-- Presets Pills -->
  <g transform="translate(680, 102)">
    <rect x="0" y="0" width="70" height="26" rx="13" fill="rgba(255,255,255,0.08)"/>
    <text x="18" y="17" font-size="11" font-weight="600" fill="#CBD5E1">Natural</text>
    <rect x="78" y="0" width="80" height="26" rx="13" fill="url(#cosmic-pill)"/>
    <text x="96" y="17" font-size="11" font-weight="700" fill="#FFFFFF">Gaming</text>
    <rect x="166" y="0" width="80" height="26" rx="13" fill="rgba(255,255,255,0.08)"/>
    <text x="182" y="17" font-size="11" font-weight="600" fill="#CBD5E1">Immersive</text>
  </g>

  <!-- Organic Wave Area in Glass -->
  <rect x="250" y="152" width="706" height="114" rx="14" fill="rgba(10, 14, 26, 0.5)" stroke="rgba(255, 255, 255, 0.08)"/>
  <!-- Smooth Liquid Curve -->
  <path d="M 280 210 C 340 185, 400 160, 480 185 C 560 215, 640 225, 720 170 C 800 135, 870 150, 930 200" fill="none" stroke="url(#cosmic-pill)" stroke-width="3" filter="url(#soft-glow)"/>
  <!-- Soft Nodes -->
  <circle cx="280" cy="210" r="5" fill="#FFFFFF" filter="url(#soft-glow)"/>
  <circle cx="480" cy="185" r="5" fill="#FFFFFF" filter="url(#soft-glow)"/>
  <circle cx="720" cy="170" r="5" fill="#FFFFFF" filter="url(#soft-glow)"/>
  <circle cx="800" cy="144" r="7" fill="#06B6D4" stroke="#FFFFFF" stroke-width="2" filter="url(#soft-glow)"/>
  <circle cx="930" cy="200" r="5" fill="#FFFFFF" filter="url(#soft-glow)"/>

  <!-- Frequency Faders below -->
  <g transform="translate(250, 280)" font-size="10" fill="#94A3B8" text-anchor="middle">
    <text x="35" y="16">31Hz</text>
    <text x="105" y="16">62Hz</text>
    <text x="175" y="16">125Hz</text>
    <text x="245" y="16">250Hz</text>
    <text x="315" y="16">500Hz</text>
    <text x="385" y="16">1kHz</text>
    <text x="455" y="16">2kHz</text>
    <text x="525" y="16">4kHz</text>
    <text x="595" y="16">8kHz</text>
    <text x="665" y="16">16kHz</text>
  </g>

  <!-- Bottom Row: Card 2 & Card 3 -->
  <!-- Card 2: Voice & Mic -->
  <rect x="226" y="362" width="365" height="278" rx="18" fill="url(#glass-card-bg)" stroke="rgba(255, 255, 255, 0.14)"/>
  <text x="250" y="394" font-size="15" font-weight="700" fill="#FFFFFF">Studio Microphone</text>
  <text x="250" y="412" font-size="12" fill="#94A3B8">Input gain &amp; real-time monitor blend</text>

  <text x="250" y="446" font-size="13" font-weight="600" fill="#E2E8F0">Input Level (85%)</text>
  <rect x="250" y="458" width="315" height="10" rx="5" fill="rgba(0,0,0,0.4)"/>
  <rect x="250" y="458" width="267" height="10" rx="5" fill="url(#cosmic-pill)"/>
  <circle cx="517" cy="463" r="8" fill="#FFFFFF" filter="url(#soft-glow)"/>

  <!-- Ambient Fluid VU Meter -->
  <text x="250" y="500" font-size="11" font-weight="600" fill="#94A3B8">Live Voice Aura</text>
  <rect x="250" y="510" width="315" height="16" rx="8" fill="rgba(0,0,0,0.4)"/>
  <rect x="252" y="512" width="210" height="12" rx="6" fill="url(#cosmic-pill)" filter="url(#soft-glow)"/>

  <!-- Sidetone Pill -->
  <text x="250" y="562" font-size="13" font-weight="600" fill="#E2E8F0">Sidetone Loop</text>
  <!-- Apple/Fluid style pill toggle (ON) -->
  <rect x="505" y="548" width="56" height="26" rx="13" fill="url(#cosmic-pill)" filter="url(#soft-glow)"/>
  <circle cx="545" cy="561" r="10" fill="#FFFFFF"/>

  <text x="250" y="598" font-size="12" fill="#94A3B8">Blend 60%</text>
  <rect x="250" y="608" width="315" height="8" rx="4" fill="rgba(0,0,0,0.4)"/>
  <rect x="250" y="608" width="189" height="8" rx="4" fill="#06B6D4"/>
  <circle cx="439" cy="612" r="7" fill="#FFFFFF"/>

  <!-- Card 3: Cosmic Spatial Sphere -->
  <rect x="611" y="362" width="369" height="278" rx="18" fill="url(#glass-card-bg)" stroke="rgba(255, 255, 255, 0.14)"/>
  <text x="635" y="394" font-size="15" font-weight="700" fill="#FFFFFF">Cosmic 7.1 Spatial</text>
  <text x="635" y="412" font-size="12" fill="#94A3B8">Acoustic space depth engine</text>

  <!-- Ambient Orb Visualizer -->
  <g transform="translate(795, 510)">
    <circle cx="0" cy="0" r="75" fill="none" stroke="rgba(255,255,255,0.1)"/>
    <circle cx="0" cy="0" r="55" fill="none" stroke="url(#cosmic-pill)" stroke-width="2" filter="url(#soft-glow)"/>
    <circle cx="0" cy="0" r="30" fill="url(#glass-card-bg)" stroke="rgba(255,255,255,0.2)"/>
    <text x="0" y="7" font-size="20" text-anchor="middle">🎧</text>

    <!-- Glowing Speaker Points -->
    <circle cx="-38" cy="-38" r="6" fill="#8B5CF6" filter="url(#soft-glow)"/>
    <circle cx="0" cy="-55" r="6" fill="#06B6D4" filter="url(#soft-glow)"/>
    <circle cx="38" cy="-38" r="6" fill="#8B5CF6" filter="url(#soft-glow)"/>
    <circle cx="-55" cy="0" r="5" fill="#A78BFA"/>
    <circle cx="55" cy="0" r="5" fill="#A78BFA"/>
    <circle cx="-38" cy="38" r="5" fill="#06B6D4"/>
    <circle cx="38" cy="38" r="5" fill="#06B6D4"/>
  </g>
  <text x="795" y="618" font-size="12" font-weight="600" fill="#C4B5FD" text-anchor="middle">Virtual Surround Enabled</text>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "4_liquid_glass.svg"), "w") as f:
    f.write(svg_glass)

print("Generated 4_liquid_glass.svg")

# ------------------------------------------------------------------------------
# 5. NATIVE GNOME / LIBADWAITA DARK (Standard Linux Integration)
# ------------------------------------------------------------------------------
svg_gnome = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" width="1000" height="660" style="background:#1E1E1E; font-family:'Cantarell', 'Ubuntu', system-ui, sans-serif;">
  <!-- Window Container -->
  <rect x="0" y="0" width="1000" height="660" rx="12" fill="#1E1E1E" stroke="#303030" stroke-width="1"/>

  <!-- GNOME AdwHeaderBar -->
  <rect x="0" y="0" width="1000" height="48" rx="12" fill="#242424"/>
  <rect x="0" y="36" width="1000" height="12" fill="#242424"/>
  <line x1="0" y1="48" x2="1000" y2="48" stroke="#333333" stroke-width="1"/>

  <!-- Window Controls (GNOME Close Button Right) -->
  <circle cx="975" cy="24" r="9" fill="#363636"/>
  <text x="975" y="27" font-size="10" font-weight="700" fill="#A0A0A0" text-anchor="middle">✕</text>

  <!-- Title Center -->
  <text x="500" y="29" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">ATK Neptune N9</text>

  <!-- Headerbar Left Status Pill -->
  <rect x="18" y="13" width="126" height="24" rx="12" fill="#303030"/>
  <circle cx="30" cy="25" r="4" fill="#2EC27E"/>
  <text x="42" y="29" font-size="11" font-weight="600" fill="#D0D0D0">Connected</text>

  <!-- Headerbar Battery Right -->
  <rect x="830" y="13" width="120" height="24" rx="12" fill="#303030"/>
  <text x="842" y="29" font-size="12">🔋</text>
  <text x="862" y="29" font-size="11" font-weight="600" fill="#FFFFFF">84% Battery</text>

  <!-- Split View: Sidebar (AdwNavigationSplitView) -->
  <rect x="0" y="48" width="220" height="612" fill="#242424"/>
  <line x1="220" y1="48" x2="220" y2="660" stroke="#333333" stroke-width="1"/>

  <!-- GNOME Sidebar List Items -->
  <g transform="translate(12, 64)">
    <!-- Dashboard (Active Row) -->
    <rect x="0" y="0" width="196" height="38" rx="8" fill="#3584E4"/>
    <text x="14" y="24" font-size="14" fill="#FFFFFF">📊</text>
    <text x="40" y="24" font-size="13" font-weight="600" fill="#FFFFFF">Overview</text>

    <!-- Equalizer -->
    <rect x="0" y="44" width="196" height="38" rx="8" fill="transparent"/>
    <text x="14" y="68" font-size="14" fill="#A0A0A0">🎚️</text>
    <text x="40" y="68" font-size="13" font-weight="500" fill="#D0D0D0">Equalizer</text>

    <!-- Microphone -->
    <rect x="0" y="88" width="196" height="38" rx="8" fill="transparent"/>
    <text x="14" y="112" font-size="14" fill="#A0A0A0">🎙️</text>
    <text x="40" y="112" font-size="13" font-weight="500" fill="#D0D0D0">Microphone</text>

    <!-- Spatial Surround -->
    <rect x="0" y="132" width="196" height="38" rx="8" fill="transparent"/>
    <text x="14" y="156" font-size="14" fill="#A0A0A0">🌐</text>
    <text x="40" y="156" font-size="13" font-weight="500" fill="#D0D0D0">Surround Audio</text>

    <!-- Settings -->
    <rect x="0" y="176" width="196" height="38" rx="8" fill="transparent"/>
    <text x="14" y="200" font-size="14" fill="#A0A0A0">⚙️</text>
    <text x="40" y="200" font-size="13" font-weight="500" fill="#D0D0D0">Preferences</text>
  </g>

  <!-- Main Content Area: AdwPreferencesPage with Grouped Rows -->
  <!-- Group 1: Equalizer Preferences Group -->
  <text x="246" y="80" font-size="12" font-weight="700" fill="#9A9996" letter-spacing="0.5">EQUALIZER PRESETS</text>

  <!-- Segmented Button Row (AdwViewSwitcher) -->
  <rect x="246" y="94" width="720" height="36" rx="8" fill="#282828" stroke="#383838"/>
  <rect x="426" y="96" width="180" height="32" rx="6" fill="#383838"/>
  <text x="336" y="116" font-size="12" font-weight="600" fill="#A0A0A0" text-anchor="middle">Flat</text>
  <text x="516" y="116" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">CS2 Competitive</text>
  <text x="696" y="116" font-size="12" font-weight="600" fill="#A0A0A0" text-anchor="middle">Valorant</text>
  <text x="876" y="116" font-size="12" font-weight="600" fill="#A0A0A0" text-anchor="middle">Bass Boost</text>

  <!-- Clean Grouped Card for EQ Curve -->
  <rect x="246" y="142" width="720" height="150" rx="10" fill="#282828" stroke="#383838"/>
  <!-- Minimalist Curve -->
  <line x1="270" y1="217" x2="940" y2="217" stroke="#383838"/>
  <path d="M 280 217 C 340 190, 420 170, 500 195 C 580 220, 660 230, 740 180 C 820 150, 880 160, 930 200" fill="none" stroke="#3584E4" stroke-width="2.5"/>
  <circle cx="280" cy="217" r="4" fill="#3584E4"/>
  <circle cx="500" cy="195" r="4" fill="#3584E4"/>
  <circle cx="740" cy="180" r="4" fill="#3584E4"/>
  <circle cx="820" cy="150" r="5" fill="#3584E4"/>
  <circle cx="930" cy="200" r="4" fill="#3584E4"/>

  <!-- Frequency Labels -->
  <g transform="translate(246, 266)" font-size="10" fill="#9A9996" text-anchor="middle">
    <text x="40" y="12">31Hz</text>
    <text x="115" y="12">62Hz</text>
    <text x="190" y="12">125Hz</text>
    <text x="265" y="12">250Hz</text>
    <text x="340" y="12">500Hz</text>
    <text x="415" y="12">1kHz</text>
    <text x="490" y="12">2kHz</text>
    <text x="565" y="12">4kHz</text>
    <text x="640" y="12">8kHz</text>
    <text x="680" y="12">16kHz</text>
  </g>

  <!-- Group 2: Microphone & Audio Settings (Grouped AdwActionRow) -->
  <text x="246" y="324" font-size="12" font-weight="700" fill="#9A9996" letter-spacing="0.5">AUDIO &amp; MICROPHONE</text>

  <!-- Grouped Container -->
  <rect x="246" y="338" width="720" height="294" rx="10" fill="#282828" stroke="#383838"/>

  <!-- Row 1: Microphone Gain -->
  <g transform="translate(266, 362)">
    <text x="0" y="14" font-size="13" font-weight="600" fill="#FFFFFF">Microphone Gain</text>
    <text x="0" y="30" font-size="11" fill="#9A9996">Hardware input sensitivity level</text>

    <!-- Slider Right -->
    <rect x="420" y="14" width="220" height="6" rx="3" fill="#383838"/>
    <rect x="420" y="14" width="187" height="6" rx="3" fill="#3584E4"/>
    <circle cx="607" cy="17" r="8" fill="#FFFFFF"/>
    <text x="655" y="20" font-size="12" font-weight="600" fill="#FFFFFF">85%</text>
  </g>
  <line x1="246" y1="410" x2="966" y2="410" stroke="#333333"/>

  <!-- Row 2: Live VU Meter Level -->
  <g transform="translate(266, 430)">
    <text x="0" y="14" font-size="13" font-weight="600" fill="#FFFFFF">Input Activity</text>
    <text x="0" y="30" font-size="11" fill="#9A9996">Real-time PipeWire audio monitor</text>

    <rect x="420" y="16" width="260" height="8" rx="4" fill="#383838"/>
    <rect x="420" y="16" width="170" height="8" rx="4" fill="#2EC27E"/>
  </g>
  <line x1="246" y1="478" x2="966" y2="478" stroke="#333333"/>

  <!-- Row 3: Hardware Sidetone Switch -->
  <g transform="translate(266, 498)">
    <text x="0" y="14" font-size="13" font-weight="600" fill="#FFFFFF">Hardware Sidetone</text>
    <text x="0" y="30" font-size="11" fill="#9A9996">Real-time zero-latency mic loopback to headset</text>

    <!-- GNOME Switch (ON) -->
    <rect x="626" y="8" width="54" height="28" rx="14" fill="#3584E4"/>
    <circle cx="666" cy="22" r="11" fill="#FFFFFF"/>
  </g>
  <line x1="246" y1="546" x2="966" y2="546" stroke="#333333"/>

  <!-- Row 4: Virtual 7.1 Surround -->
  <g transform="translate(266, 566)">
    <text x="0" y="14" font-size="13" font-weight="600" fill="#FFFFFF">Virtual 7.1 Spatial Audio</text>
    <text x="0" y="30" font-size="11" fill="#9A9996">Positional 360-degree virtual sound stage</text>

    <!-- GNOME Switch (ON) -->
    <rect x="626" y="8" width="54" height="28" rx="14" fill="#3584E4"/>
    <circle cx="666" cy="22" r="11" fill="#FFFFFF"/>
  </g>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "5_native_gnome.svg"), "w") as f:
    f.write(svg_gnome)

print("Generated 5_native_gnome.svg")
