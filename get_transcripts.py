"""
get_transcripts.py

Downloads YouTube transcripts via the Supadata API and saves each one as a
Markdown file under research/youtube-transcripts/.

File naming: author-name_video-title.md

Usage
-----
1. Edit the VIDEOS list below and run:
       python get_transcripts.py

2. Or pass URLs directly as CLI arguments (author defaults to "unknown"):
       python get_transcripts.py https://youtu.be/abc123 https://youtu.be/xyz789

3. Or pipe a file of URLs (one per line):
       python get_transcripts.py urls.txt
"""

import os
import re
import sys

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_KEY = "sd_d229f623faf34c043f21f7b42bbf0a37"
TRANSCRIPT_ENDPOINT = "https://api.supadata.ai/v1/youtube/transcript"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research", "youtube-transcripts")

# Populate this list with the videos you want to download.
# Each entry needs a "url" and an "author" (channel / expert name).
VIDEOS = [
    # Dave Gerhardt
    {"url": "https://www.youtube.com/watch?v=QAmBbjxeU3w", "author": "Dave Gerhardt"},
    {"url": "https://www.youtube.com/watch?v=mnJL8lWJS5Y", "author": "Dave Gerhardt"},
    # Instantly
    {"url": "https://www.youtube.com/watch?v=ckcSuk5e7WU", "author": "Instantly"},
    {"url": "https://www.youtube.com/watch?v=Yl_0pSSiEVs", "author": "Instantly"},
    {"url": "https://www.youtube.com/watch?v=HDIyDUSh1wA", "author": "Instantly"},
    # Adam Robinson
    {"url": "https://www.youtube.com/watch?v=3wjL3IATsyg", "author": "Adam Robinson"},
    {"url": "https://www.youtube.com/watch?v=RK1Kk1h783c", "author": "Adam Robinson"},
    {"url": "https://www.youtube.com/watch?v=ACMED_IDZb8", "author": "Adam Robinson"},
    # Alex Hormozi
    {"url": "https://www.youtube.com/watch?v=OpeN4O5myIg", "author": "Alex Hormozi"},
    {"url": "https://www.youtube.com/watch?v=pLhQOYMGa88", "author": "Alex Hormozi"},
    # HubSpot Marketing
    {"url": "https://www.youtube.com/watch?v=zw-nBnWbQD4", "author": "HubSpot Marketing"},
    {"url": "https://www.youtube.com/watch?v=qYzmG_7nx3Y", "author": "HubSpot Marketing"},
    {"url": "https://www.youtube.com/watch?v=Yu_jdy-0SOc", "author": "HubSpot Marketing"},
    {"url": "https://www.youtube.com/watch?v=dRTt69nCFlo", "author": "HubSpot Marketing"},
    {"url": "https://www.youtube.com/watch?v=3i2binoTuFk", "author": "HubSpot Marketing"},
    # Russell Brunson
    {"url": "https://www.youtube.com/watch?v=4Umi3PZlJeE", "author": "Russell Brunson"},
    {"url": "https://www.youtube.com/watch?v=dPA7643lbk4", "author": "Russell Brunson"},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert a string to a lowercase, hyphen-separated slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def get_video_title(url: str) -> str:
    """
    Fetch the video title by scraping the YouTube page.
    Falls back to 'unknown-title' if the request fails.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        match = re.search(r"<title>(.+?) - YouTube</title>", response.text)
        if match:
            return match.group(1).strip()
        # Fallback: og:title meta tag
        match = re.search(r'<meta name="title" content="([^"]+)"', response.text)
        if match:
            return match.group(1).strip()
    except requests.RequestException as exc:
        print(f"  Warning: could not fetch video title — {exc}")
    return "unknown-title"


def fetch_transcript(url: str) -> dict:
    """Call the Supadata API and return the parsed JSON response."""
    headers = {"x-api-key": API_KEY}
    params = {"url": url}
    response = requests.get(
        TRANSCRIPT_ENDPOINT, headers=headers, params=params, timeout=60
    )
    response.raise_for_status()
    return response.json()


def extract_text(data: dict) -> str:
    """
    Normalise the Supadata response into plain text regardless of format.
    Handles both flat-text and segmented responses.
    """
    if not isinstance(data, dict):
        return str(data)

    # Plain-text content field
    if "content" in data and isinstance(data["content"], str):
        return data["content"]

    # Segmented transcript (list of {"text": ..., "start": ..., "duration": ...})
    if "transcript" in data and isinstance(data["transcript"], list):
        segments = data["transcript"]
        return "\n".join(seg.get("text", "").strip() for seg in segments if seg.get("text"))

    # Generic "text" field
    if "text" in data and isinstance(data["text"], str):
        return data["text"]

    # Last resort: dump the whole response
    import json
    return json.dumps(data, indent=2)


def save_transcript(author: str, title: str, content: str, url: str) -> str:
    """Write the transcript to a Markdown file and return the file path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"{slugify(author)}_{slugify(title)}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(f"# {title}\n\n")
        fh.write(f"**Channel / Author:** {author}  \n")
        fh.write(f"**Source:** {url}  \n\n")
        fh.write("---\n\n")
        fh.write(content.strip())
        fh.write("\n")

    return filepath


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def load_videos_from_args(args: list[str]) -> list[dict]:
    """
    Accept either:
    - A single .txt file path containing one URL per line
    - One or more YouTube URLs directly
    """
    if len(args) == 1 and args[0].endswith(".txt"):
        try:
            with open(args[0], encoding="utf-8") as fh:
                urls = [line.strip() for line in fh if line.strip()]
        except OSError as exc:
            print(f"Error reading file: {exc}")
            sys.exit(1)
    else:
        urls = args

    return [{"url": u, "author": "unknown"} for u in urls]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    videos = VIDEOS

    # CLI override
    if len(sys.argv) > 1:
        videos = load_videos_from_args(sys.argv[1:])
        if not videos:
            print("No URLs found. Exiting.")
            sys.exit(1)

    if not videos:
        print(
            "No videos configured.\n"
            "Add entries to the VIDEOS list in this script, or pass URLs as arguments.\n"
            "Example:\n"
            "  python get_transcripts.py https://www.youtube.com/watch?v=abc123"
        )
        sys.exit(0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}\n")

    success, failed = 0, 0

    for i, video in enumerate(videos, start=1):
        url = video.get("url", "").strip()
        author = video.get("author", "unknown").strip() or "unknown"

        if not url:
            print(f"[{i}/{len(videos)}] Skipping entry with no URL.")
            continue

        print(f"[{i}/{len(videos)}] {author} — {url}")

        # 1. Resolve video title
        print("  Fetching video title...")
        title = get_video_title(url)
        print(f"  Title: {title}")

        # 2. Download transcript
        print("  Fetching transcript...")
        try:
            data = fetch_transcript(url)
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            body = exc.response.text[:300] if exc.response is not None else ""
            print(f"  Error {status} from Supadata API: {body}")
            failed += 1
            continue
        except requests.RequestException as exc:
            print(f"  Network error: {exc}")
            failed += 1
            continue

        # 3. Extract and save
        content = extract_text(data)
        if not content.strip():
            print("  Warning: transcript appears to be empty.")

        filepath = save_transcript(author, title, content, url)
        print(f"  Saved → {filepath}")
        success += 1

    print(f"\nDone. {success} saved, {failed} failed.")


if __name__ == "__main__":
    main()
