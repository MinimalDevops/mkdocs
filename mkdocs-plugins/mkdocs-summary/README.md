# 🧠 Auto-PDF Generator from Markdown URLs (YouTube + Web)

This Python script scans all `.md` files in a specified folder (excluding `index.md`), extracts URLs, and does the following:

- 🎥 **YouTube URLs** → Download audio → Transcribe via **Whisper** → Save as PDF → Insert PDF reference into the markdown file.
- 🌐 **Web URLs** → Launches **Headless Chrome** → Renders + scrolls the page → Converts to PDF → Inserts PDF reference into the markdown.
- 🧠 Avoids reprocessing if PDF already exists and is already linked.

---

## 📌 Features

- ✅ Skips URLs with `<!-- skip-url -->`
- 🛑 Skips placeholder URLs like `localhost`, `127.0.0.1`, `example.com`, etc.
- 🔁 Auto-scrolls pages to load lazy content before PDF rendering
- 📄 Inserts a predefined markdown block from `samplefiles/pdf.md` for each processed PDF
- 🧠 Prevents duplicate or redundant processing

---

## 🔧 Prerequisites

### 1. Python Version

- Python **3.11**

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt` example:

```text
requests
pyppeteer
yt-dlp
whisper
fpdf
imageio-ffmpeg
```

Also ensure:
- FFmpeg is installed and accessible in your system PATH.
- Chrome is installed (used with remote debugging).

---

## 🔁 Required Folder Structure

```
your_project/
├── samplefiles/
│   └── pdf.md                        # Markdown block template with placeholder 'Name.pdf'
├── docs/
│   └── System Design/
│       └── Development/
│           └── *.md                  # Markdown files to scan (excluding index.md)
└── scripts/
    └── main_script.py                # This script
```

---

## 🔑 How It Works

| URL Type | Action |
|----------|--------|
| 🎥 YouTube | Downloads audio → Transcribes using Whisper → Creates PDF → Inserts markdown |
| 🌐 Web    | Launches Headless Chrome → Scrolls to load → Renders PDF → Inserts markdown |
| ⛔ Skips | URLs with `<!-- skip-url -->`, or local/placeholder domains |

---

## 💬 Sample Markdown Block Inserted

Taken from `samplefiles/pdf.md` with `Name.pdf` replaced dynamically:

```md
📄 Related PDF: [Video Title_transcription.pdf](pdf/Video Title_transcription.pdf)
```

---

## 🏁 How to Run

### 1. Launch Chrome with Remote Debugging (manually)

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/ChromeDebug"
```

**Windows:**
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
```

> Or let the script do it automatically (it launches Chrome if needed).

### 2. Run the script

```bash
python main_script.py
```

---

## ✨ Example Output

Markdown before:
```md
Check out this video: https://www.youtube.com/watch?v=abcd1234
```

Markdown after:
```md
Check out this video: https://www.youtube.com/watch?v=abcd1234

📄 Related PDF: [MyAwesomeVideo_transcription.pdf](pdf/MyAwesomeVideo_transcription.pdf)
```

---

## 🧠 Notes

- PDFs are saved under a `pdf/` subfolder relative to each `.md` file.
- Whisper uses the `"base"` model. You can change this in the code if needed.
- FFmpeg is used to convert `.mp3` to `.wav` for Whisper input.
- All file names are sanitized to ensure compatibility with filesystems.