"""
集中管理專案設定值與常數。

依規範.md的低耦合原則,所有模組需要的固定參數(支援格式、調整範圍等)
皆從此處讀取,不在各模組內硬編碼(hard code),方便未來統一調整。
"""

APP_NAME = "簡易影片剪輯工具"

# 支援的影片副檔名(對應技術選型.md中 OpenCV/FFmpeg 的相容格式)
SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]

# 亮度調整範圍(對應 OpenCV convertScaleAbs 的 beta 參數)
BRIGHTNESS_DEFAULT = 0
BRIGHTNESS_MIN = -100
BRIGHTNESS_MAX = 100

# 對比度調整範圍(換算為 convertScaleAbs 的 alpha 參數)
CONTRAST_DEFAULT = 0
CONTRAST_MIN = -100
CONTRAST_MAX = 100

# 音量調整範圍(百分比,100 為原始音量,僅於匯出時由 FFmpeg 套用)
VOLUME_DEFAULT = 100
VOLUME_MIN = 0
VOLUME_MAX = 100

# 旋轉角度僅支援直角旋轉,避免非直角旋轉造成畫面尺寸變化
SUPPORTED_ROTATION_ANGLES = (0, 90, 180, 270)
