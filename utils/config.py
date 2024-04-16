import os
from pathlib import Path


class TestData:
    BASE_DIRECTORY = os.getcwd()
    ROOT_PATH = str(Path(__file__).parent.parent)
    BASE_URL = "https://practice.automationtesting.in/"

    # DRIVER
    DRIVER_PATH = os.path.join(BASE_DIRECTORY, 'drivers')  # use os.path.join to create a path
    WEB_DRIVER_WAIT = 60
    HEADLESS = False
    ACTION_DELAY = 2
    DOWNLOAD_WAIT_TIME = 60
    DOWNLOAD_FOLDER = os.path.join(BASE_DIRECTORY, 'results', 'media', 'download')

    # Reporting
    REPORT_TITLE = "Python automation Testing"
    REPORT_FOLDER = os.path.join(BASE_DIRECTORY, 'results', 'reports')
    INDIVIDUAL_REPORT = False
    LOG_FOLDER = os.path.join(BASE_DIRECTORY, 'results', 'logs')

    # Error handling
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    INI_CONFIGS_PATH = os.path.join(ROOT_DIR, "ini_configs")
    DATA_FILES_PATH = os.path.join(ROOT_DIR, "data")
    ALLURE_RESULTS_PATH = os.path.join(ROOT_DIR, "allure-results")

    # Application Test Data
    menu = ['', '']
    drop_down = ['', '']

    # DB Driver details
    HOST = "<host-url"
    USER_NAME = "<usr-name>"
    PASSWORD = "<pwd>"
    PORT = 3422
    DB_NAME = "<database_name"
