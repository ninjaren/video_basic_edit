"""測試 AdjustmentSettings/VideoClip 資料模型的預設值與邊界案例。"""

from src.core.video_clip import AdjustmentSettings, VideoClip, VideoInfo


def test_adjustment_settings_defaults():
    """未指定任何參數時,應維持「不調整」的中性預設值。"""
    settings = AdjustmentSettings()
    assert settings.trim_start == 0.0
    assert settings.trim_end is None
    assert settings.rotation == 0
    assert settings.brightness == 0
    assert settings.contrast == 0
    assert settings.volume == 100
    assert settings.muted is False


def test_video_clip_default_settings_are_not_shared_between_instances():
    """
    建立 VideoClip 時未指定 settings,應各自套用獨立的預設值。

    驗證 video_clip.py 使用 `field(default_factory=AdjustmentSettings)`
    而非可變預設值(mutable default argument),避免不同 VideoClip 實例
    誤共用同一個 AdjustmentSettings 物件。
    """
    info = VideoInfo(width=320, height=240, fps=24.0, duration=2.0, frame_count=48, file_format="mp4")
    clip_a = VideoClip(source_path="a.mp4", info=info)
    clip_b = VideoClip(source_path="b.mp4", info=info)

    clip_a.settings.brightness = 50

    assert clip_b.settings.brightness == 0
