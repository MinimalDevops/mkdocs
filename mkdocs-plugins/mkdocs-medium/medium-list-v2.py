import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def attach_to_existing_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_articles(driver):
    articles = set()
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        article_links = soup.find_all("a", class_="ag ah ai aj ak al am an ao ap aq ar as at au")

        for link in article_links:
            try:
                title_tag = link.find("h2")
                description_tag = link.find("h3")
                if title_tag:
                    title = title_tag.get_text()
                    url = link.get("href")
                    if url and url.startswith("/"):
                        url = "https://medium.com" + url
                    description = description_tag.get_text() if description_tag else "No description"
                    articles.add((title, url, description))
            except Exception as e:
                print(f"Error extracting article: {e}")
                continue

        print(f"Found {len(articles)} articles on this page...")
        return list(articles)

    except Exception as e:
        print(f"Error during article extraction: {e}")
        return []

def scroll_to_load(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 0
    max_retries = 5

    while retries < max_retries:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            retries += 1
            print(f"No new content loaded. Retry {retries}/{max_retries}")
            if retries == max_retries:
                break
        else:
            last_height = new_height
            retries = 0

def sanitize_filename_from_url(url):
    parts = url.split("/")
    parts = [p for p in parts if p and not p.startswith("http") and p != "list"]
    filename = "_".join(parts[-2:]) if len(parts) > 1 else parts[0]
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    return filename + ".md"

def save_to_markdown(articles, filename, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("# Medium Articles\n\n")
        for idx, (title, link, description) in enumerate(articles, 1):
            file.write(f"### {idx}. [{title}]({link})\n")
            file.write(f"*{description}*\n\n")

    print(f"✅ Articles saved to {output_path}")

def main():
    print("Attaching to the existing browser session...")
    driver = attach_to_existing_browser()

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        urls_file = os.path.join(script_dir, "urls.txt")
        output_dir = os.path.join(script_dir, "output")

        with open(urls_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        for url in urls:
            print(f"\n🔍 Processing: {url}")
            driver.get(url)
            time.sleep(5)

            scroll_to_load(driver)
            articles = extract_articles(driver)

            print(f"Total Articles Found: {len(articles)}")

            filename = sanitize_filename_from_url(url)
            save_to_markdown(articles, filename, output_dir)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
