"""
Scraper Agent — fetches new PDFs from RBI, SEBI, MCA websites.
Uses BeautifulSoup + requests. Falls back to sample data if sites are unreachable.
"""
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

REGULATOR_URLS = {
    "RBI":  "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
    "SEBI": "https://www.sebi.gov.in/legal/circulars",
    "MCA":  "https://www.mca.gov.in/MinistryV2/acts-rules.html",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RegIntelBot/1.0)"
}

def fetch_new_pdfs():
    """
    Scrape regulator sites for PDF links.
    Returns list of (source_name, pdf_url) tuples.
    """
    pdf_urls = []
    for name, base_url in REGULATOR_URLS.items():
        try:
            res = requests.get(base_url, headers=HEADERS, timeout=12)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.lower().endswith(".pdf"):
                    full_url = (
                        href if href.startswith("http")
                        else base_url.rsplit("/", 1)[0] + "/" + href.lstrip("/")
                    )
                    pdf_urls.append((name, full_url))
        except Exception as e:
            print(f"[ScraperAgent] Could not fetch {name}: {e}")
    return pdf_urls


def download_pdf(name: str, url: str, dest_folder: str = "data/raw_docs"):
    """Download a PDF file from url into dest_folder."""
    os.makedirs(dest_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}_{os.path.basename(url)}"
    local_path = os.path.join(dest_folder, filename)
    try:
        res = requests.get(url, headers=HEADERS, timeout=25)
        res.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(res.content)
        print(f"[ScraperAgent] Downloaded {name}: {url} → {local_path}")
        return local_path
    except Exception as e:
        print(f"[ScraperAgent] Error downloading {url}: {e}")
        return None
