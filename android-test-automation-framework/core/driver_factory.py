from __future__ import annotations

from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import AppConfig


def create_driver(config: AppConfig):
    app_path = Path(config.app_path)
    if not app_path.exists():
        raise FileNotFoundError(
            f"APK not found at '{app_path}'. Run scripts/download_demo_app.py "
            "or set APP_PATH in .env."
        )

    options = UiAutomator2Options()
    options.platform_name = config.platform_name
    options.automation_name = config.automation_name
    options.device_name = config.device_name
    options.app = str(app_path)
    options.app_package = config.app_package
    options.auto_grant_permissions = True
    options.new_command_timeout = config.command_timeout_seconds
    options.no_reset = False
    options.full_reset = False
    options.set_capability("appium:disableWindowAnimation", True)

    if config.platform_version:
        options.platform_version = config.platform_version

    driver = webdriver.Remote(
        command_executor=config.appium_server_url,
        options=options,
    )
    driver.implicitly_wait(0)
    return driver
