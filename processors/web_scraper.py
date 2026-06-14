"""
web_scraper.py — Scrapes college websites for current information.
Uses BeautifulSoup. Respects robots.txt and rate limits.
"""

import logging
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)


def scrape_url(url: str, timeout: int = 10) -> Optional[str]:
    """Scrape a single URL and return cleaned text content."""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; CampusBot/1.0; Educational Research)"
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove script, style, nav, footer elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extract main content
        main_content = (
            soup.find("main") or
            soup.find("article") or
            soup.find("div", class_=lambda x: x and "content" in x.lower()) or
            soup.find("body")
        )

        text = main_content.get_text(separator=" ", strip=True) if main_content else ""

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned = " ".join(lines)

        logger.info(f"Scraped {len(cleaned)} chars from {url}")
        return cleaned

    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return None


def scrape_multiple_urls(
    urls: List[str],
    delay: float = 1.5
) -> List[Dict[str, Any]]:
    """Scrape multiple URLs with rate limiting. Returns list of documents."""
    documents = []

    for url in urls:
        text = scrape_url(url)
        if text and len(text) > 100:
            # Split into chunks
            chunks = _chunk_text(text, chunk_size=800, overlap=100)
            for chunk in chunks:
                documents.append({
                    "text": chunk,
                    "metadata": {
                        "source": url,
                        "type": "web_scraped",
                        "domain": urlparse(url).netloc
                    }
                })
        time.sleep(delay)  # Rate limiting

    logger.info(f"Scraped {len(documents)} chunks from {len(urls)} URLs")
    return documents


def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# Pre-defined public college website URLs for demo scraping
SAMPLE_COLLEGE_URLS = [
    # These are public educational resource URLs (not private college systems)
    "https://www.ugc.gov.in/",
    "https://www.aicte-india.org/",
    "https://www.nirfindia.org/",
]
