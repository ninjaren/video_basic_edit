"""測試 ControlsPanel 的使用者互動邏輯(旋轉循環、剪切範圍限制、設定彙整)。"""

import pytest
from PySide6.QtWidgets import QApplication

from src.core.video_clip import VideoInfo
from src.ui.controls_panel import ControlsPanel


@pytest.fixture(scope="module")
def qapp():
    """建立測試用的 QApplication,PySide6 元件需要有 QApplication 實例才能建立。"""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def panel(qapp):
    """每個測試使用全新的 ControlsPanel,避免測試之間互相影響狀態。"""
    return ControlsPanel()


def test_rotate_button_cycles_through_angles(panel):
    """每次點擊旋轉按鈕應依 0 -> 90 -> 180 -> 270 -> 0 循環。"""
    for expected_angle in (90, 180, 270, 0):
        panel._on_rotate_clicked()
        assert panel.current_settings().rotation == expected_angle


def test_trim_controls_disabled_before_import(panel):
    """匯入影片前,剪切範圍與匯出按鈕應維持停用狀態,避免使用者誤操作。"""
    assert not panel._trim_start_spinbox.isEnabled()
    assert not panel._trim_end_spinbox.isEnabled()
    assert not panel._export_button.isEnabled()


def test_show_video_info_enables_controls_and_sets_full_trim_range(panel):
    """匯入影片後,剪切範圍應依影片長度設定,預設為完整範圍,且啟用匯出按鈕。"""
    info = VideoInfo(width=320, height=240, fps=24.0, duration=5.0, frame_count=120, file_format="mp4")
    panel.show_video_info(info)

    assert panel._trim_start_spinbox.isEnabled()
    assert panel._trim_end_spinbox.isEnabled()
    assert panel._export_button.isEnabled()

    settings = panel.current_settings()
    assert settings.trim_start == 0.0
    assert settings.trim_end == 5.0


def test_trim_start_cannot_exceed_trim_end(panel):
    """將剪切起點設定超過終點時,終點應自動跟進調整,維持起點小於終點。"""
    info = VideoInfo(width=320, height=240, fps=24.0, duration=5.0, frame_count=120, file_format="mp4")
    panel.show_video_info(info)

    panel._trim_start_spinbox.setValue(4.8)

    assert panel._trim_end_spinbox.value() > panel._trim_start_spinbox.value()


def test_mute_checkbox_reflected_in_settings(panel):
    """勾選靜音後,current_settings() 應回報 muted=True。"""
    panel._mute_checkbox.setChecked(True)
    assert panel.current_settings().muted is True
