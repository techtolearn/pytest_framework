import pytest
from datetime import datetime
from pathlib import Path
import os
from py.xml import html

from selenium import webdriver
from selenium.common import NoSuchDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from utils.config import TestData


def pytest_addoption(parser):
    """ This function adds a argument to choose the browser """
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="session")
def setup(request):
    """ Here we are doing setup for browser and the url """
    global driver
    services = None
    # Getting the driver name and instantiating the driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": TestData.DOWNLOAD_FOLDER,
            "download.prompt_for_download": False,
            "download,directory_upgrade": True,
            "safebrowsing.enabled": True,
            'w3c': False
        })

        # Set up Chrome DevTools Protocol capabilities
        caps = DesiredCapabilities.CHROME.copy()
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}  # Enable performance logs

        if TestData.HEADLESS:
            chrome_options.add_argument('--headless')

        services = Service(executable_path=f"{TestData.DRIVER_PATH}\chromedriver.exe", options=chrome_options, desired_capabilities=caps)
    elif browser_name == "firefox":
        services = Service(executable_path=f"{TestData.DRIVER_PATH}\geckodriver.exe")
    elif browser_name == "IE":
        services = Service(executable_path=f"{TestData.DRIVER_PATH}\geckodriver.exe")
    try:
        driver = webdriver.Chrome(service=services)
    except NoSuchDriverException:
        print()
        print(*25 * '*', sep='')
        print("\033[1mChrome driver path is correct, please check and update the driver")
        print(*25 * '*', sep='')
    except Exception as e:
        print(e)

    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.close()

    reports_dir = ''


def create_report_folder():
    """ Creates a report folder with the datetime stamp """
    global reports_dir
    # if config is set to create individual report then create individual report with timestamp else create single
    # report
    if TestData.INDIVIDUAL_REPORT:
        reports_dir = Path(TestData.REPORT_FOLDER, datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        reports_dir.mkdir(parents=True, exist_ok=True)
    else:
        reports_dir = Path(TestData.REPORT_FOLDER)
        if not os.path.exists(reports_dir):
            reports_dir.mkdir(parents=True, exist_ok=False)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ Updates the default configurations of pytes """
    # Create the project folder
    create_report_folder()
    # custom report file
    report = reports_dir / "report.html"
    # adjust plugin options (Updating the report path)
    config.option.htmlpath = report
    config.option.self_contained_html = True


def pytest_html_results_table_header(cells):
    """ Adds two columns (Description and time) to the report table """
    cells.insert(2, html.th('Description'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """ Adds row two column values to the row """
    cells.insert(2, html.td("report.description"))
    cells.insert(3, html.td(datetime.now(), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    """ Saves the captured screenshot to the report directory """
    global reports_dir
    # crate the test folder inside the report
    reports_dir = str(Path(reports_dir))
    if not os.path.exists(reports_dir + '/tests'):
        os.makedirs(reports_dir + '/tests')
    # save the screenshot
    try:
        driver.get_screenshot_as_file(reports_dir + '/' + name)
    except Exception as e:
        print(e)


def pytest_html_report_title(report):
    """ Adds title to the report """
    report.title = TestData.REPORT_TITLE
