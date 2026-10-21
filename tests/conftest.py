"""pytest 全域設定:測試 GUI 元件時強制使用 offscreen 平台,避免跳出視窗或依賴真實顯示環境。"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
