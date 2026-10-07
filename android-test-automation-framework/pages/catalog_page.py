from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

CATALOG_HEADER = (AppiumBy.ACCESSIBILITY_ID, "test-Catalog")
CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "test-Cart")
SORT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-Modal Selector Button")
PRODUCT_ITEM = (AppiumBy.ACCESSIBILITY_ID, "test-Item")
PRODUCT_TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-Item title")
PRODUCT_PRICE = (AppiumBy.ACCESSIBILITY_ID, "test-Item price")
ADD_TO_CART = (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART")
SORT_NAME_ASC = (AppiumBy.ACCESSIBILITY_ID, "test-Name - A to Z")
SORT_PRICE_ASC = (AppiumBy.ACCESSIBILITY_ID, "test-Price - Low to High")


class CatalogPage(BasePage):
    def wait_for_page(self):
        self.wait_visible(*CATALOG_HEADER, timeout=30)

    def product_count(self) -> int:
        return len(self.elements(*PRODUCT_ITEM))

    def product_titles(self) -> list[str]:
        return [item.text for item in self.elements(*PRODUCT_TITLE)]

    def product_prices(self) -> list[str]:
        return [item.text for item in self.elements(*PRODUCT_PRICE)]

    def add_first_product(self):
        buttons = self.elements(*ADD_TO_CART)
        if not buttons:
            raise AssertionError("No Add to Cart button found.")
        buttons[0].click()

    def open_cart(self):
        self.click(*CART_ICON)

    def open_sort(self):
        self.click(*SORT_BUTTON)

    def sort_name_ascending(self):
        self.open_sort()
        self.click(*SORT_NAME_ASC)

    def sort_price_low_to_high(self):
        self.open_sort()
        self.click(*SORT_PRICE_ASC)

    def cart_badge_text(self) -> str:
        return self.get_text(*CART_ICON, timeout=5)
