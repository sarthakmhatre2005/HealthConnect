import os
import re
import csv
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from collections import deque

# ============================================================
# WEBSITE CRAWLER + DATA SCRAPER
# ============================================================

print("=" * 70)
print("             WEBSITE DATA CRAWLER & SCRAPER")
print("=" * 70)

START_URL = input("\nEnter website URL: ").strip()

if not START_URL.startswith(("http://", "https://")):
    START_URL = "https://" + START_URL

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

MAX_PAGES = 5000
REQUEST_DELAY = 0.5
TIMEOUT = 15

OUTPUT_DIR = "scraped_website"
PAGES_DIR = os.path.join(OUTPUT_DIR, "pages")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}

# ------------------------------------------------------------
# Domain setup
# ------------------------------------------------------------

parsed_start = urlparse(START_URL)

BASE_DOMAIN = parsed_start.netloc.lower()
BASE_DOMAIN = BASE_DOMAIN.replace("www.", "")

START_URL = urldefrag(START_URL)[0]

# ------------------------------------------------------------
# Storage
# ------------------------------------------------------------

visited = set()
queued = set()
all_pages = []
all_images = []

queue = deque([START_URL])
queued.add(START_URL)

session = requests.Session()
session.headers.update(HEADERS)

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def normalize_url(url):
    """
    Normalize URL by removing fragments and unnecessary spaces.
    """

    url = urldefrag(url)[0]
    url = url.strip()

    return url


def is_internal(url):
    """
    Check whether URL belongs to the same website/domain.
    """

    try:
        domain = urlparse(url).netloc.lower()
        domain = domain.replace("www.", "")

        return domain == BASE_DOMAIN

    except Exception:
        return False


def safe_filename(value, max_length=100):
    """
    Convert URL/text into a filesystem-safe filename.
    """

    value = re.sub(r'[<>:"/\\|?*]', "_", value)
    value = value.strip()

    if not value:
        value = "page"

    return value[:max_length]


def url_hash(url):
    """
    Generate unique hash for URLs.
    """

    return hashlib.sha256(url.encode()).hexdigest()[:12]


def get_image_extension(url, response=None):
    """
    Determine image extension.
    """

    parsed = urlparse(url)
    path = parsed.path.lower()

    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".bmp",
        ".tiff",
        ".ico"
    ]

    for ext in extensions:
        if path.endswith(ext):
            return ext

    if response:

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "jpeg" in content_type:
            return ".jpg"

        if "png" in content_type:
            return ".png"

        if "gif" in content_type:
            return ".gif"

        if "webp" in content_type:
            return ".webp"

        if "svg" in content_type:
            return ".svg"

    return ".img"


def extract_image_urls(soup, page_url):
    """
    Extract images from:
    - img src
    - img data-src
    - srcset
    - picture/source
    """

    images = set()

    # <img>
    for img in soup.find_all("img"):

        src = img.get("src")

        if src:
            images.add(
                urljoin(page_url, src)
            )

        data_src = img.get("data-src")

        if data_src:
            images.add(
                urljoin(page_url, data_src)
            )

        srcset = img.get("srcset")

        if srcset:

            for item in srcset.split(","):

                image_url = item.strip().split(" ")[0]

                if image_url:
                    images.add(
                        urljoin(page_url, image_url)
                    )

    # <source>
    for source in soup.find_all("source"):

        src = source.get("src")

        if src:
            images.add(
                urljoin(page_url, src)
            )

        srcset = source.get("srcset")

        if srcset:

            for item in srcset.split(","):

                image_url = item.strip().split(" ")[0]

                if image_url:
                    images.add(
                        urljoin(page_url, image_url)
                    )

    return images


def download_image(image_url, page_url):
    """
    Download an image.
    """

    try:

        if not is_internal(image_url):
            return None

        response = session.get(
            image_url,
            timeout=TIMEOUT,
            stream=True
        )

        if response.status_code != 200:
            return None

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if not content_type.startswith("image/"):
            return None

        extension = get_image_extension(
            image_url,
            response
        )

        filename = (
            url_hash(image_url)
            + extension
        )

        filepath = os.path.join(
            IMAGES_DIR,
            filename
        )

        if not os.path.exists(filepath):

            with open(filepath, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=8192
                ):

                    if chunk:
                        file.write(chunk)

        return {
            "image_url": image_url,
            "source_page": page_url,
            "local_file": filepath
        }

    except Exception as error:

        print(
            f"   [IMAGE ERROR] {image_url} -> {error}"
        )

        return None


