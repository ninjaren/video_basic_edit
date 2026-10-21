# 影片基礎剪輯工具

Windows 桌面版的簡易影片剪輯工具,詳見規劃文件:

- [規範.md](規範.md) — 程式撰寫規範(模組化、低耦合、繁體中文註解)
- [目標.md](目標.md) — 專案目標與功能範圍
- [技術選型.md](技術選型.md) — 技術選型與理由

## 開發環境需求

- Python 3.10 以上
- 系統已安裝 FFmpeg 並可於命令列執行(開發階段匯出功能依賴此設定;
  打包成 .exe 後將改為內建 FFmpeg,詳見技術選型.md)

## 安裝依賴

```bash
pip install -r requirements-dev.txt
```

僅安裝執行所需套件(不含測試/打包工具)則使用:

```bash
pip install -r requirements.txt
```

## 執行

```bash
python main.py
```

## 執行測試

```bash
pytest
```

## 打包成 Windows 執行檔

1. 取得 FFmpeg 執行檔(例如從 [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 下載,
   或複製系統已安裝的版本),放置於 `resources/ffmpeg/ffmpeg.exe`
   (授權說明見 [resources/ffmpeg/NOTICE.md](resources/ffmpeg/NOTICE.md))。
2. 安裝打包工具:`pip install -r requirements-dev.txt`
3. 執行打包:

   ```bash
   pyinstaller build.spec --noconfirm
   ```

4. 打包結果位於 `dist/VideoBasicEdit/`,將整個資料夾壓縮分享,使用者解壓後
   雙擊資料夾內的 `VideoBasicEdit.exe` 即可執行,不需另外安裝 Python 或 FFmpeg。

## 專案結構

```
video_basic_edit/
├── main.py              # 程式進入點
├── src/
│   ├── config.py          # 集中管理設定值與常數
│   ├── core/               # 資料模型與調整管線
│   ├── io/                  # 影片讀取(OpenCV)與匯出(FFmpeg)
│   ├── effects/             # 旋轉、亮度/對比度等純函式效果
│   ├── ui/                  # PySide6 介面(主視窗/預覽/控制面板)
│   └── utils/                # 共用工具(日誌、FFmpeg 路徑解析)
└── tests/                  # 單元測試
```

## 目前骨架狀態

- [x] GUI 可啟動,支援匯入影片並顯示基本資訊
- [x] 旋轉、亮度、對比度可即時套用於預覽畫面
- [x] 剪切(Trim)起止時間介面已完成(依影片長度動態設定範圍,並確保起點不超過終點)
- [x] 已以 mp4/mov/avi/mkv/wmv 五種格式測試影片驗證 `VideoReader` 讀取相容性
- [x] 匯出功能已實作:`VideoExporter` 透過 `ffmpeg_command_builder` 組裝剪切/旋轉/
  亮度/對比度/音量/靜音的 FFmpeg filter,並以 `ExportWorker`(QThread)於背景
  執行緒執行,避免阻塞 UI
- [x] 已完成多格式端對端測試(mp4/mov/avi/mkv/wmv)與效能檢查(720p 影片預覽
  延遲平均 28.7ms、匯出 8 秒影片耗時 0.47 秒),單元測試增至 23 個
- [x] 已完成打包成 Windows 執行檔(PyInstaller onedir 模式,內建 FFmpeg),
  啟動與匯出邏輯已驗證可正常運作;僅缺「完全乾淨的 Windows 機器」實機測試,
  詳見 [實作步驟.md](實作步驟.md) 階段 4 的待辦說明
- [x] 亮度/對比度/音量新增數字輸入框(與滑桿同步),方便精確輸入數值
  (使用者實測真實 4K 影片後的回饋調整)
