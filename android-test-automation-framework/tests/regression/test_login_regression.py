import pytest

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_invalid_password_is_rejected(driver, users):
    login = LoginPage(driver)
    login.wait_for_page()
    login.login(users["standard"]["username"], "wrong-password")

    assert login.is_error_visible()


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_locked_user_is_rejected(driver, users):
    login = LoginPage(driver)
    login.wait_for_page()
    login.login(users["locked"]["username"], users["locked"]["password"])

    assert login.is_error_visible()


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
@pytest.mark.parametrize(
    "username,password",
    [
        ("", ""),
        ("", "10203040"),
        ("bob@example.com", ""),
    ],
)
def test_login_validation_for_missing_credentials(driver, username, password):
    login = LoginPage(driver)
    login.wait_for_page()
    login.login(username, password)

    assert login.is_error_visible()


@pytest.mark.regression
@pytest.mark.functional
@pytest.mark.mobile
def test_login_leads_to_catalog(driver, users):
    login = LoginPage(driver)
    catalog = CatalogPage(driver)

    login.wait_for_page()
    login.login(users["standard"]["username"], users["standard"]["password"])
    catalog.wait_for_page()

    assert catalog.product_count() >= 1
