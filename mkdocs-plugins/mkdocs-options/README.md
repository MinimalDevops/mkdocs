# 🧩 Markdown Snippet Generator for VSCode from `mkdocs.yml`

This Python script reads paths from your `mkdocs.yml`, filters out markdown file entries (excluding `index.md` and `tags.md`), and generates a **VSCode snippet** JSON block for use in your Markdown editing workflow.

---

## 📌 Features

- 🗃️ Parses `mkdocs.yml` to extract all `.md` file paths
- 🧼 Skips `index.md` and `tags.md` to focus only on content pages
- 🔄 Converts file names to a `|`-separated list (used in VSCode snippet dropdowns)
- 🧠 Outputs a **pre-formatted VSCode snippet block**, ready to be pasted in `snippets/markdown.json`

---

## 🐍 Requirements

- Python **3.11**
- No external libraries required – only uses Python's standard `pathlib`

---

## 🧩 Example VSCode Snippet Output

The script prints something like:

```json
"md.command10": {
    "scope": "markdown",
    "prefix": "mdreplace",
    "body": [
        "[[${2|intro,getting-started,api-reference|}|${TM_SELECTED_TEXT:${1}}]]"
    ],
    "description": "Replace selected text with one of the predefined options"
},
```

Use this in your `markdown.json` snippet file to quickly wrap selected text with a Wiki-style link using a dropdown of available markdown pages.

---

## ✏️ Parameters You Might Change

| Variable | Description |
|----------|-------------|
| `file_path` | Path to `mkdocs.yml` file (relative to script location) |

Default value:

```python
file_path = (current_dir / "../../mkdocs.yml").resolve()
```

Make sure this points to your actual `mkdocs.yml`.

---

## 🏁 How to Run

```bash
python generate_snippet.py
```

The script will:

1. Read your `mkdocs.yml`
2. Extract file names like `intro.md`, `api-reference.md`, etc.
3. Format them into a snippet dropdown list: `intro,api-reference,...`
4. Output a ready-to-paste VSCode snippet block

---

## 🧼 File Structure Example

```text
your_project/
├── mkdocs.yml
└── scripts/
    └── generate_snippet.py
```

---

## 💡 Tip: Where to Paste the Output

Paste the snippet block into:

```bash
.vscode/
└── snippets/
    └── markdown.json
```

> Don’t forget to reload VSCode after adding the snippet.

---

## 🛑 Error Handling

- If `mkdocs.yml` is not found, the script creates an informative message
- General exceptions are caught and logged with details