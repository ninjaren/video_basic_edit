# FFmpeg 授權說明

本專案打包發行時,會將 `ffmpeg.exe` 隨應用程式一起發行,用於影片匯出功能。

## 來源

- 建置版本:`ffmpeg version 8.0-essentials_build` by [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- 原始碼:[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## 授權

此建置版本啟用了 `--enable-gpl --enable-version3`,並連結 `libx264`、`libx265` 等
GPL 授權的函式庫,因此本專案發行的 `ffmpeg.exe` 屬於 **GPLv3** 授權。

- 完整授權條文:[https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

## 與本專案的關係

本專案(`video_basic_edit` 的 Python 原始碼)僅以「獨立子行程(subprocess)」的方式
呼叫 `ffmpeg.exe`,並未靜態或動態連結 FFmpeg 的函式庫,屬於與 GPL 軟體的
「單純聚合(mere aggregation)」,因此本專案的原始碼本身不因此被要求以 GPL 授權發行。

但發行包中包含的 `ffmpeg.exe` 本身仍受 GPLv3 約束,發行者有義務:

1. 於發行包中保留本授權說明。
2. 提供取得對應版本 FFmpeg 原始碼的方式(見上方連結)。

## 注意

`ffmpeg.exe` 檔案本身(約 95MB)不會提交到版本控制(見專案根目錄 `.gitignore`),
建置 `.exe` 前請依 [實作步驟.md](../../實作步驟.md) 階段 4 的說明,自行取得
FFmpeg 執行檔並放置於此目錄。
