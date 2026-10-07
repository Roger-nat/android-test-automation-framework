from __future__ import annotations

import logging
from pathlib import Path

from config.settings import ROOT_DIR


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_dir = ROOT_DIR / "artifacts"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_dir / "framework.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
