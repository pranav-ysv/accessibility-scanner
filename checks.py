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