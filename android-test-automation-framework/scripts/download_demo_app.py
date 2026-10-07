from __future__ import annotations

import sys
from pathlib import Path

import requests

from config.settings import ROOT_DIR

# Public sample application release endpoint.
# The binary itself is intentionally excluded from Git.
DEFAULT_URL = (
    "https://github.com/saucelabs/my-demo-app-rn/releases/"
    "latest/download/Android.MyDemoAppRN.apk"
)

OUT_PATH = ROOT_DIR / "app" / "Android.MyDemoAppRN.apk"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with OUT_PATH.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    print(f"Downloaded APK to: {OUT_PATH}")


if __name__ == "__main__":
    main()
