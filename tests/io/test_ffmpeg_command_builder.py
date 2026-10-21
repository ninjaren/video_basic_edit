"""測試 FFmpeg 命令組裝邏輯,不實際執行 FFmpeg。"""

from src.core.video_clip import AdjustmentSettings
from src.io.ffmpeg_command_builder import build_export_command


def test_default_settings_produce_minimal_command():
    """未調整任何參數時,不應加入 -vf,也不應加入 -af。"""
    settings = AdjustmentSettings(trim_start=0.0, trim_end=5.0)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    assert "-vf" not in command
    assert "-af" not in command
    assert "-an" not in command
    assert "-t" in command
    assert command[command.index("-t") + 1] == "5.0"


def test_rotation_90_maps_to_transpose_1():
    """旋轉 90 度應對應 FFmpeg transpose=1,與 cv2.ROTATE_90_CLOCKWISE 方向一致。"""
    settings = AdjustmentSettings(rotation=90)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    vf_index = command.index("-vf")
    assert command[vf_index + 1] == "transpose=1"


def test_rotation_180_maps_to_hflip_vflip():
    """旋轉 180 度以水平+垂直翻轉等效實現。"""
    settings = AdjustmentSettings(rotation=180)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    vf_index = command.index("-vf")
    assert command[vf_index + 1] == "hflip,vflip"


def test_brightness_and_contrast_combine_with_rotation():
    """旋轉與亮度/對比度應合併在同一個 -vf 參數中,以逗號分隔。"""
    settings = AdjustmentSettings(rotation=270, brightness=50, contrast=-20)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    vf_index = command.index("-vf")
    assert command[vf_index + 1] == "transpose=2,eq=brightness=0.5:contrast=0.8"


def test_muted_adds_an_flag_without_audio_filter():
    """靜音時應加入 -an,且不應同時加入 -af 或 -c:a。"""
    settings = AdjustmentSettings(muted=True, volume=50)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    assert "-an" in command
    assert "-af" not in command
    assert "-c:a" not in command


def test_custom_volume_adds_volume_filter():
    """非預設音量時應加入對應的 volume filter。"""
    settings = AdjustmentSettings(volume=50)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    af_index = command.index("-af")
    assert command[af_index + 1] == "volume=0.5"
    assert "-c:a" in command


def test_trim_end_none_omits_duration_flag():
    """trim_end 為 None 時不應加入 -t,代表剪切到影片結尾。"""
    settings = AdjustmentSettings(trim_start=1.0, trim_end=None)
    command = build_export_command("ffmpeg", "input.mp4", settings, "output.mp4")

    assert "-t" not in command
    assert "-ss" in command
    assert command[command.index("-ss") + 1] == "1.0"
