"""
Nordic Precision Industrial Design Theme for ATK Neptune N9.
Inspired by Teenage Engineering (TX-6 / OP-1) and Wooting (Wootility v5).
Palette: Matte Carbon (#111114, #17171C), Technical Slate (#1E1E26), Safety Orange (#FF5500), Monospace Accents.
"""

MAIN_STYLESHEET = """
/* Global Window */
QWidget {
    background-color: #111114;
    color: #FFFFFF;
    font-family: 'Inter', 'Segoe UI', 'Ubuntu', 'Cantarell', sans-serif;
    font-size: 12px;
    outline: none;
}

/* Technical Monospace Tokens */
.mono-text {
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    border: none;
    background: #141418;
    width: 4px;
    border-radius: 0px;
}
QScrollBar::handle:vertical {
    background: #2B2B36;
    border-radius: 0px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #FF5500;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Header Top Bar */
QFrame#topbar {
    background-color: #141418;
    border-bottom: 1px solid #24242D;
}

/* Sidebar Container */
QFrame#sidebar {
    background-color: #141418;
    border-right: 1px solid #24242D;
}

/* Sidebar Navigation Buttons */
QPushButton.nav-btn {
    background-color: transparent;
    color: #8C8E9A;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 2px;
    padding: 10px 14px;
    text-align: left;
    font-size: 11px;
    font-weight: 700;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.5px;
}
QPushButton.nav-btn:hover {
    background-color: #1C1C24;
    color: #FFFFFF;
}
QPushButton.nav-btn:checked {
    background-color: #1F1F2A;
    color: #FFFFFF;
    border-left: 3px solid #FF5500;
    font-weight: 800;
}

/* Cards & Containers - Industrial Sharp */
QFrame.card {
    background-color: #16161B;
    border: 1px solid #282834;
    border-radius: 3px;
    padding: 16px;
}
QFrame.card:hover {
    border: 1px solid #363646;
}

QFrame.sub-card {
    background-color: #1B1B22;
    border: 1px solid #2C2C3A;
    border-radius: 2px;
    padding: 12px 14px;
}
QFrame.sub-card:hover {
    border: 1px solid #3B3B4E;
}

/* Typography */
QLabel.card-title {
    font-size: 12px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 1px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}
QLabel.card-subtitle {
    font-size: 11px;
    color: #7D7F8E;
    line-height: 1.3;
}

/* Preset Pill Buttons - Stepped Industrial */
QPushButton.preset-btn {
    background-color: #1B1B24;
    color: #9295A6;
    border: 1px solid #2A2A38;
    border-radius: 2px;
    padding: 6px 12px;
    font-weight: 700;
    font-size: 10px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.5px;
}
QPushButton.preset-btn:hover {
    background-color: #242432;
    color: #FFFFFF;
    border-color: #FF5500;
}
QPushButton.preset-btn:checked {
    background-color: #FF5500;
    color: #000000;
    border: 1px solid #FF5500;
    font-weight: 800;
}

/* Action Buttons */
QPushButton.action-btn {
    background-color: #FF5500;
    color: #000000;
    border: none;
    border-radius: 2px;
    padding: 8px 16px;
    font-weight: 800;
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.8px;
}
QPushButton.action-btn:hover {
    background-color: #FF6E24;
}
QPushButton.action-btn:pressed {
    background-color: #D94800;
}

/* Secondary Button */
QPushButton.secondary-btn {
    background-color: #1E1E28;
    color: #A2A5B8;
    border: 1px solid #2B2B3A;
    border-radius: 2px;
    padding: 7px 14px;
    font-weight: 700;
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}
QPushButton.secondary-btn:hover {
    background-color: #262634;
    color: #FFFFFF;
    border-color: #3E3E52;
}

/* Dangerous / Mute Switch Button */
QPushButton.mute-btn {
    background-color: #1A1A22;
    color: #8C8E9E;
    border: 1px solid #2C2C3C;
    border-radius: 2px;
    padding: 8px 14px;
    font-weight: 700;
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}
QPushButton.mute-btn:hover {
    background-color: #242430;
    color: #FFFFFF;
}
QPushButton.mute-btn:checked {
    background-color: rgba(255, 85, 0, 0.18);
    color: #FF5500;
    border: 1px solid #FF5500;
    font-weight: 800;
}

/* Sliders (Vertical - EQ) - Mechanical Faders */
QSlider::groove:vertical {
    background: #20202A;
    width: 4px;
    border-radius: 0px;
}
QSlider::sub-page:vertical {
    background: #20202A;
    border-radius: 0px;
}
QSlider::add-page:vertical {
    background: #FF5500;
    border-radius: 0px;
}
QSlider::handle:vertical {
    background: #FFFFFF;
    border: none;
    height: 8px;
    width: 18px;
    margin: 0 -7px;
    border-radius: 1px;
}
QSlider::handle:vertical:hover {
    background: #FF5500;
}

/* Sliders (Horizontal) - Stepped Track */
QSlider::groove:horizontal {
    background: #20202A;
    height: 4px;
    border-radius: 0px;
}
QSlider::sub-page:horizontal {
    background: #FF5500;
    border-radius: 0px;
}
QSlider::add-page:horizontal {
    background: #20202A;
    border-radius: 0px;
}
QSlider::handle:horizontal {
    background: #FFFFFF;
    border: none;
    width: 8px;
    height: 18px;
    margin: -7px 0;
    border-radius: 1px;
}
QSlider::handle:horizontal:hover {
    background: #FF5500;
}

/* Pill Badges - Industrial Telemetry */
QLabel.badge-connected {
    background-color: #1A1A24;
    color: #00F5A0;
    border: 1px solid #282838;
    border-radius: 2px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 700;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.5px;
}
QLabel.badge-disconnected {
    background-color: #1A1A24;
    color: #FF4B5C;
    border: 1px solid #282838;
    border-radius: 2px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 700;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.5px;
}

QLabel.badge-latency {
    background-color: #181822;
    color: #FF5500;
    border: 1px solid #2B2B3C;
    border-radius: 2px;
    padding: 3px 8px;
    font-size: 10px;
    font-weight: 800;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
    letter-spacing: 0.5px;
}

/* Bottom Status Bar */
QFrame#statusbar {
    background-color: #111114;
    border-top: 1px solid #20202A;
    color: #6C6F82;
    font-size: 10px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}

/* Combo Box (Language Selector etc.) */
QComboBox {
    background-color: #1A1A24;
    color: #FFFFFF;
    border: 1px solid #2C2C3C;
    border-radius: 2px;
    padding: 5px 12px;
    min-width: 140px;
    font-weight: 600;
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}
QComboBox:hover {
    border-color: #FF5500;
    background-color: #21212E;
}
QComboBox::drop-down {
    border: none;
    width: 22px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-top: 4px solid #FF5500;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #16161E;
    color: #FFFFFF;
    border: 1px solid #2C2C3C;
    border-radius: 2px;
    padding: 2px;
    selection-background-color: #FF5500;
    selection-color: #000000;
    font-family: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', 'Ubuntu Mono', monospace;
}

/* Checkbox */
QCheckBox {
    spacing: 8px;
    color: #FFFFFF;
    font-size: 12px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 2px;
    border: 1px solid #363648;
    background-color: #1A1A22;
}
QCheckBox::indicator:hover {
    border-color: #FF5500;
}
QCheckBox::indicator:checked {
    background-color: #FF5500;
    border-color: #FF5500;
}
"""
