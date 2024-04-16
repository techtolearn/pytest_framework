import json
import logging
import os
import time
from datetime import datetime

import pandas as pd
import pyautogui
from bs4 import BeautifulSoup
from selenium.common import ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import TestData
from utils.db_connection import DatabaseHelper
from utils.enums import WaitType


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, WaitType.WEB_DRIVER_WAIT.value)
        self._short_wait = WebDriverWait(self.driver, WaitType.SHORT.value)
        self._long_wait = WebDriverWait(self.driver, WaitType.LONG.value)
        self._fluent_wait = WebDriverWait(self.driver, WaitType.FLUENT.value, poll_frequency=1,
                                          ignored_exceptions=[ElementNotVisibleException])
        self.db = DatabaseHelper(TestData.HOST, TestData.USER_NAME, TestData.PASSWORD, TestData.DB_NAME, TestData.PORT)

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(5)

    def get_element(self, locator):
        return self.driver.find_element(locator)

    def click_element(self, locator):
        element = self.get_element(locator)
        self.highlight_element(element, "green")
        element.click()

    def click_with_Js(self, locator):
        self.driver.execute_script("arguments[0].click();", locator)

    def close_browser(self):
        self.driver.quit()

    def is_element_displayed(self, element_locator):
        try:
            return self._wait.until(EC.visibility_of_element_located(element_locator)).is_displayed()
        except:
            return False

    def is_element_present(self, element_locator):
        try:
            self._wait.until(EC.presence_of_element_located(element_locator))
            return True
        except:
            return False

    def is_element_visible(self, element_locator):
        try:
            return self._wait.until(EC.visibility_of_element_located(element_locator)).is_displayed()
        except:
            return False

    def input_text(self, locator, text):
        element = self.get_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self._wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def get_all_text_from_elements(self, locator):
        elements = self._wait.until(EC.presence_of_all_elements_located(locator))
        return [element.text for element in elements]

    @staticmethod
    def get_tooltip_text(self, element):
        tooltip_text = element.get_attribute("title")
        return tooltip_text if tooltip_text else element.get_attribute("aria-label")

    def send_text(self, element_locator, text):
        element = self._wait.until(EC.presence_of_element_located(element_locator))
        element.clear()
        element.send_keys(text)

    def clear_text(self, locator):
        el = self._wait.until(EC.element_to_be_clickable(locator))
        el.clear()

    def handle_alert(self, accept=True):
        alert = self._wait.until(EC.alert_is_present())

        if accept:
            alert.accept()
        else:
            alert.dismiss()

    def wait_for_element(self, locator):
        self._wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility_of_element(self, locator):
        self._wait.until(EC.visibility_of_element_located(locator))

    def wait_for_invisibility_of_element(self, locator):
        self._wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text_in_element(self, locator, text):
        self._wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_page_load(self):
        self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    def select_dropdown_option(self, locator, option, select_by='text'):
        element = self.get_element(locator)
        select = Select(element)

        if select_by == 'text':
            select.select_by_visible_text(option)
        elif select_by == 'value':
            select.select_by_value(option)
        elif select_by == 'index':
            select.select_by_index(option)
        else:
            raise ValueError("Invalid 'select_by' option. Use 'text', 'value', or 'index'.")

    def double_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.double_click(element).perform()

    def context_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.context_click(element).perform()

    def hover_and_get_text(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).perform()
        return element.text

    def scroll_to_element(self, locator):
        self.driver.execute_script("argument[0].scrollIntoView(true);", self.get_element(locator))

    def get_page_max_umber(self, locator):
        """ get the max number from the web-table pagination"""
        html = self.get_element(locator).get_attribute("outerHtml")
        soup = BeautifulSoup(html, 'lxml')
        soup.select_one('div.pagination > span').text.split(' ')[-1]

    def get_text_page_source(self, expected_text):
        page_source = self.driver.page_source
        if expected_text in page_source:
            print(f"Text '{expected_text}' found in the page source")
        else:
            print(f"Text '{expected_text}' not found in the page source")

    def get_text_from_source(self, locator):
        """
        get the page source of the current page
        :param locator:
        :return:
        """
        return self.driver.execute_script(f"return arguments[0].outerHTML;", locator)

    def get_page_source_usingJs(self, loc_type, locator):
        """
        driver.execute_script("return document.getElementsByTagName('html)[0].innerHtml")
        :param loc_type:
        :param locator:
        :return:
        eg: self.get_page_source_usingJs("ByClassName", "<class-name>"))
        """
        content = self.driver.execute_script(f"return document.getElements{loc_type}({locator}')[0].innerHTML")
        soup = BeautifulSoup(content, 'lxml')
        return soup.prettify()

    def perform_actions(self, actions_list):
        # """
        #  # Example: Performing a sequence of actions
        # actions_list = [
        #     {'action': 'move_to_element', 'by': By.ID, 'value': 'exampleElement1'},
        #     {'action': 'click', 'by': By.XPATH, 'value': "//button[@id='exampleButton']"},
        #     {'action': 'double_click', 'by': By.CLASS_NAME, 'value': 'exampleClass'},
        #     # Add more actions as needed
        # ]
        # :param actions_list:
        # :return:
        # """
        action_chains = ActionChains(self.driver)
        for action in actions_list:
            if action['action'] == 'move_to_element':
                element = self.get_element(action['by'], action['value'])
                action_chains.move_to_element(element)
            elif action['action'] == 'click':
                element = self.get_element(action['by'], action['value'])
                action_chains.click(element)
            elif action['action'] == 'double_click':
                element = self.get_element(action['by'], action['value'])
                action_chains.double_click(element)
            elif action['action'] == 'context_click':
                element = self.get_element(action['by'], action['value'])
                action_chains.context_click(element)
            # Add more actions as needed

        action_chains.perform()

    def drag_and_drop(self, source_by, source_locator, target_locator):
        source_element = self.get_element(source_locator)
        target_element = self.get_element(target_locator)

        action_chains = ActionChains(self.driver)
        action_chains.drag_and_drop(source_element, target_element).perform()

    @staticmethod
    def click_element_with_robot(element):
        location = element.location_once_scrolled_into_view
        pyautogui.click(location['x'], location['y'])

    def perform_robot_actions(self, actions_list):
        # """
        #     # Example: Performing robot actions
        # actions_list = [
        #     {'action': 'click', 'by': By.ID, 'value': 'exampleButton'},
        #     {'action': 'type', 'by': By.NAME, 'value': 'exampleInput', 'text': 'Hello, World!'},
        #     {'action': 'scroll', 'direction': 'down', 'amount': 3},
        # ]
        # web_driver_utils.perform_robot_actions(actions_list)
        # :param actions_list:
        # :return:
        # """
        for action in actions_list:
            if action['action'] == 'click':
                element = self.get_element(action['by'], action['value'])
                self.click_element_with_robot(element)
            elif action['action'] == 'type':
                element = self.get_element(action['by'], action['value'])
                self.type_with_robot(element, action['text'])
            elif action['action'] == 'scroll':
                self.scroll_with_robot(action['direction'], action['amount'])

            # Add more actions as needed

    # pyautogui: This is the Python library for GUI automation, which includes functions for simulating mouse and
    # keyboard actions. pip install pyautogui

    @staticmethod
    def type_with_robot(self, element, text):
        element.click()
        pyautogui.typewrite(text)

    @staticmethod
    def scroll_with_robot(self, direction, amount):
        if direction == 'up':
            pyautogui.scroll(amount)
        elif direction == 'down':
            pyautogui.scroll(-amount)

    def highlight_element(self, element, color):
        original_style = element.get_attribute("style")
        new_style = "background-color:yellow;border: 1px solid " + color + original_style
        self.driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", element)
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)

    def get_page_source(self):
        return self.driver.page_source

    def assert_element_locator(self, locator, expected_text):
        element = self.get_element(locator)
        actual_text = element.text
        assert expected_text in actual_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'."

    @staticmethod
    def assert_element_text(actual_text, expected_text):
        assert expected_text in actual_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'."

    def assert_element_present(self, locator):
        try:
            self._wait.until(EC.presence_of_element_located(locator))
            assert True, f"Element located by {locator} is present."
        except Exception as e:
            assert False, f"Element located by {locator} is not present. {str(e)}"

    def assert_any_of_text(actual_text, expected_text):
        assert (actual_text in expected_text, f"Actual value should be one of {expected_text}")

    def assert_text_page_source(self, expected_text, locator):
        assert expected_text in self.get_page_source_usingJs(
            locator), f"Expected text '{expected_text}' not found in the page source"

    def validate_grid(self, grid_locator, expected_data):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        actual_data = [cell.text for cell in grid.find_elements(By.TAG_NAME, 'td')]

        assert actual_data == expected_data, f"Grid validation failed. Expected: {expected_data}, Actual: {actual_data}"

    def iterate_grid_rows(self, grid_locator):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            # Process each cell in the row
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                print(cell.text)

    def iterate_grid(self, grid_locator):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')

            for cell in cells:
                print(f"Row: {rows.index(row) + 1}, Column: {cells.index(cell) + 1}, Text: {cell.text}")

    def validate_grid_data(self, grid_locator, expected_data):
        grid = self._wait.until(EC.presence_of_element_located(grid_locator))
        rows = grid.find_elements(By.TAG_NAME, 'tr')

        for row_index, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, 'td')

            for col_index, cell in enumerate(cells):
                actual_data = cell.text
                expected_value = expected_data[row_index][col_index]

                assert actual_data == expected_value, f"Grid validation failed at Row {row_index + 1}, Column {col_index + 1}. Expected: {expected_value}, Actual: {actual_data}"

    def upload_file(self, file_input_locator, file_path):
        file_input = self._wait.until(EC.presence_of_element_located(file_input_locator))
        file_input.send_keys(file_path)

    def get_network_performance(self):
        performance_logs = self.driver.get_log('performance')

        # Read network logs
        network_logs = [json.loads(log['message'])['message'] for log in performance_logs if
                        'Network' in log['message']]

        # Extract network information
        network_info = [entry['params'] for entry in network_logs if 'params' in entry]

        # Extract status codes from network information
        status_codes = [entry['response']['status'] for entry in network_info if 'response' in entry]

        return status_codes

    def current_date(self, formate):
        """
        Fixture to get the current date in the desired format.
        """
        # Customize the desired format here
        if formate == "-":
            date_format = "%Y-%m-%d"
        elif formate == "/":
            date_format = "%m/%d/%Y"
        else:
            date_format = "%m%d%Y"
        current_date = datetime.now().strftime(date_format)
        return current_date

    def read_csv_from_downloads(self, file_name, locator, button):

        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            download_dir = os.path.join(user_profile, 'Downloads')
        else:
            print("Failed to retrieve user profile directory")
            return None
        # Construct the full path to the CSV file
        file_path = os.path.join(download_dir, file_name)

        if os.path.exists(file_path):
            print(f"The '{file_name}' already exists in the Downloads directory. Removing it. ")
            os.remove(file_path)

        print("Downloading CSV file...")
        # define the method in base page and call it here
        self.csv_download_file(locator, button)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print("Error: ", e)
        else:
            print(f"File '{file_name}' not found in Downloads directory.")
            return None

    def csv_download_file(self, locator, button):
        self.clear_text(locator)
        self.send_text(locator, "URL")
        self.click_element(button)
        time.sleep(5)
        pyautogui.hotkey('enter')
        time.sleep(5)

    def connect_database(self, query):
        return self.db.execute_query(query)

    def get_all_rows_columns(self, query):
        logging.info("Validating records from database")
        return self.db.fetch_rows_with_column_names(query)

    def del_records_from_table(self, query):
        logging.info("Deleting records from the table")
        self.db.delete_query(query)

    @staticmethod
    def current_dates(dt_format):
        """
        Fixture to get the current date in the desired format.
        :param dt_format:
        :return:
        """
        # customize the desired format here
        # date format  = "%Y-%m-%d"

        if dt_format == "/":
            date_format = "%Y/%m/%d"
        elif dt_format == "-":
            date_format = "%Y-%m-%d"
        else:
            date_format = "%m%d%Y"
        current_date = datetime.now().strftime(date_format)
        return current_date
