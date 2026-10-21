"""影片片段的資料模型與調整參數,不涉及實際的讀取、效果運算或編碼邏輯。"""

from dataclasses import dataclass, field


@dataclass
class VideoInfo:
    """影片的基本中繼資料,由 io 模組讀取後填入。"""

    width: int
    height: int
    fps: float
    duration: float
    frame_count: int
    file_format: str


@dataclass
class AdjustmentSettings:
    """
    使用者對影片套用的調整參數。

    預覽流程與匯出流程皆讀取同一份設定,確保兩者呈現的效果一致。
    trim_end 為 None 代表剪切範圍一路延伸到影片結尾。
    """

    trim_start: float = 0.0
    trim_end: float | None = None
    rotation: int = 0
    brightness: int = 0
    contrast: int = 0
    volume: int = 100
    muted: bool = False


@dataclass
class VideoClip:
    """代表使用者匯入的一段影片,結合來源路徑、中繼資料與調整設定。"""

    source_path: str
    info: VideoInfo
    settings: AdjustmentSettings = field(default_factory=AdjustmentSettings)
