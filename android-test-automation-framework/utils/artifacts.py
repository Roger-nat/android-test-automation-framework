from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import subprocess

from config.settings import ROOT_DIR, settings
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")[:120]


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_screenshot(driver, test_name: str) -> Path | None:
    try:
        out_dir = ROOT_DIR / "artifacts" / "screenshots"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{_safe_name(test_name)}_{_stamp()}.png"
        driver.save_screenshot(str(path))
        LOGGER.info("Saved screenshot: %s", path)
        return path
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Could not save screenshot: %s", exc)
        return None


def capture_logcat(test_name: str) -> Path | None:
    out_dir = ROOT_DIR / "artifacts" / "logcat"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{_safe_name(test_name)}_{_stamp()}.txt"

    try:
        result = subprocess.run(
            ["adb", "logcat", "-d", "-t", "250"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        path.write_text(result.stdout or result.stderr, encoding="utf-8")
        LOGGER.info("Saved Logcat: %s", path)
        return path
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Could not capture Logcat: %s", exc)
        return None
