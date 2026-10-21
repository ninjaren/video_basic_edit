"""提供全專案共用的日誌記錄器,避免各模組各自設定 handler 造成重複輸出。"""

import logging


def get_logger(name: str) -> logging.Logger:
    """取得指定名稱的 logger,若尚未設定過 handler 才進行初始化。"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
