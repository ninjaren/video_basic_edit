"""
處理 FFmpeg 執行檔路徑解析。

依技術選型.md的決定,FFmpeg 會在打包階段隨 .exe 一起發行,
但開發階段仍依賴開發者自行安裝的系統版 FFmpeg,因此需要依執行環境
(一般 Python 直接執行 / PyInstaller 打包後執行)回傳不同的路徑來源。
"""

import sys
from pathlib import Path


def resolve_ffmpeg_path() -> str:
    """
    回傳可用的 FFmpeg 執行檔路徑。

    打包成 .exe 後(sys.frozen 為 True),FFmpeg 會位於 PyInstaller 執行時
    解壓的暫存目錄(sys._MEIPASS)下的 ffmpeg 子目錄;
    開發環境則直接回傳 "ffmpeg",由系統 PATH 解析。
    """
    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", "."))
        bundled_path = base_path / "ffmpeg" / "ffmpeg.exe"
        if bundled_path.exists():
            return str(bundled_path)
    return "ffmpeg"
