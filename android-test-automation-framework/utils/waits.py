from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_visible(driver, locator: tuple[str, str], timeout: int):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_clickable(driver, locator: tuple[str, str], timeout: int):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def accessibility_id(value: str) -> tuple[str, str]:
    return (AppiumBy.ACCESSIBILITY_ID, value)
