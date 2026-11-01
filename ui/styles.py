"""
Ultra-Modern Gaming Peripheral Design Theme for ATK Neptune N9.
Inspired by modern SteelSeries GG/Sonar, Razer Synapse 4, and ATK Hub standards.
Palette: Deep Stealth Black (#0B0C0E, #13141B), Cyber Cyan (#00D2FF), Mint Green (#00F5A0).
"""

MAIN_STYLESHEET = """
/* Global Window */
QWidget {
    background-color: #0B0C0E;
    color: #FFFFFF;
    font-family: 'Inter', 'Segoe UI', 'Ubuntu', 'Cantarell', sans-serif;
    font-size: 13px;
    outline: none;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    border: none;
    background: #13141B;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #252836;
    border-radius: 3px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #00D2FF;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Header Top Bar */
QFrame#topbar {
    background-color: #0F1015;
    border-bottom: 1px solid #1C1E28;
}

/* Sidebar Container */
QFrame#sidebar {
    background-color: #0F1015;
    border-right: 1px solid #1C1E28;
}

/* Sidebar Navigation Buttons */
QPushButton.nav-btn {
    background-color: transparent;
    color: #8C90A2;
    border: none;
    border-radius: 10px;
    padding: 12px 18px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
}
QPushButton.nav-btn:hover {
    background-color: #171822;
    color: #FFFFFF;
}
QPushButton.nav-btn:checked {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 210, 255, 0.16), stop:1 rgba(0, 210, 255, 0.02));
    color: #00D2FF;
    border-left: 3px solid #00D2FF;
    font-weight: 700;
}

/* Cards & Containers */
QFrame.card {
    background-color: #13141B;
    border: 1px solid #1E202B;
    border-radius: 14px;
    padding: 18px;
}
QFrame.card:hover {
    border: 1px solid #282C3D;
}

QFrame.sub-card {
    background-color: #181924;
    border: 1px solid #222533;
    border-radius: 10px;
    padding: 14px 16px;
}
QFrame.sub-card:hover {
    border: 1px solid #2D3144;
}

/* Typography */
QLabel.card-title {
    font-size: 14px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 0.6px;
}
QLabel.card-subtitle {
    font-size: 12px;
    color: #72768A;
    line-height: 1.4;
}

/* Preset Pill Buttons */
QPushButton.preset-btn {
    background-color: #181924;
    color: #A0A5BA;
    border: 1px solid #252837;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton.preset-btn:hover {
    background-color: #212332;
    color: #FFFFFF;
    border-color: #00D2FF;
}
QPushButton.preset-btn:checked {
    background-color: #00D2FF;
    color: #080A0E;
    border: 1px solid #00D2FF;
    font-weight: 800;
}

/* Action Buttons */
QPushButton.action-btn {
    background-color: #00D2FF;
    color: #080A0E;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 0.3px;
}
QPushButton.action-btn:hover {
    background-color: #33DBFF;
}
QPushButton.action-btn:pressed {
    background-color: #00B4DC;
}

/* Secondary Button */
QPushButton.secondary-btn {
    background-color: #1F212D;
    color: #B2B6C8;
    border: 1px solid #2B2F40;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton.secondary-btn:hover {
    background-color: #272A3B;
    color: #FFFFFF;
    border-color: #3A3F55;
}

/* Dangerous / Mute Switch Button */
QPushButton.mute-btn {
    background-color: #1C1E29;
    color: #A2A6B8;
    border: 1px solid #2A2D3D;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 600;
}
QPushButton.mute-btn:hover {
    background-color: #242735;
    color: #FFFFFF;
}
QPushButton.mute-btn:checked {
    background-color: rgba(255, 51, 102, 0.16);
    color: #FF3366;
    border: 1px solid #FF3366;
    font-weight: 800;
}

/* Sliders (Vertical - EQ) */
QSlider::groove:vertical {
    background: #1D1F2A;
    width: 6px;
    border-radius: 3px;
}
QSlider::sub-page:vertical {
    background: #1D1F2A;
    border-radius: 3px;
}
QSlider::add-page:vertical {
    background: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 #0099FF, stop:1 #00E5FF);
    border-radius: 3px;
}
QSlider::handle:vertical {
    background: #FFFFFF;
    border: 2px solid #00D2FF;
    height: 16px;
    width: 16px;
    margin: 0 -5px;
    border-radius: 8px;
}
QSlider::handle:vertical:hover {
    background: #00D2FF;
    border-color: #FFFFFF;
}

/* Sliders (Horizontal) */
QSlider::groove:horizontal {
    background: #1D1F2A;
    height: 6px;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0099FF, stop:1 #00E5FF);
    border-radius: 3px;
}
QSlider::add-page:horizontal {
    background: #1D1F2A;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #FFFFFF;
    border: 2px solid #00D2FF;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #00D2FF;
    border-color: #FFFFFF;
}

/* Pill Badges */
QLabel.badge-connected {
    background-color: rgba(0, 245, 160, 0.12);
    color: #00F5A0;
    border: 1px solid rgba(0, 245, 160, 0.35);
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}
QLabel.badge-disconnected {
    background-color: rgba(255, 51, 102, 0.12);
    color: #FF3366;
    border: 1px solid rgba(255, 51, 102, 0.35);
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

QLabel.badge-latency {
    background-color: rgba(0, 210, 255, 0.10);
    color: #00D2FF;
    border: 1px solid rgba(0, 210, 255, 0.25);
    border-radius: 12px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
}

/* Bottom Status Bar */
QFrame#statusbar {
    background-color: #0B0C0E;
    border-top: 1px solid #181924;
    color: #616578;
    font-size: 11px;
}

/* Combo Box (Language Selector etc.) */
QComboBox {
    background-color: #181924;
    color: #FFFFFF;
    border: 1px solid #2B2F40;
    border-radius: 8px;
    padding: 6px 14px;
    min-width: 140px;
    font-weight: 600;
    font-size: 12px;
}
QComboBox:hover {
    border-color: #00D2FF;
    background-color: #212332;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #00D2FF;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #13141B;
    color: #FFFFFF;
    border: 1px solid #2B2F40;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: #00D2FF;
    selection-color: #0B0C0E;
}

"""
