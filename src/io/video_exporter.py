"""負責將調整後的影片匯出為檔案,封裝 FFmpeg 的呼叫細節。"""

import subprocess

from src.core.video_clip import VideoClip
from src.io.ffmpeg_command_builder import build_export_command
from src.utils.ffmpeg_utils import resolve_ffmpeg_path
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VideoExporter:
    """負責呼叫 FFmpeg,將 VideoClip 的調整設定套用後輸出成影片檔案。"""

    def __init__(self) -> None:
        self._ffmpeg_path = resolve_ffmpeg_path()

    def export(self, clip: VideoClip, output_path: str) -> None:
        """
        將 clip 的調整設定(剪切、旋轉、亮度/對比度、音量/靜音)套用後匯出至 output_path。

        失敗時統一拋出 RuntimeError,夾帶可供使用者理解的錯誤訊息,
        此為 IO 模組對外的系統邊界,呼叫端(UI 層)不需要了解 FFmpeg 的細節。
        """
        command = build_export_command(
            self._ffmpeg_path, clip.source_path, clip.settings, output_path
        )
        logger.info("執行匯出指令: %s", " ".join(command))

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
        except FileNotFoundError as error:
            raise RuntimeError(
                f"找不到 FFmpeg 執行檔({self._ffmpeg_path}),請確認已正確安裝或打包。"
            ) from error

        if result.returncode != 0:
            logger.error("FFmpeg 匯出失敗(結束碼 %s): %s", result.returncode, result.stderr)
            raise RuntimeError(f"匯出失敗,FFmpeg 回傳錯誤:\n{result.stderr[-1000:]}")

        logger.info("匯出完成: %s", output_path)
