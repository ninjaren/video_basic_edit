"""測試 core/pipeline.py 整合旋轉與亮度/對比度效果的套用順序與組合效果。"""

import numpy as np

from src.core.pipeline import apply_adjustments
from src.core.video_clip import AdjustmentSettings


def test_apply_adjustments_with_no_changes_returns_equivalent_frame():
    """預設設定(無旋轉、無亮度/對比度調整)應回傳內容相同的畫面。"""
    frame = np.full((10, 20, 3), 100, dtype=np.uint8)
    result = apply_adjustments(frame, AdjustmentSettings())
    assert np.array_equal(result, frame)


def test_apply_adjustments_rotates_before_brightness_contrast():
    """旋轉應先套用,因此輸出畫面的尺寸應已是旋轉後的尺寸,且亮度調整仍生效。"""
    frame = np.full((10, 20, 3), 100, dtype=np.uint8)
    settings = AdjustmentSettings(rotation=90, brightness=20)
    result = apply_adjustments(frame, settings)

    assert result.shape[0] == 20
    assert result.shape[1] == 10
    assert result.mean() > frame.mean()


def test_apply_adjustments_combines_rotation_brightness_and_contrast():
    """同時設定旋轉、亮度、對比度時,三者皆應生效且不互相干擾。"""
    frame = np.full((10, 20, 3), 100, dtype=np.uint8)
    settings = AdjustmentSettings(rotation=180, brightness=-30, contrast=10)
    result = apply_adjustments(frame, settings)

    assert result.shape == frame.shape  # 180 度旋轉尺寸不變
    assert result.mean() < frame.mean()  # 降低亮度後應變暗
