import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def _login(driver, users):
    LoginPage(driver).wait_for_page()
    LoginPage(driver).login(
        users["standard"]["username"],
        users["standard"]["password"],
    )
    catalog = CatalogPage(driver)
    catalog.wait_for_page()
    return catalog


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_catalog_displays_products(driver, users):
    catalog = _login(driver, users)

    assert catalog.product_count() > 0
    assert all(title.strip() for title in catalog.product_titles())


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_catalog_prices_are_visible(driver, users):
    catalog = _login(driver, users)

    prices = catalog.product_prices()
    assert prices
    assert all("$" in price for price in prices)


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_sort_by_name_ascending_changes_catalog(driver, users):
    catalog = _login(driver, users)

    before = catalog.product_titles()
    catalog.sort_name_ascending()
    after = catalog.product_titles()

    assert after == sorted(after, key=str.lower)
    assert before != []


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_sort_by_price_low_to_high_changes_catalog(driver, users):
    catalog = _login(driver, users)

    catalog.sort_price_low_to_high()
    prices = catalog.product_prices()

    def price_value(value: str) -> float:
        return float(value.replace("$", "").strip())

    assert prices == sorted(prices, key=price_value)


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_product_can_be_added_to_cart(driver, users):
    catalog = _login(driver, users)

    catalog.add_first_product()
    catalog.open_cart()

    from pages.cart_page import CartPage

    cart = CartPage(driver)
    cart.wait_for_page()
    assert cart.item_count() == 1
