# El País Opinion Scraper & Cross-Browser Automation

## Overview

This project scrapes the first five articles from the "Opinión" (Opinion) section of [El País](https://elpais.com/), a major Spanish news outlet. It extracts the article titles and content in Spanish, downloads cover images, translates the titles to English, analyzes repeated words in the translated headers, and supports automated cross-browser testing using BrowserStack.

---

## Features

- **Web Scraping:** Collects the first five articles from the El País Opinión section.
- **Image Download:** Downloads and saves cover images for each article (if available).
- **Translation:** Translates article titles from Spanish to English using Google Translate.
- **Text Analysis:** Identifies words repeated more than twice in the translated headers.
- **Cross-Browser Testing:** Runs the workflow on BrowserStack across 5 parallel browsers/devices using Selenium and pytest. The BrowserStack test now scrapes and prints the first 5 article titles and content, checks image accessibility, and marks the session as passed only if all 5 articles have non-empty titles, content, and accessible images.

---

## Project Structure

```
final_proj/
├── images/                # Downloaded cover images
├── scraper.py             # Main script for scraping, translation, and analysis
├── test_cross_browser.py  # Automated cross-browser test for BrowserStack
├── requirements.txt       # Python dependencies
├── .gitignore             # Files/folders to ignore in git
├── .env                   # (Not committed) BrowserStack credentials
└── README.md              # This file
```

---

## Local Scraper: How It Works

The main logic is in `scraper.py`:

1. **Open El País Opinión Section:**
   - Uses Selenium to open the Opinión section in a headless Chrome browser.
2. **Extract Articles:**
   - Parses the page with BeautifulSoup to find the first five articles.
   - For each article, extracts the title, link, and cover image URL.
3. **Fetch Article Content:**
   - Navigates to each article page and extracts the main content (paragraphs).
4. **Download Images:**
   - Downloads the cover image (if available) to the `images/` directory.
5. **Translate Titles:**
   - Uses the `googletrans` library to translate each title from Spanish to English.
6. **Analyze Translated Headers:**
   - Tokenizes all translated headers and counts word occurrences.
   - Prints any word that appears more than twice.
7. **Output:**
   - Prints the original and translated titles, content snippets, and image download confirmations.

---

## How to Run Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
python scraper.py
```

- The script will print the scraped article titles, content, and translated headers.
- Downloaded images will appear in the `images/` directory.

---

## Cross-Browser Testing with BrowserStack

### 1. Set Up BrowserStack Credentials

- Create a `.env` file in your project root:
  ```
  BROWSERSTACK_USERNAME=your_browserstack_username
  BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
  ```

### 2. Run the Automated Test

```bash
python -m pytest -n 5 test_cross_browser.py
```

- This will run the test in parallel on 5 browsers/devices via BrowserStack.
- **The test will scrape and print the first 5 article titles and content in each browser/device, check image accessibility, and mark the session as passed only if all 5 articles have non-empty titles, content, and accessible images.**
- You can view the results and videos in your [BrowserStack Automate dashboard](https://automate.browserstack.com/dashboard/v2/builds).
- Each session will be marked as "passed" if all 5 articles are valid, or "failed" otherwise.

---

## Example Output

```
Scraping El País Opinión section...

--- Articles (in Spanish) ---

Article 1:
Title: Un proyecto falto de ambición
Content: ...

Article 2:
Title: Miseria en Cuba
Content: ...

...

--- Translated Headers ---
1. A project lacking ambition
2. Misery in Cuba
...

--- Repeated Words (more than twice) ---

```

**BrowserStack test output:**

```
Article 1:
Title: Un proyecto falto de ambición
Content: ...
Image URL: https://... (Status: 200)
...
```

---

## Notes

- **ChromeDriver** must be installed and in your PATH for local scraping.
- **BrowserStack** free trial required for cross-browser automation.
- **.env** and `images/` are excluded from git via `.gitignore`.
- The code is compatible with Selenium 4.14+ and the latest BrowserStack requirements.

---

## Contributing

Pull requests and suggestions are welcome! If you find a bug or want to add a feature, feel free to open an issue or PR.

---

## License

This project is licensed under the MIT License.
