# 📚 Auto-Generate `index.md` for Subdirectories in `docs/`

This Python script generates an `index.md` file for each **immediate subfolder** of the `docs/` directory (excluding folders like `images`, `assets`, and `blog`). Each `index.md` lists all markdown (`.md`) files within that subfolder and its subfolders in a **wikilink format**.

---

## 📌 Features

- 🚫 **Ignores specific folders** (`images`, `assets`, `blog`)
- 📂 **Generates `index.md`** in each non-ignored immediate subdirectory of `docs/`
- 🔁 **Recursively scans subfolders** to include all `.md` files (excluding `index.md`)
- 📄 **Keeps existing first line** of `index.md` (if present and starts with `# `)
- 🔗 **Generates wikilinks** in the format: `[[FileName|Heading]]`, where heading is from the first line in the file

---

## 🐍 Requirements

- Python **3.11**
- No third-party packages required – uses only standard Python libraries

---

## 📁 Folder Structure Assumption

```text
your_project/
├── docs/
│   ├── Security/
│   │   ├── index.md           # Auto-generated
│   │   ├── Tools/
│   │   │   └── SecurityToolsTool1.md
│   ├── images/                # Ignored
│   ├── blog/                  # Ignored
│   └── assets/                # Ignored
└── scripts/
    └── your_script.py         # This Python script
```

---

## 🔧 Parameterization Before Running

Please update the following values in the script **before running**:

| Variable | Description | Example |
|----------|-------------|---------|
| `root_dir` | Root directory to scan | `../../docs` |
| `ignored_folders` | Folders to skip from scanning | `{'images', 'assets', 'blog'}` |

---

## 🏁 How to Run

1. **Edit the script** to ensure `root_dir` points to your actual `docs/` directory.
2. Run the script:

```bash
python your_script.py
```

> 💡 Use a virtual environment (e.g., `conda`) with Python 3.11 for isolation:

```bash
conda create -n mdindexgen python=3.11
conda activate mdindexgen
```

---

## 📌 Sample Output (`index.md`)

```md
# Security

- [[SecurityToolsTool1|Tools for Secure Deployment]]
- [[NetworkSecurityChecklist|Network Security Checklist]]
...
```

---

## 🛑 Important Notes

- The script **overwrites** `index.md` in each subfolder.
- The **first line** (title line starting with `# `) of an existing `index.md` is preserved if present.
- Only files with `.md` extension are considered. `index.md` itself is excluded from listings.
