# 📘 Minimal DevOps Knowledge Hub

Welcome to **Minimal DevOps**, an open, structured, and evolving knowledge base powered by **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)**. This repository is a curated set of topics and tools focused on **DevOps, Cloud, System Design, Kubernetes, AI, CICD**, and much more—organized for developers, SREs, platform engineers, and architects.

> 🧠 Designed for productivity, automation, and readability — with tag support, summaries, integrations, and PDF generation.

---

## 🚀 Features

✅ Built with [**MkDocs Material**](https://squidfunk.github.io/mkdocs-material/)

✅ Tags, summaries, and structured navigation using plugins like `meta-manager`, `obsidian-interactive-graph`, `ezlinks`, `blog`, and `macros`

✅ PDF generation, OneNote syncing, and automation scripts included

✅ Beautiful dark/light mode toggle, keyboard-friendly navigation

✅ Ready for both local and hosted deployment

---

## 🔌 Plugins Used

The following MkDocs plugins are configured:

| Plugin | Purpose |
|--------|---------|
| `meta-manager` | Centralized metadata and tag management |
| `tags` | Tag-based navigation |
| `blog` | Blogging support |
| `macros` | Reusable logic and content with external YAML |
| `mkdocs-pdf` | PDF export capabilities |
| `obsidian-interactive-graph` | Interactive graph view for linking |
| `ezlinks` | Obsidian-style wikilinks (e.g., `[[PageName]]`) |

---

## 🎨 Theme & UI Features

- Light/Dark mode toggle
- Autohiding headers
- Tabbed navigation and sections
- Footer with social links
- Inline code copy, annotation, and highlighting
- Search with suggestion, highlight, and share

---

## 🛠 Getting Started Locally

### 1. Install Requirements

```bash
pip install mkdocs-material mkdocs-macros-plugin mkdocs-tags-plugin mkdocs-blog-plugin mkdocs-meta-manager mkdocs-pdf obsidian-interactive-graph mkdocs-ezlinks
```

> (You may also want to `cd mkdocs/` and explore automation tools/scripts there.)

### 2. Serve Locally

```bash
mkdocs serve
```

Then open `http://localhost:8080/` in your browser.

---

## 📦 Extra Enhancements

- ✅ `extra_javascript` and `extra_css` are added for tags + graph rendering
- 📄 `assets/yaml/macro1.yml` is used for macro-driven content
- 📂 PDF files and summaries are supported if `extra.pdf` and `extra.summarized_content` are enabled

---

## 🔗 Social

Stay connected with Minimal DevOps content:

- [GitHub](https://github.com/MinimalDevops/shared-for-you)
- [Medium](https://medium.com/@minimaldevops)
- [LinkedIn](https://www.linkedin.com/company/minimal-devops)

---

## 📄 License

Licensed under the [MIT License](./LICENSE).