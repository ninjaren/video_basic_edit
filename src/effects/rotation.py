"""畫面旋轉效果,純函式實作,不依賴 UI 或 IO 的任何細節,方便獨立測試與重複使用。"""

import cv2
import numpy as np

_ROTATE_MAP = {
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE,
}


def apply_rotation(frame: np.ndarray, angle: int) -> np.ndarray:
    """
    將畫面依指定角度旋轉。

    僅支援 0/90/180/270 四種直角角度;非直角旋轉會改變畫面邊界與尺寸,
    超出本工具「簡單調整」的設計範圍,因此刻意不支援,直接拋出例外提醒呼叫端。
    """
    if angle == 0:
        return frame
    if angle not in _ROTATE_MAP:
        raise ValueError(f"不支援的旋轉角度: {angle},僅支援 0/90/180/270。")
    return cv2.rotate(frame, _ROTATE_MAP[angle])
