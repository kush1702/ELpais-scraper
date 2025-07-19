import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        # Wait for articles to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
        )
        articles = driver.find_elements(By.CSS_SELECTOR, 'article')
        titles = []
        for art in articles[:5]:
            try:
                title = art.find_element(By.CSS_SELECTOR, 'h2, h1').text
            except Exception:
                title = ''
            titles.append(title)
        print("Scraped article titles:")
        for i, t in enumerate(titles, 1):
            print(f"{i}. {t}")
        if len([t for t in titles if t.strip()]) >= 5:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Scraped 5 article titles successfully"}}')
        else:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Could not scrape 5 article titles"}}')
            assert False, "Could not scrape 5 article titles"
    except Exception as e:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Test failed: %s"}}' % str(e))
        raise
    finally:
        driver.quit() 