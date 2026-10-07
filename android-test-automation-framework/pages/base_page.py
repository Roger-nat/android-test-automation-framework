from __future__ import annotations

from typing import Iterable

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from utils.logger import get_logger
from utils.waits import wait_clickable, wait_visible

LOGGER = get_logger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, strategy: str, value: str, timeout: int | None = None):
        return wait_visible(
            self.driver,
            (strategy, value),
            timeout or settings.element_timeout_seconds,
        )

    def wait_clickable(self, strategy: str, value: str, timeout: int | None = None):
        return wait_clickable(
            self.driver,
            (strategy, value),
            timeout or settings.element_timeout_seconds,
        )

    def click(self, strategy: str, value: str):
        element = self.wait_clickable(strategy, value)
        element.click()
        return element

    def type_text(self, strategy: str, value: str, text: str):
        element = self.wait_visible(strategy, value)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, strategy: str, value: str, timeout: int | None = None) -> str:
        return self.wait_visible(strategy, value, timeout).text

    def exists(self, strategy: str, value: str, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(strategy, value)) > 0
            )
            return True
        except TimeoutException:
            return False

    def elements(self, strategy: str, value: str) -> list:
        return self.driver.find_elements(strategy, value)

    def back(self):
        self.driver.back()

    def hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def scroll_to_text(self, text: str):
        ui_selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"));'
        )
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)
