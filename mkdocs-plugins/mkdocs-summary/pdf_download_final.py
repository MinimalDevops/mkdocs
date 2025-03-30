import os
import re
import asyncio
import subprocess
from pathlib import Path
from pyppeteer import connect
import requests
import time
from hashlib import sha256
import whisper
import yt_dlp
from fpdf import FPDF
import imageio_ffmpeg as ffmpeg
import whisper.audio

# Get the absolute path of the current script's directory
current_dir = Path(__file__).parent.resolve()

# Path to the sample PDF markdown content
SAMPLE_PDF_MD_PATH = 'samplefiles/pdf.md'

def convert_shorts_url(url):
    """Convert YouTube Shorts URL to standard URL."""
    if "youtube.com/shorts/" in url:
        return re.sub(r"/shorts/", "/watch?v=", url)
    return url

def download_audio(youtube_url):
    """Download audio from YouTube using yt_dlp and return the file path."""
    try:
        print("Downloading audio from YouTube...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,
            'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),
            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as filename
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_title = info_dict.get('title', 'video')
            sanitized_title = re.sub(r'[\\/*?\"<>|]', "", video_title)
            ydl_opts['outtmpl'] = f"{sanitized_title}.%(ext)s"  # Ensure sanitized filename
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_inner:
                ydl_inner.download([youtube_url])
            downloaded_file = f"{sanitized_title}.mp3"
            print(f"Audio downloaded to: {downloaded_file}")
            return os.path.abspath(downloaded_file)  # Return the absolute path
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None



def transcribe_audio(audio_path):
    """Transcribe audio using Whisper."""
    # Ensure the audio file exists before processing
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}. Skipping transcription.")
        return None

    wav_path = audio_path.replace('.mp3', '.wav')  # Output WAV file
    try:
        print(f"Transcribing audio using Whisper for file: {audio_path}...")
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

        # Convert MP3 to WAV format
        if os.path.exists(wav_path):
            os.remove(wav_path)  # Remove existing WAV file
        subprocess.run(
            [ffmpeg_path, "-i", audio_path, wav_path],
            check=True
        )

        # Load Whisper model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(wav_path, fp16=False)
        print("Transcription complete.")
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
    finally:
        # Clean up files after processing
        if os.path.exists(audio_path):
            os.remove(audio_path)  # Delete the MP3 file
        if os.path.exists(wav_path):
            os.remove(wav_path)  # Delete the WAV file


