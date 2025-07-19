import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from dotenv import load_dotenv

load_dotenv()

BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME')
BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')

BROWSERS = [
    {
        'os': 'Windows', 'osVersion': '10', 'browserName': 'Chrome', 'browserVersion': 'latest', 'sessionName': 'Chrome_Win10'
    },
    {
        'os': 'OS X', 'osVersion': 'Monterey', 'browserName': 'Safari', 'browserVersion': 'latest', 'sessionName': 'Safari_Mac'
    },
    {
        'os': 'Windows', 'osVersion': '10', 'browserName': 'Firefox', 'browserVersion': 'latest', 'sessionName': 'Firefox_Win10'
    },
    {
        'deviceName': 'Samsung Galaxy S22', 'realMobile': 'true', 'osVersion': '12.0', 'sessionName': 'Galaxy_S22', 'browserName': 'Chrome'
    },
    {
        'deviceName': 'iPhone 13', 'realMobile': 'true', 'osVersion': '15', 'sessionName': 'iPhone_13', 'browserName': 'Safari'
    }
]

def get_options(browserName, caps, bstack_options):
    if browserName.lower() == 'chrome':
        options = ChromeOptions()
    elif browserName.lower() == 'firefox':
        options = FirefoxOptions()
    elif browserName.lower() == 'safari':
        options = SafariOptions()
    else:
        options = ChromeOptions()
    # Set all capabilities
    for key, value in caps.items():
        if key != 'sessionName':
            options.set_capability(key, value)
    options.set_capability('bstack:options', bstack_options)
    return options

@pytest.mark.parametrize('caps', BROWSERS)
def test_scraper_on_browserstack(caps):
    bstack_options = {
        'userName': BROWSERSTACK_USERNAME,
        'accessKey': BROWSERSTACK_ACCESS_KEY,
        'sessionName': caps.get('sessionName', 'Test')
    }
    browserName = caps.get('browserName', 'chrome')
    options = get_options(browserName, caps, bstack_options)
    driver = webdriver.Remote(
        command_executor='https://hub-cloud.browserstack.com/wd/hub',
        options=options
    )
    try:
        driver.get('https://elpais.com/opinion/')
        assert 'Opinión' in driver.title or 'Opinion' in driver.title
    finally:
        driver.quit() 