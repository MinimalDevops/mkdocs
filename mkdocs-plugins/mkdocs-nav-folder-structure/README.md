# 🏗️ MkDocs Folder and File Structure Generator

This Python script reads the `mkdocs.yml` file, extracts paths ending in `.md` (excluding `index.md` and `tags.md`), and **automatically creates**:

- Necessary folder structures under the `docs/` directory
- Content `.md` files using a provided `contentpage_sample.md`
- `index.md` files in top-level folders using `index_sample.md` with folder name as heading
- `.meta.yml` in each folder and subfolder

---

## 📌 Features

- 🧠 **Parses `mkdocs.yml`** as plain text, no YAML library used
- 📂 **Creates missing directories and markdown files**
- 📄 **Copies sample markdown content** for content and index files
- 🏷️ **Adds `.meta.yml`** to each created folder and its subfolders
- ✅ **Skips existing files** – does not overwrite

---

## 🐍 Requirements

- Python **3.11**
- No external dependencies – uses standard libraries only (`os`, `shutil`, `pathlib`)

---

## 🧩 Required Files and Structure

Make sure the following sample files exist in your project before running the script:

```text
your_project/
├── mkdocs.yml
├── docs/
│   └── (Folders will be created here)
├── samplefiles/
│   ├── .meta.yml                # Metadata template
│   ├── index_sample.md          # Sample for index.md (must contain "# Heading")
│   └── contentpage_sample.md    # Sample content for each .md page
└── scripts/
    └── generate_structure.py    # This script
```

---

## ✏️ What You Should Parameterize Before Running

Ensure the following variables point to the correct locations:

| Variable | Description |
|----------|-------------|
| `mkdocs_file_path` | Path to your `mkdocs.yml` file |
| `docs_base_path` | Root directory for generated content (`docs/`) |
| `meta_file_path` | Path to `.meta.yml` sample file |
| `index_sample_file_path` | Path to `index_sample.md` |
| `content_sample_file_path` | Path to `contentpage_sample.md` |

> These are currently hardcoded to look like `../../mkdocs.yml`, relative to the script location. Adjust if needed.

---

## 🏁 How to Run

```bash
python generate_structure.py
```

It will:

1. Read lines from `mkdocs.yml`
2. Parse file paths ending in `.md` (excluding `index.md` and `tags.md`)
3. Create folder structure under `docs/`
4. Add `.meta.yml` to folders and subfolders
5. Generate content `.md` files from `contentpage_sample.md`
6. Create or skip `index.md` using `index_sample.md`, replacing `# Heading` with folder name

---

## ✅ Output Example

For a line in `mkdocs.yml` like:

```yaml
  - Getting Started: getting-started/intro.md
```

The following is created:

```text
docs/
└── getting-started/
    ├── .meta.yml
    ├── index.md                # Only if not already present
    └── intro.md                # From contentpage_sample.md
```

---

## 🚫 What It Skips

- Files named `index.md` and `tags.md` from `mkdocs.yml`
- Existing files (no overwrites)
- Directories and files with malformed paths in `mkdocs.yml`