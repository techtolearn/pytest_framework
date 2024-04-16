from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from utils.config import TestData


class LoginPage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        super().__init__(self.driver)
        self.links1 = "//div[@class='et_pb_text_inner']//li/a"
        self.links = (By.XPATH, "//div[@class='et_pb_text_inner']//li/a")

    def navigate_to_app(self):
        self.open_url(TestData.BASE_URL)

    def find_links(self):
        list_links = self.driver.find_elements(By.XPATH, self.links1)
        for link in list_links:
            print(link.text)
            # print(self.get_hyper_links(self.links))

    def get_network_status(self):
        self.get_network_performance()
