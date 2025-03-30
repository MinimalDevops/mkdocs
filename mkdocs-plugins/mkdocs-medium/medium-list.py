import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def attach_to_existing_browser():
    """Attach to an existing Chrome browser session."""
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_articles(driver):
    """Extract articles with their titles and URLs."""
    articles = set()
    try:
        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all article links
        article_links = soup.find_all("a", class_="ag ah ai aj ak al am an ao ap aq ar as at au")

        for link in article_links:
            try:
                # Extract the title from the nested <h2> tag
                title_tag = link.find("h2")
                description_tag = link.find("h3")
                if title_tag:
                    title = title_tag.get_text()
                    url = link.get("href")
                    # Handle relative URLs
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
    """Scroll and load articles."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    retries = 0
    max_retries = 5

    while retries < max_retries:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give some time for new articles to load
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            retries += 1
            print(f"No new content loaded. Retry {retries}/{max_retries}")
            if retries == max_retries:
                break
        else:
            last_height = new_height
            retries = 0

def save_to_markdown(articles):
    """Save the articles to a Markdown file."""
    with open("medium_articles.md", "w", encoding="utf-8") as file:
        file.write("# Medium Articles\n\n")
        for idx, (title, link, description) in enumerate(articles, 1):
            file.write(f"### {idx}. [{title}]({link})\n")
            file.write(f"*{description}*\n\n")
    print("\nArticles saved to medium_articles.md")

def main():
    print("Attaching to the existing browser session...")
    driver = attach_to_existing_browser()

    try:
        url = "https://medium.com/@minimaldevops/list/reading-list"
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        print("Scrolling to load all articles...")
        scroll_to_load(driver)

        print("Extracting articles...")
        articles = extract_articles(driver)

        print(f"\nTotal Articles Found: {len(articles)}")
        for idx, (title, link, description) in enumerate(articles, 1):
            print(f"{idx}. {title} - {link}")
            print(f"   Description: {description}\n")

        save_to_markdown(articles)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
