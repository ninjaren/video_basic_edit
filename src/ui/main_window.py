"""應用程式主視窗,串接影片匯入、調整參數蒐集與預覽畫面更新的使用者互動流程。"""

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QWidget

from src.config import APP_NAME, SUPPORTED_VIDEO_EXTENSIONS
from src.core.pipeline import apply_adjustments
from src.core.video_clip import VideoClip
from src.io.video_reader import VideoReader
from src.ui.controls_panel import ControlsPanel
from src.ui.export_worker import ExportWorker
from src.ui.preview_widget import PreviewWidget
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """主視窗:組合預覽元件與控制面板,並處理兩者之間的資料流動。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1000, 650)

        self._clip: VideoClip | None = None
        self._reader: VideoReader | None = None
        self._export_worker: ExportWorker | None = None

        self._preview_widget = PreviewWidget()
        self._controls_panel = ControlsPanel()
        self._controls_panel.import_requested.connect(self._on_import_requested)
        self._controls_panel.adjustment_changed.connect(self._on_adjustment_changed)
        self._controls_panel.export_requested.connect(self._on_export_requested)

        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self._preview_widget, stretch=3)
        layout.addWidget(self._controls_panel, stretch=1)
        self.setCentralWidget(central_widget)

    def _on_import_requested(self) -> None:
        """使用者點擊「匯入影片」後,開啟檔案選擇對話框並載入影片。"""
        extension_filter = " ".join(f"*{ext}" for ext in SUPPORTED_VIDEO_EXTENSIONS)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇影片檔案", "", f"影片檔案 ({extension_filter})"
        )
        if not file_path:
            return

        try:
            self._reader = VideoReader(file_path)
            info = self._reader.read_info()
            self._clip = VideoClip(source_path=file_path, info=info)
        except IOError as error:
            logger.error("匯入影片失敗: %s", error)
            QMessageBox.critical(self, "匯入失敗", str(error))
            return

        self._controls_panel.show_video_info(info)
        self._refresh_preview()

    def _on_adjustment_changed(self) -> None:
        """使用者調整滑桿等控制項後,更新調整設定並重新產生預覽畫面。"""
        if self._clip is None:
            return
        self._clip.settings = self._controls_panel.current_settings()
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        """依目前的調整設定重新計算並顯示預覽畫面。"""
        if self._clip is None or self._reader is None:
            return
        frame = self._reader.read_frame_at(self._clip.settings.trim_start)
        adjusted_frame = apply_adjustments(frame, self._clip.settings)
        self._preview_widget.show_frame(adjusted_frame)

    def _on_export_requested(self) -> None:
        """使用者點擊「匯出影片」後,選擇輸出路徑並於背景執行緒開始匯出。"""
        if self._clip is None:
            return
        if self._export_worker is not None and self._export_worker.isRunning():
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "匯出影片", "", "MP4 影片 (*.mp4)")
        if not output_path:
            return

        self._clip.settings = self._controls_panel.current_settings()
        self._controls_panel.set_export_in_progress(True)
        logger.info("開始匯出影片至: %s", output_path)

        self._export_worker = ExportWorker(self._clip, output_path)
        self._export_worker.export_finished.connect(self._on_export_finished)
        self._export_worker.start()

    def _on_export_finished(self, success: bool, error_message: str) -> None:
        """匯出完成(成功或失敗)後,恢復介面狀態並顯示結果訊息。"""
        self._controls_panel.set_export_in_progress(False)
        if success:
            QMessageBox.information(self, "匯出完成", "影片已成功匯出。")
        else:
            logger.error("匯出失敗: %s", error_message)
            QMessageBox.critical(self, "匯出失敗", error_message)
