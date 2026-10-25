PLACEHOLDER_ALTS = {
    "image", "img", "photo", "photograph", "picture", "pic",
    "graphic", "icon", "placeholder", "spacer", "untitled", "blank",
}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp")


def fail(element, message):
    return {"level": "fail", "element": element, "message": message}


def review(element, message):
    return {"level": "review", "element": element, "message": message}


def check_title(soup):
    """Check that the page has a <title> with real text in it. WCAG 2.4.2 (Page Titled)."""
    title = soup.title
    if title is None:
        return [fail("<title>", "Page has no <title>. A screen reader has no page name to announce. (WCAG 2.4.2)")]
    if title.get_text().strip() == "":
        return [fail("<title>", "Page <title> is empty. A screen reader has no page name to announce. (WCAG 2.4.2)")]
    return []


def check_lang(soup):
    """Check that the <html> tag declares the page's language. WCAG 3.1.1 (Language of Page)."""
    html_tag = soup.html
    if html_tag is None:
        return [fail("<html>", "Page has no <html> element, so no language is declared. (WCAG 3.1.1)")]
    lang = html_tag.get("lang")
    if lang is None or lang.strip() == "":
        return [fail("<html>", "Page has no language set on <html>. A screen reader may pronounce everything wrong. (WCAG 3.1.1)")]
    return []


def describe_img(img):
    """Short label for an image so a site owner can find it."""
    src = img.get("src", "(no src)")
    if len(src) > 80:
        src = src[:77] + "..."
    return f'<img src="{src}">'


def check_images(soup):
    """Check that images have useful text descriptions. WCAG 1.1.1 (Non-text Content)."""
    findings = []

    for img in soup.find_all("img"):
        element = describe_img(img)

        # Marked as decorative or hidden from screen readers: no description needed
        if img.get("aria-hidden") == "true" or img.get("role") in ("presentation", "none"):
            continue

        # Described another way than alt
        if (img.get("aria-label") or "").strip() or img.get("aria-labelledby"):
            continue

        alt = img.get("alt")

        if alt is None:
            findings.append(fail(element,
                "Image has no text description. A screen reader user won't know what it shows. (WCAG 1.1.1)"))
        elif alt.strip() == "":
            findings.append(review(element,
                'Image is marked decorative (alt=""), so screen readers skip it. Check that it really shows nothing important.'))
        elif alt.strip().lower() in PLACEHOLDER_ALTS or alt.strip().lower().endswith(IMAGE_EXTENSIONS):
            findings.append(fail(element,
                f'Image description "{alt.strip()}" is a placeholder and tells the user nothing. (WCAG 1.1.1)'))

    return findings