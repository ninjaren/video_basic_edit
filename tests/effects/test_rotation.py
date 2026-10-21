"""測試旋轉效果的純函式邏輯。"""

import numpy as np
import pytest

from src.effects.rotation import apply_rotation


def test_rotate_0_degrees_returns_same_frame():
    """角度為 0 時應直接回傳原始畫面,不做任何處理。"""
    frame = np.zeros((10, 20, 3), dtype=np.uint8)
    result = apply_rotation(frame, 0)
    assert result is frame


def test_rotate_90_degrees_swaps_dimensions():
    """旋轉 90 度後,畫面寬高應互換。"""
    frame = np.zeros((10, 20, 3), dtype=np.uint8)
    result = apply_rotation(frame, 90)
    assert result.shape[0] == 20
    assert result.shape[1] == 10


def test_rotate_invalid_angle_raises_value_error():
    """非直角角度應拋出例外,提醒呼叫端這是不支援的輸入。"""
    frame = np.zeros((10, 20, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        apply_rotation(frame, 45)
