import os
import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

START_URL = "https://www.icici.bank.in/"
OUTPUT_DIR = "icici_cc_pages"
MAX_PAGES = 1000
DELAY_SECONDS = 1

os.makedirs(OUTPUT_DIR, exist_ok=True)

domain = urlparse(START_URL).netloc
robots_url = urljoin(START_URL, "/robots.txt")

rp = RobotFileParser()
rp.set_url(robots_url)
rp.read()

headers = {
    "User-Agent": "Mozilla/5.0 compatible; personal-learning-crawler/1.0"
}

visited = set()
queue = [START_URL]
count = 0


def filename_from_url(url, output_dir):
    path = urlparse(url).path.strip("/")

    if not path:
        name = "home"
    else:
        name = path.split("/")[-1]

    name = re.sub(r"[^a-zA-Z0-9_-]", "-", name)

    filename = os.path.join(output_dir, f"{name}.txt")

    counter = 2
    while os.path.exists(filename):
        filename = os.path.join(output_dir, f"{name}-{counter}.txt")
        counter += 1

    return filename


def clean_text(html):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip(), soup


while queue and count < MAX_PAGES:
    url = queue.pop(0)

    if url in visited:
        continue

    visited.add(url)

    if not rp.can_fetch(headers["User-Agent"], url):
        print(f"Blocked by robots.txt: {url}")
        continue

    try:
        print(f"Crawling: {url}")

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "text/html" not in content_type:
            continue

        text, soup = clean_text(response.text)

        count += 1
        filename = filename_from_url(url, OUTPUT_DIR)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)

        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            parsed = urlparse(next_url)

            next_url = parsed._replace(fragment="").geturl()

            if parsed.netloc != domain:
                continue

                # Only keep credit card pages
            if "credit-card" not in next_url.lower():
                continue

            if next_url not in visited:
                queue.append(next_url)

        time.sleep(DELAY_SECONDS)

    except Exception as e:
        print(f"Error crawling {url}: {e}")

print(f"Done. Saved {count} pages in {OUTPUT_DIR}/")
