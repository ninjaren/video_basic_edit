"""
背景執行緒包裝器,避免匯出影片(耗時的 FFmpeg 子行程)阻塞主視窗的使用者介面。

此類別屬於 UI 層,負責將 io 層的 VideoExporter 包裝進 QThread,
io 層本身不依賴 Qt,維持低耦合。
"""

from PySide6.QtCore import QThread, Signal

from src.core.video_clip import VideoClip
from src.io.video_exporter import VideoExporter


class ExportWorker(QThread):
    """在背景執行緒呼叫 VideoExporter,完成或失敗時透過訊號通知主執行緒。"""

    export_finished = Signal(bool, str)

    def __init__(self, clip: VideoClip, output_path: str) -> None:
        super().__init__()
        self._clip = clip
        self._output_path = output_path
        self._exporter = VideoExporter()

    def run(self) -> None:
        """執行緒進入點:呼叫匯出邏輯,將結果(成功/錯誤訊息)以訊號回報。"""
        try:
            self._exporter.export(self._clip, self._output_path)
        except RuntimeError as error:
            self.export_finished.emit(False, str(error))
        else:
            self.export_finished.emit(True, "")
