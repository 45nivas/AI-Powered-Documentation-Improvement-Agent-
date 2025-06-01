from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import requests

def fetch_article(url, wait_time=20):
    """
    Fetches and extracts readable content (headings, paragraphs, lists)
    from a given documentation URL using Selenium and BeautifulSoup.
    Returns the content as a single string.
    """
    # Try fetching with requests first
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Check for common verification/captcha phrases
        if "verifying you are human" not in resp.text.lower() and "captcha" not in resp.text.lower():
            # Try to extract main content (update selector as needed)
            main = soup.select_one(".article-body, .article-content, main, .content")
            if not main:
                main = soup.body
            content = []
            for element in main.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
                if element.name in ['h1', 'h2', 'h3']:
                    content.append(f"## {element.get_text(strip=True)}")
                elif element.name == 'p':
                    content.append(element.get_text(strip=True))
                elif element.name in ['ul', 'ol']:
                    items = [li.get_text(strip=True) for li in element.find_all('li')]
                    content.append('\n'.join(f"- {item}" for item in items))
            return "\n\n".join(content)
    except Exception as e:
        print(f"Requests/BeautifulSoup failed: {e}")

    # If requests fails or CAPTCHA detected, fall back to Selenium
    print("Falling back to Selenium (Chrome) due to CAPTCHA or verification...")
    options = Options()
    # Comment out the next line to see the browser and complete verification manually
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-body, .article-content, main, .content"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for selector in [".article-body", ".article-content", "main", ".content"]:
            main = soup.select_one(selector)
            if main:
                break
        else:
            main = soup.body

        content = []
        for element in main.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
            if element.name in ['h1', 'h2', 'h3']:
                content.append(f"## {element.get_text(strip=True)}")
            elif element.name == 'p':
                content.append(element.get_text(strip=True))
            elif element.name in ['ul', 'ol']:
                items = [li.get_text(strip=True) for li in element.find_all('li')]
                content.append('\n'.join(f"- {item}" for item in items))
        return "\n\n".join(content)
    finally:
        driver.quit()

def extract_actionable_suggestions(report_text):
    """
    Extracts all actionable suggestions (bullet points) from the Agent 1 markdown report.
    Returns a string suitable for actionable_suggestions.txt.
    """
    sections = re.findall(r'##\s*\d*\.?\s*([^\n]+)\n+.*?Actionable Suggestions:\s*((?:- .+\n?)+)', report_text, re.DOTALL)
    output = []
    for section, suggestions in sections:
        output.append(f"## {section.strip()}\n")
        output.append(suggestions.strip())
        output.append("")  # Blank line between sections
    return "\n".join(output)