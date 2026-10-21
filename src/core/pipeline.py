"""
影片畫面調整管線。

整合 effects 模組中各項獨立效果,依固定順序套用至單一畫面幀,
讓預覽流程與匯出流程共用同一份邏輯,避免兩邊實作不一致。
音量/靜音屬於音訊處理,不在此畫面管線範圍內,由匯出階段的 FFmpeg 另行處理。
"""

import numpy as np

from src.core.video_clip import AdjustmentSettings
from src.effects.brightness_contrast import apply_brightness_contrast
from src.effects.rotation import apply_rotation


def apply_adjustments(frame: np.ndarray, settings: AdjustmentSettings) -> np.ndarray:
    """依序套用旋轉、亮度、對比度調整,回傳處理後的畫面幀。"""
    frame = apply_rotation(frame, settings.rotation)
    frame = apply_brightness_contrast(frame, settings.brightness, settings.contrast)
    return frame
