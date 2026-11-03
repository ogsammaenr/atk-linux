"""
Real-time Hardware & Software Microphone VU Meter for ATK Neptune N9.
Captures live PCM samples via QtMultimedia / PipeWire and displays an industrial dBFS LED meter.
"""

import struct
from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt6.QtMultimedia import QMediaDevices, QAudioSource, QAudioFormat

from ui.i18n import I18N


class VUMeterWidget(QWidget):
    """
    Precision live VU Meter with smoothed decay, peak hold, and hardware mute awareness.
    Styled according to Nordic Precision standards with discrete rectangular segments.
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedHeight(28)
        self.setMinimumWidth(200)

        self.is_muted = False
        self._monitoring = False
        self._level = 0.0          # Current smoothed level (0.0 to 1.0)
        self._peak_hold = 0.0      # Peak hold indicator (0.0 to 1.0)
        self._peak_hold_ticks = 0  # Hold duration counter

        # Audio capture objects
        self._audio_source: Optional[QAudioSource] = None
        self._io_device = None

        # Sample processor timer (~25 fps)
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self._process_audio_samples)

    def _select_input_device(self):
        """Find ATK Neptune N9 input device or fallback to system default."""
        inputs = QMediaDevices.audioInputs()
        for dev in inputs:
            desc = dev.description().lower()
            if "atk" in desc or "n9" in desc:
                return dev
        return QMediaDevices.defaultAudioInput()

    def start_monitoring(self):
        """Start capturing microphone stream."""
        if self._monitoring:
            return

        try:
            dev = self._select_input_device()
            if not dev or dev.isNull():
                return

            fmt = QAudioFormat()
            fmt.setSampleRate(48000)
            fmt.setChannelCount(1)
            fmt.setSampleFormat(QAudioFormat.SampleFormat.Int16)

            self._audio_source = QAudioSource(dev, fmt, self)
            self._audio_source.setBufferSize(4096)
            self._io_device = self._audio_source.start()

            self._monitoring = True
            self._timer.start()
        except Exception:
            self._monitoring = False

    def stop_monitoring(self):
        """Stop capturing and sleep audio thread."""
        self._timer.stop()
        if self._audio_source:
            try:
                self._audio_source.stop()
            except Exception:
                pass
            self._audio_source = None
            self._io_device = None

        self._monitoring = False
        self._level = 0.0
        self._peak_hold = 0.0
        self.update()

    def set_muted(self, muted: bool):
        """Update hardware mute state."""
        self.is_muted = muted
        if muted:
            self._level = 0.0
            self._peak_hold = 0.0
        self.update()

    def _process_audio_samples(self):
        """Read buffer and calculate RMS/Peak amplitude."""
        if not self._monitoring or not self._io_device or self.is_muted:
            self._level = max(0.0, self._level * 0.82)
            self._peak_hold = max(0.0, self._peak_hold - 0.04)
            self.update()
            return

        try:
            data = self._io_device.readAll().data()
            if data:
                count = len(data) // 2
                if count > 0:
                    samples = struct.unpack(f"<{count}h", data[:count * 2])
                    peak = max(abs(s) for s in samples) / 32768.0
                    peak = min(1.0, peak * 2.2)

                    if peak > self._level:
                        self._level = peak
                    else:
                        self._level = max(0.0, self._level * 0.85)
                else:
                    self._level = max(0.0, self._level * 0.85)
            else:
                self._level = max(0.0, self._level * 0.85)
        except Exception:
            self._level = max(0.0, self._level * 0.85)

        # Update peak hold
        if self._level >= self._peak_hold:
            self._peak_hold = self._level
            self._peak_hold_ticks = 12
        else:
            if self._peak_hold_ticks > 0:
                self._peak_hold_ticks -= 1
            else:
                self._peak_hold = max(0.0, self._peak_hold - 0.035)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())

        # Outer industrial frame with sharp 2px border
        bg_rect = QRectF(0, 0, w, h)
        painter.setPen(QPen(QColor("#262634"), 1.0))
        painter.setBrush(QBrush(QColor("#111114")))
        painter.drawRoundedRect(bg_rect, 2, 2)

        mono_font = QFont("JetBrains Mono", 9)
        mono_font.setStyleHint(QFont.StyleHint.Monospace)

        if self.is_muted:
            painter.setPen(QColor("#FF5500"))
            painter.setFont(mono_font)
            painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, f"[HARDWARE_MUTED]")
            return

        # Discrete Segment Meter layout
        text_width = 46.0
        meter_width = w - text_width - 16.0
        meter_x = 8.0
        meter_y = 5.0
        meter_h = h - 10.0

        num_segments = 24
        seg_spacing = 2.0
        seg_w = max(2.0, (meter_width - (num_segments - 1) * seg_spacing) / num_segments)

        active_count = int(self._level * num_segments)
        peak_seg = int(self._peak_hold * num_segments)

        for i in range(num_segments):
            seg_x = meter_x + i * (seg_w + seg_spacing)
            seg_rect = QRectF(seg_x, meter_y, seg_w, meter_h)

            ratio = i / float(num_segments)
            if ratio < 0.65:
                color = QColor("#8A8D9C") # Discrete Slate/Silver
            elif ratio < 0.85:
                color = QColor("#FFFFFF") # Stark White
            else:
                color = QColor("#FF5500") # Safety Orange Peak

            if i < active_count:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRoundedRect(seg_rect, 1, 1)
            elif i == peak_seg and self._peak_hold > 0.05:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#FF5500")))
                painter.drawRoundedRect(seg_rect, 1, 1)
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor("#1A1A22")))
                painter.drawRoundedRect(seg_rect, 1, 1)

        # Monospace Right side readout
        pct_val = int(self._level * 100)
        painter.setPen(QColor("#FF5500") if pct_val > 0 else QColor("#5E6278"))
        painter.setFont(mono_font)
        text_rect = QRectF(w - text_width - 6.0, 0, text_width, h)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{pct_val}%")
