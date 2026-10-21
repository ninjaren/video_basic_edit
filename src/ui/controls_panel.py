"""
控制面板:提供影片匯入按鈕與剪切/旋轉/亮度/對比度/音量等調整控制項。

此元件只負責蒐集使用者輸入並發出訊號,不直接操作影片資料或呼叫
IO/effects 模組,由 MainWindow 負責串接,維持低耦合。
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.config import (
    BRIGHTNESS_DEFAULT,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    CONTRAST_DEFAULT,
    CONTRAST_MAX,
    CONTRAST_MIN,
    VOLUME_DEFAULT,
    VOLUME_MAX,
    VOLUME_MIN,
)
from src.core.video_clip import AdjustmentSettings, VideoInfo


class ControlsPanel(QWidget):
    """使用者調整影片參數的面板。"""

    import_requested = Signal()
    export_requested = Signal()
    adjustment_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._info_label = QLabel("尚未匯入影片")
        self._video_duration = 0.0

        self._import_button = QPushButton("匯入影片")
        self._import_button.clicked.connect(self.import_requested.emit)

        self._trim_start_spinbox = self._create_trim_spinbox()
        self._trim_start_spinbox.valueChanged.connect(self._on_trim_start_changed)

        self._trim_end_spinbox = self._create_trim_spinbox()
        self._trim_end_spinbox.valueChanged.connect(self._on_trim_end_changed)

        self._brightness_slider, brightness_row = self._create_slider_with_spinbox(
            BRIGHTNESS_MIN, BRIGHTNESS_MAX, BRIGHTNESS_DEFAULT
        )
        self._contrast_slider, contrast_row = self._create_slider_with_spinbox(
            CONTRAST_MIN, CONTRAST_MAX, CONTRAST_DEFAULT
        )
        self._volume_slider, volume_row = self._create_slider_with_spinbox(
            VOLUME_MIN, VOLUME_MAX, VOLUME_DEFAULT
        )

        self._mute_checkbox = QCheckBox("靜音")
        self._mute_checkbox.toggled.connect(self._emit_adjustment_changed)

        self._rotation_angle = 0
        self._rotate_button = QPushButton("旋轉 90°")
        self._rotate_button.clicked.connect(self._on_rotate_clicked)

        self._export_button = QPushButton("匯出影片")
        self._export_button.setEnabled(False)
        self._export_button.clicked.connect(self.export_requested.emit)

        self._export_status_label = QLabel("")

        layout = QVBoxLayout(self)
        layout.addWidget(self._import_button)
        layout.addWidget(self._info_label)
        layout.addWidget(QLabel("剪切起點"))
        layout.addWidget(self._trim_start_spinbox)
        layout.addWidget(QLabel("剪切終點"))
        layout.addWidget(self._trim_end_spinbox)
        layout.addWidget(QLabel("亮度"))
        layout.addWidget(brightness_row)
        layout.addWidget(QLabel("對比度"))
        layout.addWidget(contrast_row)
        layout.addWidget(QLabel("音量"))
        layout.addWidget(volume_row)
        layout.addWidget(self._mute_checkbox)
        layout.addWidget(self._rotate_button)
        layout.addWidget(self._export_button)
        layout.addWidget(self._export_status_label)
        layout.addStretch()

    def _create_trim_spinbox(self) -> QDoubleSpinBox:
        """建立剪切起點/終點用的數字輸入框,匯入影片前停用,匯入後才依影片長度設定範圍。"""
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(1)
        spinbox.setSuffix(" 秒")
        spinbox.setEnabled(False)
        return spinbox

    def _on_trim_start_changed(self, value: float) -> None:
        """剪切起點變更時,確保不超過終點(至少保留 0.1 秒的剪切範圍)。"""
        if value >= self._trim_end_spinbox.value():
            self._trim_end_spinbox.setValue(min(value + 0.1, self._trim_end_spinbox.maximum()))
        self.adjustment_changed.emit()

    def _on_trim_end_changed(self, value: float) -> None:
        """剪切終點變更時,確保不小於起點(至少保留 0.1 秒的剪切範圍)。"""
        if value <= self._trim_start_spinbox.value():
            self._trim_start_spinbox.setValue(max(value - 0.1, self._trim_start_spinbox.minimum()))
        self.adjustment_changed.emit()

    def _create_slider_with_spinbox(
        self, minimum: int, maximum: int, default: int
    ) -> tuple[QSlider, QWidget]:
        """
        建立「滑桿 + 數字輸入框」的組合,兩者數值互相同步。

        滑桿方便快速拖曳調整,數字輸入框則方便輸入精確數值,
        兩者透過 valueChanged 互相連動,僅滑桿的訊號轉發 adjustment_changed
        (輸入框變更會連動更新滑桿,進而觸發同一個轉發路徑,不需重複連接)。
        """
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(default)

        spinbox = QSpinBox()
        spinbox.setMinimum(minimum)
        spinbox.setMaximum(maximum)
        spinbox.setValue(default)

        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(self._emit_adjustment_changed)

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.addWidget(slider)
        row_layout.addWidget(spinbox)
        return slider, row

    def _emit_adjustment_changed(self, *_args) -> None:
        """
        統一轉發 adjustment_changed 訊號。

        QSlider.valueChanged 會帶出 int、QCheckBox.toggled 會帶出 bool,
        但 adjustment_changed 定義為零參數訊號,直接連接會因參數數量不符而
        連線失敗(PySide6 嚴格檢查訊號簽章),因此統一透過此方法轉發並忽略參數。
        """
        self.adjustment_changed.emit()

    def _on_rotate_clicked(self) -> None:
        """每點擊一次旋轉 90°,依 0 -> 90 -> 180 -> 270 -> 0 循環。"""
        self._rotation_angle = (self._rotation_angle + 90) % 360
        self.adjustment_changed.emit()

    def show_video_info(self, info: VideoInfo) -> None:
        """顯示匯入影片的基本資訊,並依影片長度重新設定剪切起點/終點的可選範圍。"""
        self._info_label.setText(
            f"解析度: {info.width}x{info.height}  FPS: {info.fps:.2f}  "
            f"長度: {info.duration:.1f} 秒  格式: {info.file_format}"
        )

        self._video_duration = info.duration
        for spinbox in (self._trim_start_spinbox, self._trim_end_spinbox):
            spinbox.blockSignals(True)
            spinbox.setRange(0.0, info.duration)
            spinbox.setEnabled(True)
            spinbox.blockSignals(False)
        self._trim_start_spinbox.setValue(0.0)
        self._trim_end_spinbox.setValue(info.duration)
        self._export_button.setEnabled(True)

    def set_export_in_progress(self, in_progress: bool) -> None:
        """切換匯出按鈕的可用狀態與狀態文字,避免使用者在匯出期間重複觸發。"""
        self._export_button.setEnabled(not in_progress)
        self._export_status_label.setText("匯出中,請稍候..." if in_progress else "")

    def current_settings(self) -> AdjustmentSettings:
        """彙整目前介面上的調整參數,回傳給呼叫端套用。"""
        return AdjustmentSettings(
            trim_start=self._trim_start_spinbox.value(),
            trim_end=self._trim_end_spinbox.value(),
            rotation=self._rotation_angle,
            brightness=self._brightness_slider.value(),
            contrast=self._contrast_slider.value(),
            volume=self._volume_slider.value(),
            muted=self._mute_checkbox.isChecked(),
        )
