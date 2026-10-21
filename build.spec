# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包設定。

採用 onedir(資料夾)而非 onefile 模式:FFmpeg 執行檔(約 95MB)加上
PySide6/OpenCV 的體積較大,onefile 模式每次啟動都需先解壓縮至暫存目錄,
onedir 模式則只在建置時展開一次,後續啟動速度明顯較快,對於會重複開關的
桌面工具而言使用者體驗較好。發行時可將整個 dist/VideoBasicEdit 資料夾
壓縮成 zip 分享,使用者解壓後雙擊資料夾內的 .exe 即可執行。

FFmpeg 執行檔會被放入打包結果的 ffmpeg/ 子目錄,對應
src/utils/ffmpeg_utils.py 中 resolve_ffmpeg_path() 的路徑解析邏輯。
"""

from pathlib import Path

project_root = Path.cwd()
ffmpeg_exe = project_root / "resources" / "ffmpeg" / "ffmpeg.exe"

if not ffmpeg_exe.exists():
    raise SystemExit(
        f"找不到 {ffmpeg_exe},請先依 resources/ffmpeg/NOTICE.md 的說明放置 FFmpeg 執行檔。"
    )

a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=[(str(ffmpeg_exe), "ffmpeg")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VideoBasicEdit",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="VideoBasicEdit",
)