def extract_page_data(soup, page_url):
    """
    Extract as much useful structured data as possible.
    """

    # Remove scripts/styles from text extraction
    for tag in soup(
        ["script", "style", "noscript", "svg"]
    ):
        tag.decompose()

    title = ""

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True
        )

    description = ""

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description:
        description = meta_description.get(
            "content",
            ""
        )

    headings = {}

    for level in range(1, 7):

        headings[f"h{level}"] = [
            heading.get_text(
                " ",
                strip=True
            )
            for heading in soup.find_all(
                f"h{level}"
            )
        ]

    paragraphs = [
        p.get_text(
            " ",
            strip=True
        )
        for p in soup.find_all("p")
        if p.get_text(strip=True)
    ]

    links = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href:

            absolute_url = normalize_url(
                urljoin(page_url, href)
            )

            links.append({
                "text": link.get_text(
                    " ",
                    strip=True
                ),
                "url": absolute_url
            })

    # Tables
    tables = []

    for table in soup.find_all("table"):

        rows = []

        for row in table.find_all("tr"):

            cells = row.find_all(
                ["th", "td"]
            )

            rows.append([
                cell.get_text(
                    " ",
                    strip=True
                )
                for cell in cells
            ])

        if rows:
            tables.append(rows)

    # Lists
    lists = []

    for ul in soup.find_all(
        ["ul", "ol"]
    ):

        items = [
            li.get_text(
                " ",
                strip=True
            )
            for li in ul.find_all(
                "li"
            )
        ]

        if items:
            lists.append(items)

    # Full visible text
    body_text = ""

    if soup.body:

        body_text = soup.body.get_text(
            "\n",
            strip=True
        )

    else:

        body_text = soup.get_text(
            "\n",
            strip=True
        )

    # Forms
    forms = []

    for form in soup.find_all("form"):

        form_data = {
            "action": urljoin(
                page_url,
                form.get("action", "")
            ),
            "method": form.get(
                "method",
                "GET"
            ).upper(),
            "inputs": []
        }

        for input_tag in form.find_all(
            ["input", "textarea", "select"]
        ):

            form_data["inputs"].append({
                "name": input_tag.get(
                    "name"
                ),
                "type": input_tag.get(
                    "type",
                    input_tag.name
                ),
                "placeholder": input_tag.get(
                    "placeholder"
                )
            })

        forms.append(form_data)

    return {
        "url": page_url,
        "title": title,
        "description": description,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "tables": tables,
        "lists": lists,
        "forms": forms,
        "text": body_text
    }


# ------------------------------------------------------------
# Main crawler
# ------------------------------------------------------------

print("\nStarting crawler...")
print(f"Target domain : {BASE_DOMAIN}")
print(f"Maximum pages : {MAX_PAGES}")
print("=" * 70)

