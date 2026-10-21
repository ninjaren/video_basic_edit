"""負責讀取影片檔案、取得中繼資料與畫面幀,封裝 OpenCV 的呼叫細節。"""

from pathlib import Path

import cv2
import numpy as np

from src.core.video_clip import VideoInfo


class VideoReader:
    """包裝 cv2.VideoCapture,提供讀取影片資訊與指定時間點畫面的介面。"""

    def __init__(self, source_path: str) -> None:
        self._source_path = source_path
        self._capture = cv2.VideoCapture(source_path)
        if not self._capture.isOpened():
            raise IOError(f"無法開啟影片檔案: {source_path}")

    def read_info(self) -> VideoInfo:
        """讀取影片基本中繼資料(解析度、FPS、長度、格式)。"""
        width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self._capture.get(cv2.CAP_PROP_FPS) or 0.0
        frame_count = int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0.0
        file_format = Path(self._source_path).suffix.lstrip(".").lower()
        return VideoInfo(
            width=width,
            height=height,
            fps=fps,
            duration=duration,
            frame_count=frame_count,
            file_format=file_format,
        )

    def read_frame_at(self, time_seconds: float) -> np.ndarray:
        """讀取指定時間點(秒)的畫面幀,回傳 BGR 格式的 numpy 陣列。"""
        fps = self._capture.get(cv2.CAP_PROP_FPS) or 0.0
        frame_index = int(time_seconds * fps) if fps > 0 else 0
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, frame = self._capture.read()
        if not success:
            raise IOError(f"無法讀取時間點 {time_seconds} 秒的畫面。")
        return frame

    def close(self) -> None:
        """釋放底層的 VideoCapture 資源。"""
        self._capture.release()