def create_pdf(transcription, pdf_path):
    """Create a PDF from the transcription text."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", "/Users/tapinder.singh/Library/Fonts/DejaVu Sans Mono for Powerline.ttf", uni=True)  # Add a Unicode font
        pdf.set_font("DejaVu", size=12)  # Set the Unicode font
        pdf.multi_cell(0, 10, transcription)  # Add the transcription text
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        pdf.output(pdf_path)
        print(f"PDF created at {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error creating PDF: {e}")



async def download_pdf(url, pdf_name, pdf_dir):
    """Download the PDF from the URL."""
    try:
        response = requests.get("http://localhost:9222/json/version")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to connect to Chrome: {e}")
        return

    ws_url = response.json().get("webSocketDebuggerUrl")
    if not ws_url:
        print("WebSocket Debugger URL not found.")
        return

    browser = await connect(browserWSEndpoint=ws_url)
    page = await browser.newPage()
    await page.goto(url)

    # Detect and accept cookies if the popup appears
    try:
        print("Checking for cookie consent popup...")
        cookie_selectors = [
            'button[aria-label="Accept all cookies"]',
            'button[class*="accept"]',  # Generic "accept" button
            'div[class*="cookie"] button',  # Cookie banner button
        ]
        retries = 1
        for _ in range(retries):
            for selector in cookie_selectors:
                try:
                    await page.waitForSelector(selector, timeout=3000)
                    await page.click(selector)
                    print(f"Accepted cookies using selector: {selector}")
                    break
                except Exception as e:
                    print(f"Selector {selector} not found: {e}")
            else:
                continue
            break
        else:
            print("No cookie consent popup found or interaction failed.")
    except Exception as e:
        print(f"Error handling cookie consent: {e}")

    await auto_scroll(page)

    # Ensure the PDF directory exists
    os.makedirs(pdf_dir, exist_ok=True)

    pdf_path = os.path.join(pdf_dir, f"{pdf_name}.pdf")
    if not os.path.exists(pdf_path):
        try:
            await page.pdf({'path': pdf_path, 'format': 'A4', 'printBackground': True})
            print(f"PDF generated successfully at {pdf_path}!")
        except Exception as e:
            print(f"Error generating PDF: {e}")

    await browser.close()


async def auto_scroll(page):
    """Scroll the page to trigger lazy loading."""
    await page.evaluate('''
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                let distance = 100;
                let timer = setInterval(() => {
                    let scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        }
    ''')

def open_chrome_with_profile():
    """Open Chrome with remote debugging."""
    subprocess.Popen([
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--remote-debugging-port=9222',
        '--profile-directory=Profile 2'
    ])
    time.sleep(2)

def generate_pdf_name(url):
    """Generate a PDF name based on the URL."""
    url_parts = url.rstrip('/').split('/')
    pdf_name = url_parts[-1] if url_parts[-1] else url_parts[-2]
    return re.sub(r'[^\w\-_]', '_', pdf_name)

def get_youtube_title(youtube_url):
    """Retrieve the title of a YouTube video without downloading."""
    try:
        print(f"Fetching title for YouTube URL: {youtube_url}")
        ydl_opts = {
            'quiet': True,  # Suppress yt-dlp logs
            'nocheckcertificate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_title = info_dict.get('title', 'video')
            sanitized_title = re.sub(r'[\\/*?\"<>|]', "", video_title)  # Sanitize title
            return sanitized_title
    except Exception as e:
        print(f"Error fetching YouTube title: {e}")
        return None

def process_markdown(md_path):
    """Process markdown files for URLs and YouTube links."""
    with open(md_path, 'r') as file:
        lines = file.readlines()
    
    url_pattern = re.compile(r'(https?://[^\s)]+)')
    youtube_pattern = re.compile(r'(https?://(www\.)?(youtube\.com|youtu\.be)/)')
    modified_lines = []
    existing_content = ''.join(lines)

    for line in lines:
        modified_lines.append(line)
        url_match = url_pattern.search(line)

        # Check if this line has a skip marker
        if url_match and "<!-- skip-url -->" in line:
            print(f"⏭️ Skipping URL: {url_match.group(0)} (Marked as 'skip-url')")
            continue  # Skip this URL
        
        url = url_match.group(0) if url_match else None
        if url:
            # Check for YouTube links
            if youtube_pattern.search(url):
                title = get_youtube_title(url)
                if title:
                    pdf_dir = os.path.join(os.path.dirname(md_path), 'pdf')
                    pdf_path = f"{pdf_dir}/{title}_transcription.pdf"

                    # Check if the PDF already exists
                    if os.path.exists(pdf_path):
                        print(f"Transcription PDF already exists for {title}. Skipping...")
                        continue

                    # If PDF exists but is missing in markdown, add it
                    with open(SAMPLE_PDF_MD_PATH, 'r') as sample_file:
                        pdf_content = sample_file.read().replace("Name.pdf", f"{title}_transcription.pdf")

                    if pdf_content in existing_content:
                        print(f"Markdown entry for {title} already exists. Skipping...")
                        continue

                    if os.path.exists(pdf_path) and pdf_content not in existing_content:
                        print(f"✅ Adding missing PDF reference for: {title}")
                        modified_lines.append(pdf_content + '\n')
                        continue  # No need to download again

                    # If PDF does not exist, process YouTube video
                    if not os.path.exists(pdf_path):
                        audio_path = download_audio(url)
                        if audio_path and os.path.exists(audio_path):
                            transcription = transcribe_audio(audio_path)
                            if transcription:
                                create_pdf(transcription, pdf_path)
                                print(f"📄 PDF created: {pdf_path}")
                                modified_lines.append(pdf_content + '\n')
                continue

            # Skip localhost URLs
            if "localhost" in url or "127.0.0.1" in url or "example.com" in url or "domain.com" in url:
                print(f"⚠️ Skipping localhost URL: {url}")
                continue  

            # Process other URLs for PDFs
            pdf_name = generate_pdf_name(url)
            pdf_dir = os.path.join(os.path.dirname(md_path), 'pdf')
            pdf_path = f"{pdf_dir}/{pdf_name}.pdf"

            # If PDF exists but is missing in markdown, add it
            with open(SAMPLE_PDF_MD_PATH, 'r') as sample_file:
                pdf_content = sample_file.read().replace("Name.pdf", f"{pdf_name}.pdf")
            if os.path.exists(pdf_path) and pdf_content not in existing_content:
                print(f"✅ Adding missing PDF reference for: {pdf_name}")
                modified_lines.append(pdf_content + '\n')
                continue  # No need to download again

            # If PDF does not exist, process the link
            if not os.path.exists(pdf_path):
                open_chrome_with_profile()
                asyncio.run(download_pdf(url, pdf_name, pdf_dir))
                print(f"📄 PDF created: {pdf_path}")
                modified_lines.append(pdf_content + '\n')

    # Write the modified content back to the markdown file
    with open(md_path, 'w') as file:
        file.writelines(modified_lines)


def process_all_markdown_in_directory(directory):
    """Recursively process all markdown files."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                markdown_path = os.path.join(root, file)
                process_markdown(markdown_path)

# Example usage
docs_directory = (current_dir / "../../docs/System Design/Development").resolve()
process_all_markdown_in_directory(docs_directory)
