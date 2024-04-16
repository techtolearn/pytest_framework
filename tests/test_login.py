from pages.LoginPage import LoginPage
from tests.base_test import BaseTest


class Login(BaseTest):
    def __int__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(self.driver)

    def test_login_app(self):
        self.login_page.navigate_to_app()
        self.login_page.find_links()
        self.login_page.get_network_status()


