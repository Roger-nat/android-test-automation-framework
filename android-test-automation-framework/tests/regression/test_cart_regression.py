import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def _open_cart_with_item(driver, users):
    login = LoginPage(driver)
    catalog = CatalogPage(driver)

    login.wait_for_page()
    login.login(users["standard"]["username"], users["standard"]["password"])
    catalog.wait_for_page()
    catalog.add_first_product()
    catalog.open_cart()

    cart = CartPage(driver)
    cart.wait_for_page()
    return catalog, cart


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_cart_contains_added_product(driver, users):
    _, cart = _open_cart_with_item(driver, users)

    assert cart.item_count() == 1
    assert cart.item_titles()


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_remove_product_returns_cart_to_empty_state(driver, users):
    _, cart = _open_cart_with_item(driver, users)

    cart.remove_first_item()

    assert cart.item_count() == 0
    assert cart.is_empty()


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_continue_shopping_returns_to_catalog(driver, users):
    catalog, cart = _open_cart_with_item(driver, users)

    cart.continue_shopping()

    catalog.wait_for_page()
    assert catalog.product_count() > 0


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_checkout_is_available_when_cart_has_item(driver, users):
    _, cart = _open_cart_with_item(driver, users)

    assert cart.checkout_visible()
