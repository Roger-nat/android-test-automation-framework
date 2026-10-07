from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from config.settings import ROOT_DIR, settings
from core.driver_factory import create_driver
from utils.adb import clear_app_data
from utils.ai_failure_analyzer import analyze_failure
from utils.artifacts import capture_logcat, save_screenshot


def _load_users() -> dict[str, Any]:
    path = ROOT_DIR / "tests" / "data" / "users.json"
    return json.loads(path.read_text(encoding="utf-8"))


USERS = _load_users()


def pytest_configure(config):
    for directory in (
        ROOT_DIR / "reports",
        ROOT_DIR / "artifacts" / "screenshots",
        ROOT_DIR / "artifacts" / "logcat",
        ROOT_DIR / "artifacts" / "failure_analysis",
    ):
        directory.mkdir(parents=True, exist_ok=True)


def pytest_collection_modifyitems(config, items):
    if settings.run_mobile_tests:
        return

    skip_mobile = pytest.mark.skip(
        reason="RUN_MOBILE_TESTS is not enabled; set RUN_MOBILE_TESTS=1 for device tests."
    )
    for item in items:
        if "mobile" in item.keywords:
            item.add_marker(skip_mobile)


@pytest.fixture(scope="session")
def users():
    return USERS


@pytest.fixture()
def driver(request):
    test_driver = create_driver(settings)
    try:
        yield test_driver
    finally:
        try:
            test_driver.quit()
        except Exception:
            pass


@pytest.fixture()
def logged_in(driver, users):
    from pages.login_page import LoginPage
    from pages.catalog_page import CatalogPage

    login = LoginPage(driver)
    catalog = CatalogPage(driver)
    login.wait_for_page()
    login.login(
        settings.standard_user_email or users["standard"]["username"],
        settings.standard_user_password or users["standard"]["password"],
    )
    catalog.wait_for_page()
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed or "mobile" not in item.keywords:
        return

    test_name = item.nodeid
    test_driver = item.funcargs.get("driver")

    if test_driver is not None:
        save_screenshot(test_driver, test_name)

    log_path = capture_logcat(test_name)

    failure_text = report.longreprtext or "No Pytest failure text available."
    logcat_text = ""
    if log_path and Path(log_path).exists():
        logcat_text = Path(log_path).read_text(encoding="utf-8", errors="ignore")

    analyze_failure(
        test_name=test_name,
        failure_text=failure_text,
        logcat_text=logcat_text,
    )
