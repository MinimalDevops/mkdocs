# 📰 Medium Article Extractor with Selenium

This Python script attaches to an **existing Chrome browser session**, navigates to a Medium reading list, scrolls to load content dynamically, extracts articles (titles, URLs, and descriptions), and saves the information in a neatly formatted `medium_articles.md` file.

---

## 📌 Features

- 🔗 **Connects to an existing Chrome browser session** running with `--remote-debugging-port=9222`
- 📜 **Extracts article titles, links, and descriptions** using `BeautifulSoup`
- 🔁 **Scrolls the Medium page** to load additional articles dynamically
- 📄 **Outputs a Markdown file** with clickable links and short descriptions

---

## 🐍 Requirements

- Python **3.11**
- Google Chrome running with `--remote-debugging-port=9222`
- The following Python packages:

### Install via pip:
```bash
pip install selenium webdriver-manager beautifulsoup4
```

> 💡 It's recommended to use a virtual environment (e.g., `conda`):
```bash
conda create -n medium-scraper python=3.11
conda activate medium-scraper
pip install selenium webdriver-manager beautifulsoup4
```

---

## 🛠 Required Setup Before Running

Before executing the script, **manually start Chrome** using the following command (or a shortcut with this flag):

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
```

> On macOS or Linux, the command will look like:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/ChromeDebug"
```

This enables the script to attach to the existing browser session using the debugging port.

---

## 🧩 Parameterization

You **must update the Medium reading list URL** in the script before running:

```python
url = "https://medium.com/@minimaldevops/list/reading-list"
```

Replace this with your own Medium list or collection URL if needed.

---

## 🏁 How to Run

1. Start Chrome with `--remote-debugging-port=9222`
2. Run the script:

```bash
python medium_list.py
```

---

## 📄 Output Format (medium_articles.md)

```md
# Medium Articles

### 1. [The Future of DevOps](https://medium.com/...)  
*How AI is changing DevOps forever*

### 2. [Policy-as-Code Demystified](https://medium.com/...)  
*A simple intro to Open Policy Agent (OPA)*

...
```

## 🏁 How to Run V2

1. Start Chrome with `--remote-debugging-port=9222`
2. Save all the URLs in a file `urls.txt` under the same folder.
3. Run the script:

```bash
python medium_list-v2.py
```

---

## 📄 Output Format (medium_articles.md)

An `output` directory will be created which will contain individual files for each URL.

```md
# Medium Articles

### 1. [The Future of DevOps](https://medium.com/...)  
*How AI is changing DevOps forever*

### 2. [Policy-as-Code Demystified](https://medium.com/...)  
*A simple intro to Open Policy Agent (OPA)*

...
```

---

## 🔄 What It Does Under the Hood

| Function | Purpose |
|---------|---------|
| `attach_to_existing_browser()` | Connects to an existing Chrome session using remote debugging |
| `scroll_to_load()` | Automatically scrolls the Medium page to load all articles |
| `extract_articles()` | Parses the HTML to collect article titles, URLs, and descriptions |
| `save_to_markdown()` | Writes the extracted data to `medium_articles.md` |
| `main()` | Orchestrates the entire workflow |

---

## 🛑 Notes

- This script **does not launch a new browser**, it connects to an existing one.
- Ensure you **open the browser and are logged into Medium** before running the script.
- The script uses class names to locate article links – if Medium changes their structure, this may need to be updated.
