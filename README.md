# 📘 MkDocs Automation Toolkit

A collection of Python scripts, templates, and tools to **automate and enhance MkDocs** site generation — including folder structure management, plugin usage, homepage/index page creation, OneNote integration, Medium imports, summaries, and full MkDocs configuration management.

---

## 🗂 Repository Structure

```
.
├── mkdocs/                          # All MkDocs automation scripts
│   ├── mkdocs-plugins/             # Plugin usage and recommendations
│   ├── mkdocs-homepage/            # Generate homepage from recently modified files
│   ├── mkdocs-indexpages/          # Add index.md to each content folder
│   ├── mkdocs-medium/              # Import Medium articles and format as markdown
│   ├── mkdocs-nav-folder-structure/# Sync folder structure with mkdocs.yml nav
│   ├── mkdocs-onenote/             # Upload markdown content to OneNote via Graph API
│   ├── mkdocs-options/             # Automate enhancements in mkdocs.yml
│   └── mkdocs-summary/             # Create section summaries and TOCs
│
├── mkdocs-yml/
│   └── mkdocs.yml                  # Central MkDocs config: theme, nav, plugins, extensions
│
├── samplefiles/                    # Templates: index_sample.md, .meta.yml, contentpage_sample.md
├── .gitignore
├── LICENSE
└── README.md                       # You're here!
```

---

## 🚀 What You Can Do with This Toolkit

- ✅ Build and sync folder structure directly from `mkdocs.yml`
- 🏠 Generate a dynamic homepage with recently modified files
- 📑 Auto-create `index.md` for all major folders
- 📚 Import articles from Medium and format as markdown
- 🧾 Auto-generate markdown summaries and section TOCs
- 🧠 Sync selected notes to OneNote using Microsoft Graph API
- 🔧 Manage and modularize `mkdocs.yml` with YAML macros
- 🗺 Reflect folder structure as `nav:` in `mkdocs.yml`
- 📄 Export PDFs of rendered markdown files

---

## ⚙️ mkdocs.yml – The Brain of This Setup

The core MkDocs configuration is kept in [`mkdocs-yml/mkdocs.yml`](./mkdocs-yml/mkdocs.yml), which:

- 🧭 Defines full site navigation structure
- 🎨 Enables advanced features via [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- 🔌 Loads custom plugins:
  - `meta-manager`, `tags`, `macros`, `pdf`, `blog`, `ezlinks`, `obsidian-interactive-graph`
- 🧠 Pulls in YAML macros from `assets/yaml/` for reusable logic and tags

---

## 📦 Requirements

- Python **3.11+**

Install required packages:

```bash
pip install -r requirements.txt
```

Or manually (common libraries used):

```bash
pip install mkdocs-material pyppeteer requests fpdf yt-dlp whisper msal
```

---

## 🛠 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-repo/mkdocs-automation-toolkit.git
   cd mkdocs-automation-toolkit
   ```

2. **Set up your environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Start local dev server**
   ```bash
   mkdocs serve -f mkdocs-yml/mkdocs.yml
   ```

   Then visit: [http://localhost:8000](http://localhost:8000)

---

## 📚 Documentation Modules

| Folder | Purpose |
|--------|---------|
| `mkdocs-homepage` | Build homepage (`index.md`) from top 5 modified markdown files |
| `mkdocs-indexpages` | Create `index.md` in all content folders with TOC |
| `mkdocs-plugins` | Plugin setup and usage patterns |
| `mkdocs-medium` | Import Medium articles into markdown |
| `mkdocs-summary` | Auto-generate summaries and TOCs per folder |
| `mkdocs-onenote` | Sync `.md` content to OneNote using Microsoft Graph |
| `mkdocs-options` | Automate logic in `mkdocs.yml` using external macros |
| `mkdocs-nav-folder-structure` | Reflect folder/subfolder hierarchy into navigation |
| `mkdocs-yml/` | Main configuration file (`mkdocs.yml`) with nav + theme + plugins |

---

## 🤝 Contributing

Feel free to fork the repo, submit issues, or open PRs. Contributions are always welcome — especially plugin ideas and automation helpers.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.