import os
import pytest
import requests
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
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
        )
        articles = driver.find_elements(By.CSS_SELECTOR, 'article')[:5]
        results = []
        all_ok = True
        for idx, art in enumerate(articles, 1):
            try:
                title = art.find_element(By.CSS_SELECTOR, 'h2, h1').text.strip()
            except Exception:
                title = ''
            try:
                link = art.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except Exception:
                link = None
            try:
                img_url = art.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            except Exception:
                img_url = None
            content = ''
            if link:
                try:
                    driver.execute_script("window.open(arguments[0]);", link)
                    driver.switch_to.window(driver.window_handles[-1])
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-dtm-region="articulo_cuerpo"] p'))
                    )
                    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div[data-dtm-region="articulo_cuerpo"] p')
                    content = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except Exception:
                    content = ''
                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            # Check image URL
            img_status = None
            if img_url:
                try:
                    resp = requests.get(img_url, timeout=10)
                    img_status = resp.status_code
                except Exception:
                    img_status = None
            results.append({
                'title': title,
                'content': content,
                'img_url': img_url,
                'img_status': img_status
            })
            # Validation
            if not title or not content or img_status != 200:
                all_ok = False
        # Print results
        for i, res in enumerate(results, 1):
            print(f"\nArticle {i}:")
            print(f"Title: {res['title']}")
            print(f"Content: {res['content'][:300]}...\n")
            print(f"Image URL: {res['img_url']} (Status: {res['img_status']})")
        if all_ok:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Scraped 5 articles with titles, content, and images"}}')
        else:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "One or more articles missing title, content, or image"}}')
            assert False, "One or more articles missing title, content, or image"
    except Exception as e:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Test failed: %s"}}' % str(e))
        raise
    finally:
        driver.quit() 