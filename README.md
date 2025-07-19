# El País Opinion Scraper & Cross-Browser Test

## Features

- Scrapes first 5 articles from El País Opinión section (in Spanish)
- Downloads cover images
- Translates article titles to English
- Analyzes repeated words in translated headers
- Runs cross-browser tests on BrowserStack (5 parallel browsers/devices)

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your BrowserStack credentials (see `.env.example`).

## Usage

### Scrape and Analyze Locally

```bash
python scraper.py
```

### Cross-Browser Testing on BrowserStack

1. Ensure your `.env` is set up.
2. Run tests in parallel:
   ```bash
   pytest -n 5 test_cross_browser.py
   ```

## Notes

- ChromeDriver must be installed and in your PATH for local scraping.
- BrowserStack free trial required for cross-browser automation.
- Images are saved in the `images/` directory.
