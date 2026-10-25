import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

USER_AGENT = "AccessibilityScanner/0.1 (+https://github.com/pranav-ysv/accessibility-scanner)"
TIMEOUT = 10  # seconds to wait before giving up
PAUSE = 1     # seconds to wait between requests


class FetchError(Exception):
    """Raised when a page can't or shouldn't be scanned. The message says why."""


def allowed_by_robots(url):
    """Read the site's robots.txt and return True if our tool may fetch this URL."""
    parts = urlparse(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"

    try:
        response = requests.get(robots_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    except requests.RequestException:
        raise FetchError("Couldn't reach the site to read its robots.txt rules, so it wasn't scanned.")

    if response.status_code >= 500:
        raise FetchError("The site's server had an error reading its robots.txt rules, so it wasn't scanned.")
    if response.status_code >= 400:
        # No robots.txt (usually a 404): the site has set no rules for tools.
        return True

    parser = RobotFileParser()
    parser.parse(response.text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def fetch_page(url):
    """Politely download one page and return its HTML. Raises FetchError if it can't."""
    if not url.startswith(("http://", "https://")):
        raise FetchError("The URL must start with http:// or https://")

    if not allowed_by_robots(url):
        raise FetchError("This site's robots.txt doesn't allow automated tools on this page, so it wasn't scanned.")

    time.sleep(PAUSE)

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    except requests.Timeout:
        raise FetchError(f"The page didn't respond within {TIMEOUT} seconds.")
    except requests.RequestException:
        raise FetchError("Couldn't connect to the page.")

    if response.status_code != 200:
        raise FetchError(f"The page returned an error (status code {response.status_code}).")

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise FetchError(f"This isn't a web page ({content_type or 'unknown type'}), so it can't be scanned.")

    return response.text