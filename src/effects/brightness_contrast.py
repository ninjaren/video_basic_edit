"""亮度與對比度調整效果,純函式實作,只依賴輸入的畫面陣列與參數。"""

import cv2
import numpy as np


def apply_brightness_contrast(frame: np.ndarray, brightness: int, contrast: int) -> np.ndarray:
    """
    調整畫面亮度與對比度。

    brightness/contrast 範圍為 -100~100(對應 config.py 的設定範圍):
    - brightness 直接對應 OpenCV convertScaleAbs 的 beta(像素偏移量)。
    - contrast 換算為 alpha(像素縮放倍數),0 代表維持原始對比。
    此換算公式為經驗公式,目的是讓滑桿兩端呈現明顯但不過度失真的效果。
    """
    beta = brightness
    alpha = 1 + (contrast / 100.0)
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
