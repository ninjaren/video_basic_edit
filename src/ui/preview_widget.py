"""顯示單張畫面幀的預覽元件,只負責呈現,不處理任何影片讀取或效果運算邏輯。"""

import cv2
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PreviewWidget(QWidget):
    """顯示單張畫面幀的預覽元件。"""

    def __init__(self) -> None:
        super().__init__()
        self._label = QLabel("請匯入影片")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setMinimumSize(320, 240)

        layout = QVBoxLayout(self)
        layout.addWidget(self._label)

    def show_frame(self, frame: np.ndarray) -> None:
        """將 BGR 格式的 numpy 畫面幀轉換為 QPixmap 並顯示,依元件大小等比例縮放。"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytes_per_line = channel * width
        image = QImage(
            rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(
            self._label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled_pixmap)
