from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _bool_env(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(int(default))).strip().lower() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class AppConfig:
    appium_server_url: str
    platform_name: str
    automation_name: str
    device_name: str
    platform_version: str | None
    app_path: str
    app_package: str
    standard_user_email: str
    standard_user_password: str
    locked_user_email: str
    locked_user_password: str
    command_timeout_seconds: int
    element_timeout_seconds: int
    run_mobile_tests: bool
    llm_api_url: str | None
    llm_api_key: str | None
    llm_model: str | None
    llm_timeout_seconds: int


def load_config() -> AppConfig:
    app_path = os.getenv("APP_PATH", "./app/Android.MyDemoAppRN.apk")
    resolved_app_path = str((ROOT_DIR / app_path).resolve()) if not os.path.isabs(app_path) else app_path

    return AppConfig(
        appium_server_url=os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723"),
        platform_name=os.getenv("PLATFORM_NAME", "Android"),
        automation_name=os.getenv("AUTOMATION_NAME", "UiAutomator2"),
        device_name=os.getenv("DEVICE_NAME", "Pixel_6_API_33"),
        platform_version=os.getenv("PLATFORM_VERSION") or None,
        app_path=resolved_app_path,
        app_package=os.getenv("APP_PACKAGE", "com.swaglabsmobileapp"),
        standard_user_email=os.getenv("STANDARD_USER_EMAIL", "bob@example.com"),
        standard_user_password=os.getenv("STANDARD_USER_PASSWORD", "10203040"),
        locked_user_email=os.getenv("LOCKED_USER_EMAIL", "alice@example.com"),
        locked_user_password=os.getenv("LOCKED_USER_PASSWORD", "10203040"),
        command_timeout_seconds=int(os.getenv("COMMAND_TIMEOUT_SECONDS", "180")),
        element_timeout_seconds=int(os.getenv("ELEMENT_TIMEOUT_SECONDS", "20")),
        run_mobile_tests=_bool_env("RUN_MOBILE_TESTS", False),
        llm_api_url=os.getenv("LLM_API_URL") or None,
        llm_api_key=os.getenv("LLM_API_KEY") or None,
        llm_model=os.getenv("LLM_MODEL") or None,
        llm_timeout_seconds=int(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
    )


settings = load_config()
