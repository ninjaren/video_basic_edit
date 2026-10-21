"""測試亮度/對比度效果的純函式邏輯。"""

import numpy as np

from src.effects.brightness_contrast import apply_brightness_contrast


def test_zero_adjustment_keeps_frame_unchanged():
    """亮度與對比度皆為 0 時,畫面像素值應維持不變。"""
    frame = np.full((5, 5, 3), 100, dtype=np.uint8)
    result = apply_brightness_contrast(frame, brightness=0, contrast=0)
    assert np.array_equal(result, frame)


def test_positive_brightness_increases_pixel_values():
    """提高亮度應讓像素值變大(調亮)。"""
    frame = np.full((5, 5, 3), 100, dtype=np.uint8)
    result = apply_brightness_contrast(frame, brightness=50, contrast=0)
    assert result.mean() > frame.mean()


def test_negative_brightness_decreases_pixel_values():
    """降低亮度應讓像素值變小(調暗)。"""
    frame = np.full((5, 5, 3), 100, dtype=np.uint8)
    result = apply_brightness_contrast(frame, brightness=-50, contrast=0)
    assert result.mean() < frame.mean()
