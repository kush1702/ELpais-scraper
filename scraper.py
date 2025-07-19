import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from googletrans import Translator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
EL_PAIS_URL = "https://elpais.com/"
OPINION_SECTION = "https://elpais.com/opinion/"
IMAGE_DIR = "images"

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--lang=es')
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_opinion_articles():
    driver = get_driver()
    driver.get(OPINION_SECTION)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select('article')[:5]
    results = []
    for art in articles:
        # Title
        title_tag = art.find(['h2', 'h1'])
        title = title_tag.get_text(strip=True) if title_tag else 'No title'
        # Link
        link_tag = art.find('a', href=True)
        link = link_tag['href'] if link_tag else None
        if link and not link.startswith('http'):
            link = 'https://elpais.com' + link
        # Cover image
        img_tag = art.find('img')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
        # Fetch article content
        content = ''
        if link:
            driver.get(link)
            time.sleep(2)
            article_soup = BeautifulSoup(driver.page_source, 'html.parser')
            paragraphs = article_soup.select('div[data-dtm-region="articulo_cuerpo"] p')
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        # Download image
        img_path = None
        if img_url:
            try:
                img_data = requests.get(img_url).content
                img_name = os.path.join(IMAGE_DIR, os.path.basename(img_url.split('?')[0]))
                with open(img_name, 'wb') as f:
                    f.write(img_data)
                img_path = img_name
            except Exception as e:
                print(f"Failed to download image: {e}")
        results.append({
            'title': title,
            'content': content,
            'img_url': img_url,
            'img_path': img_path
        })
    driver.quit()
    return results

def translate_titles(titles):
    translator = Translator()
    translations = []
    for title in titles:
        try:
            translated = translator.translate(title, src='es', dest='en').text
        except Exception as e:
            translated = f"[Translation failed: {e}]"
        translations.append(translated)
    return translations

def analyze_headers(headers):
    from collections import Counter
    import re
    words = []
    for header in headers:
        words += re.findall(r'\b\w+\b', header.lower())
    counter = Counter(words)
    repeated = {word: count for word, count in counter.items() if count > 2}
    return repeated

def main():
    print("Scraping El País Opinión section...")
    articles = scrape_opinion_articles()
    print("\n--- Articles (in Spanish) ---")
    for i, art in enumerate(articles, 1):
        print(f"\nArticle {i}:")
        print(f"Title: {art['title']}")
        print(f"Content: {art['content'][:500]}...\n")
        if art['img_path']:
            print(f"Cover image saved to: {art['img_path']}")
    # Translate headers
    titles = [a['title'] for a in articles]
    translated = translate_titles(titles)
    print("\n--- Translated Headers ---")
    for i, t in enumerate(translated, 1):
        print(f"{i}. {t}")
    # Analyze
    repeated = analyze_headers(translated)
    print("\n--- Repeated Words (more than twice) ---")
    for word, count in repeated.items():
        print(f"'{word}': {count}")

if __name__ == "__main__":
    main() 