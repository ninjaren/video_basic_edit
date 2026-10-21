"""
將 AdjustmentSettings 轉換為 FFmpeg 命令列參數。

純函式實作,不涉及子行程執行,方便獨立測試命令組裝邏輯是否正確,
與實際呼叫 FFmpeg 的 VideoExporter 分離,維持低耦合。
"""

from src.core.video_clip import AdjustmentSettings

# FFmpeg transpose filter 的方向需與 effects/rotation.py 的 cv2 旋轉方向保持一致:
# 90 對應 cv2.ROTATE_90_CLOCKWISE,270 對應 cv2.ROTATE_90_COUNTERCLOCKWISE,
# 180 無對應的單一 transpose 方向,改以等效的水平+垂直翻轉實現。
_ROTATION_FILTER_MAP = {
    90: "transpose=1",
    180: "hflip,vflip",
    270: "transpose=2",
}


def _build_video_filter(settings: AdjustmentSettings) -> str | None:
    """依旋轉/亮度/對比度組裝 -vf 的 filter 字串,若無任何畫面調整則回傳 None。"""
    filters = []

    if settings.rotation in _ROTATION_FILTER_MAP:
        filters.append(_ROTATION_FILTER_MAP[settings.rotation])

    if settings.brightness != 0 or settings.contrast != 0:
        # 換算公式需與 effects/brightness_contrast.py 的 convertScaleAbs 參數對齊,
        # 確保匯出結果與預覽畫面呈現一致幅度的調整。
        eq_brightness = settings.brightness / 100.0
        eq_contrast = 1 + settings.contrast / 100.0
        filters.append(f"eq=brightness={eq_brightness}:contrast={eq_contrast}")

    return ",".join(filters) if filters else None


def build_export_command(
    ffmpeg_path: str,
    source_path: str,
    settings: AdjustmentSettings,
    output_path: str,
) -> list[str]:
    """
    組裝匯出用的 FFmpeg 命令列參數列表。

    設計原則:
    - 一律重新編碼畫面(libx264)與音訊(aac),避免不同來源格式/音訊編碼
      造成串流複製(stream copy)失敗,犧牲少量速度/畫質換取相容性。
    - 剪切以輸入端 -ss(起點)搭配 -t(長度)實現,兼顧速度與可接受的準確度。
      trim_end 為 None 時代表不設定長度上限,即剪到影片結尾。
    - 音量為預設值(100)且未靜音時,不加入 -af,避免無意義的 filter。
    """
    trim_start = settings.trim_start
    trim_end = settings.trim_end
    duration = (trim_end - trim_start) if trim_end is not None else None

    command = [ffmpeg_path, "-y", "-ss", str(trim_start), "-i", source_path]
    if duration is not None:
        command += ["-t", str(duration)]

    video_filter = _build_video_filter(settings)
    if video_filter:
        command += ["-vf", video_filter]

    if settings.muted:
        command += ["-an"]
    else:
        command += ["-c:a", "aac"]
        if settings.volume != 100:
            command += ["-af", f"volume={settings.volume / 100.0}"]

    command += ["-c:v", "libx264", "-pix_fmt", "yuv420p", output_path]
    return command
