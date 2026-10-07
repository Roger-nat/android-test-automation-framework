import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.mobile
def test_standard_user_can_login(driver, users):
    login = LoginPage(driver)
    catalog = CatalogPage(driver)

    login.wait_for_page()
    login.login(users["standard"]["username"], users["standard"]["password"])
    catalog.wait_for_page()

    assert catalog.product_count() > 0
