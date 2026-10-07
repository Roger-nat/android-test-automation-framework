from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

CART_TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-Cart")
CART_ITEM = (AppiumBy.ACCESSIBILITY_ID, "test-Item")
ITEM_TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-Item title")
REMOVE_ITEM = (AppiumBy.ACCESSIBILITY_ID, "test-Remove Item")
CHECKOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT")
CONTINUE_SHOPPING = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE SHOPPING")
EMPTY_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-No Items")


class CartPage(BasePage):
    def wait_for_page(self):
        self.wait_visible(*CART_TITLE, timeout=20)

    def item_count(self) -> int:
        return len(self.elements(*CART_ITEM))

    def item_titles(self) -> list[str]:
        return [item.text for item in self.elements(*ITEM_TITLE)]

    def remove_first_item(self):
        buttons = self.elements(*REMOVE_ITEM)
        if not buttons:
            raise AssertionError("No remove button found in cart.")
        buttons[0].click()

    def is_empty(self) -> bool:
        return self.exists(*EMPTY_MESSAGE, timeout=5)

    def checkout_visible(self) -> bool:
        return self.exists(*CHECKOUT_BUTTON, timeout=5)

    def continue_shopping(self):
        self.click(*CONTINUE_SHOPPING)
