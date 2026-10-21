"""應用程式進入點,啟動 PySide6 的 QApplication 與主視窗。"""

import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
