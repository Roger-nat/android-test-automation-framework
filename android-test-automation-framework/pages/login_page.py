from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

USERNAME = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")
LOGIN_LOGO = (AppiumBy.ACCESSIBILITY_ID, "test-Login")


class LoginPage(BasePage):
    def wait_for_page(self):
        self.wait_visible(*LOGIN_BUTTON, timeout=30)

    def enter_username(self, username: str):
        self.type_text(*USERNAME, username)

    def enter_password(self, password: str):
        self.type_text(*PASSWORD, password)

    def tap_login(self):
        self.click(*LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login()

    def error_message(self) -> str:
        return self.get_text(*ERROR_MESSAGE, timeout=8)

    def is_error_visible(self) -> bool:
        return self.exists(*ERROR_MESSAGE, timeout=5)
