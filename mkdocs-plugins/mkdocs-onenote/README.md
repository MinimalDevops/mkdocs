# 📝 Push Local Markdown Content to Microsoft OneNote using Graph API

This Python script authenticates with **Microsoft Graph API**, checks for a specific **OneNote notebook and section**, and creates a **OneNote page** using the contents of a local markdown file (`index.md`).

---

## 📌 Features

- 🔐 Interactive login with Microsoft personal accounts via `msal`
- 📒 Checks if a notebook/section exists, creates them if not
- 📄 Reads local markdown file (`index.md`) and converts it to **OneNote-compatible HTML**
- 🧾 Posts content as a new page to OneNote via Graph API

---

## 🧑‍💻 Pre-Requirements

### ✅ Microsoft Azure App Registration
Before running this script, you must:

1. Register a new application at [https://portal.azure.com](https://portal.azure.com)
2. Note down:
   - **Client ID**
   - **Redirect URI** (e.g., `http://localhost`)
3. Under **Authentication**, allow `Mobile and desktop applications`
4. Under **API permissions**, add the following **delegated** permissions:
   - `User.Read`
   - `Files.ReadWrite`
   - `Notes.ReadWrite`
5. **Admin consent** may be required

---

## 🐍 Python Environment

### ✅ Python Version: `3.11`

### 📦 Required Libraries:

Install using pip:

```bash
pip install msal requests
```

Or with `conda`:

```bash
conda create -n onenote-uploader python=3.11
conda activate onenote-uploader
pip install msal requests
```

---

## 🔧 Parameters to Update Before Running

Edit the following variables in your script:

| Variable         | Description                              |
|------------------|------------------------------------------|
| `CLIENT_ID`      | Your Azure application's Client ID       |
| `SCOPES`         | Required Microsoft Graph scopes          |
| `AUTHORITY`      | Use `https://login.microsoftonline.com/consumers` for personal accounts |
| `REDIRECT_URI`   | Should match the one configured in Azure |
| `FILE_PATH`      | Path to the local file (default: `index.md`) |
| `NOTEBOOK_NAME`  | OneNote notebook name (e.g., `"My Notes"`) |
| `SECTION_NAME`   | Section name under the notebook          |
| `PAGE_TITLE`     | Title of the new page in OneNote         |

---

## 🏁 How to Run

```bash
python onenote_uploader.py
```

When prompted, a browser window will open for you to log in and grant access. Upon successful authentication, the script will:

1. Read content from `index.md`
2. Create or reuse the specified OneNote notebook and section
3. Upload the content as a formatted HTML page

---

## 📄 Sample Output (in OneNote)

- Page Title: `test6`
- Content:
  ```
  # Default Content
  (or whatever is in index.md, formatted in OneNote)
  ```

---

## 🛑 Notes

- If `index.md` doesn’t exist, the script will create it with default content.
- You must be logged into a **Microsoft personal account**, not a work/school account (based on the consumer authority).
- The Graph API enforces rate limits and token expiration – sessions may expire after a while.

---

## 🧼 Example File Structure

```text
your_project/
├── onenote_uploader.py
├── index.md           # Content source (created if not present)
```