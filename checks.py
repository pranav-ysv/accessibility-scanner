def check_title(soup):
    """Check that the page has a <title> with real text in it. WCAG 2.4.2 (Page Titled)."""
    title = soup.title

    # Case A: no <title> tag at all
    if title is None:
        return ["Page has no <title>. A screen reader has no page name to announce. (WCAG 2.4.2)"]

    # Cases B and C: the tag exists, but is empty or only spaces
    if title.get_text().strip() == "":
        return ["Page <title> is empty. A screen reader has no page name to announce. (WCAG 2.4.2)"]

    # Passed
    return []


def check_lang(soup):
    """Check that the <html> tag declares the page's language. WCAG 3.1.1 (Language of Page)."""
    html_tag = soup.html

    # No <html> tag at all (rare, but broken pages exist)
    if html_tag is None:
        return ["Page has no <html> element, so no language is declared. (WCAG 3.1.1)"]

    lang = html_tag.get("lang")

    # Missing, empty, or only spaces
    if lang is None or lang.strip() == "":
        return ["Page has no language set on <html>. A screen reader may pronounce everything wrong. (WCAG 3.1.1)"]

    return []