while queue and len(visited) < MAX_PAGES:

    current_url = queue.popleft()

    if current_url in visited:
        continue

    if not is_internal(current_url):
        continue

    print(
        f"\n[{len(visited) + 1}] "
        f"Scanning: {current_url}"
    )

    try:

        response = session.get(
            current_url,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        final_url = normalize_url(
            response.url
        )

        if not is_internal(final_url):
            print("   Skipped external redirect")
            continue

        if response.status_code != 200:

            print(
                f"   HTTP {response.status_code}"
            )

            visited.add(current_url)

            continue

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        # Only parse HTML pages
        if "text/html" not in content_type:

            print(
                f"   Non-HTML: {content_type}"
            )

            visited.add(current_url)

            continue

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Extract page information
        page_data = extract_page_data(
            soup,
            final_url
        )

        all_pages.append(
            page_data
        )

        visited.add(current_url)
        visited.add(final_url)

        # ----------------------------------------------------
        # Save raw HTML
        # ----------------------------------------------------

        filename = (
            safe_filename(
                urlparse(final_url).path
            )
            + "_"
            + url_hash(final_url)
            + ".html"
        )

        html_path = os.path.join(
            PAGES_DIR,
            filename
        )

        with open(
            html_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(response.text)

        # ----------------------------------------------------
        # Find internal links
        # ----------------------------------------------------

        for link in soup.find_all("a"):

            href = link.get("href")

            if not href:
                continue

            absolute_url = normalize_url(
                urljoin(final_url, href)
            )

            parsed = urlparse(
                absolute_url
            )

            # Ignore non-web links
            if parsed.scheme not in [
                "http",
                "https"
            ]:
                continue

            # Only same domain
            if not is_internal(
                absolute_url
            ):
                continue

            # Ignore common file downloads
            ignored_extensions = (
                ".pdf",
                ".zip",
                ".rar",
                ".exe",
                ".dmg",
                ".iso",
                ".mp4",
                ".mp3",
                ".avi",
                ".mov"
            )

            if parsed.path.lower().endswith(
                ignored_extensions
            ):
                continue

            if (
                absolute_url not in visited
                and absolute_url not in queued
            ):

                queue.append(
                    absolute_url
                )

                queued.add(
                    absolute_url
                )

        # ----------------------------------------------------
        # Find and download images
        # ----------------------------------------------------

        image_urls = extract_image_urls(
            soup,
            final_url
        )

        for image_url in image_urls:

            if image_url in [
                image["image_url"]
                for image in all_images
            ]:
                continue

            print(
                f"   Image: {image_url}"
            )

            image_data = download_image(
                image_url,
                final_url
            )

            if image_data:

                all_images.append(
                    image_data
                )

        print(
            f"   Links queued : {len(queue)}"
        )

        print(
            f"   Images found : {len(image_urls)}"
        )

        time.sleep(
            REQUEST_DELAY
        )

    except requests.exceptions.RequestException as error:

        print(
            f"   Request error: {error}"
        )

    except Exception as error:

        print(
            f"   Error: {error}"
        )


# ============================================================
# SAVE DATA
# ============================================================

print("\n" + "=" * 70)
print("Saving scraped data...")
print("=" * 70)

# ------------------------------------------------------------
# Pages CSV
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "pages.csv"
    ),
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "URL",
        "Title",
        "Description",
        "Text"
    ])

    for page in all_pages:

        writer.writerow([
            page["url"],
            page["title"],
            page["description"],
            page["text"]
        ])


# ------------------------------------------------------------
# Links CSV
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "links.csv"
    ),
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Source Page",
        "Link Text",
        "URL"
    ])

    for page in all_pages:

        for link in page["links"]:

            writer.writerow([
                page["url"],
                link["text"],
                link["url"]
            ])


# ------------------------------------------------------------
# Images CSV
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "images.csv"
    ),
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Image URL",
        "Source Page",
        "Local File"
    ])

    for image in all_images:

        writer.writerow([
            image["image_url"],
            image["source_page"],
            image["local_file"]
        ])


# ------------------------------------------------------------
# Complete text dump
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "complete_text.txt"
    ),
    "w",
    encoding="utf-8"
) as file:

    for page in all_pages:

        file.write("\n")
        file.write("=" * 100)
        file.write("\n")

        file.write(
            f"URL: {page['url']}\n"
        )

        file.write(
            f"TITLE: {page['title']}\n"
        )

        file.write(
            f"DESCRIPTION: "
            f"{page['description']}\n"
        )

        file.write("\n")

        file.write(
            page["text"]
        )

        file.write("\n\n")


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("                 SCRAPING COMPLETE")
print("=" * 70)

print(
    f"Pages scraped  : {len(all_pages)}"
)

print(
    f"Images scraped : {len(all_images)}"
)

print(
    f"URLs visited   : {len(visited)}"
)

print(
    f"\nOutput folder  : {OUTPUT_DIR}/"
)

print("\nFiles created:")

print(
    "  ├── pages.csv"
)

print(
    "  ├── links.csv"
)

print(
    "  ├── images.csv"
)

print(
    "  ├── complete_text.txt" 
)

print(
    "  ├── pages/"
)

print(
    "  └── images/"
)

print("=" * 70)