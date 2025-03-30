# 📝 Auto-Generate `index.md` for Recently Modified Markdown Files

This Python script scans a specified folder (default: `../../docs/`), identifies the five most recently modified `.md` (Markdown) files (excluding `index.md`), and creates or overwrites an `index.md` file by appending:
- Predefined content from `home.md`
- A list of recently updated files, linking the filename with its title.

---

## 📌 Features

- 📂 **Scans folders recursively** to find `.md` files (excluding `index.md`)
- 🕒 **Sorts files by last modified time**
- 📄 **Extracts headings** from each file (first line starting with `# `)
- ✍️ **Generates a markdown list** in the format `[[FileName|Heading]]`
- 🧩 **Appends it to the content of `home.md`**
- 🗂 **Outputs it to a new or existing `index.md`**

---

## 🐍 Requirements

- Python **3.11**
- No external libraries required (uses only standard libraries)

---

## 📁 Folder Structure Assumption

```text
your_project/
├── samplefiles/
│   └── home.md               # Content to prepend
├── docs/
│   └── index.md              # Will be overwritten
│   └── other_markdowns.md    # Markdown files to be scanned
└── scripts/
    └── your_script.py        # This Python script
```

---

## 🔧 Parameterization and Setup

Update the following paths in your script **before running**:

| Variable | Description | Example |
|----------|-------------|---------|
| `folder_path` | Folder containing `.md` files to scan | `../../docs/` |
| `output_path` | Path to write the final `index.md` | `../../docs/index.md` |
| `home_file_path` | Path to `home.md` file | `../../samplefiles/home.md` |

Change them to your own paths if your directory structure differs.

---

## 🏁 How to Run

1. **Clone or copy the script** to your project
2. **Edit the script** to provide correct paths (see above)
3. Run the script:

```bash
python your_script.py
```

> Ensure you're running it using Python 3.11. If you're using `conda`, create an environment like this:

```bash
conda create -n mdindexer python=3.11
conda activate mdindexer
```

---

## 🧼 Note

This script **overwrites `index.md`**. Be sure to back it up if you don’t want to lose previous content.

---

## ✅ Sample Output in `index.md`

```md
# Welcome to My Docs

# Latest Modified Files

1. [[api_reference|API Reference]]
2. [[getting_started|Getting Started]]
3. [[troubleshooting|Troubleshooting]]
...
```