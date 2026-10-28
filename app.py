from pathlib import Path

import streamlit as st
from bs4 import BeautifulSoup

from checks import check_title, check_lang, check_images, check_form_labels
from fetch import fetch_page, FetchError

CHECKS = [
    ("Page title", check_title),
    ("Page language", check_lang),
    ("Image descriptions", check_images),
    ("Form labels", check_form_labels),
]

st.set_page_config(page_title="Accessibility Scanner", layout="centered")

# Load the custom styles from style.css
css = (Path(__file__).parent / "style.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("Accessibility Scanner")
st.markdown(
    "**How to use it**\n"
    "1. Paste a link to a page. You can leave off the `https://`.\n"
    "2. Press **Scan**.\n"
    "3. Anything marked red needs fixing. Anything under \"to check yourself\" needs a person to look at it."
)

with st.form("scan"):
    col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
    url = col1.text_input("Page URL", placeholder="durhamnc.gov")
    submitted = col2.form_submit_button("Scan")

st.info("A clean result does not mean a page is accessible. This tool checks four things out of many.")
with st.expander("What this tool can't check"):
    st.markdown(
        "- Anything beyond the single page you enter\n"
        "- Content added by JavaScript\n"
        "- Whether descriptions and labels are accurate or helpful\n"
        "- Color contrast, keyboard navigation, video captions, PDFs, and most of WCAG\n\n"
        "Real people, including people who use screen readers, still need to test the site."
    )

if submitted:
    target = url.strip()
    if target and not target.startswith(("http://", "https://")):
        target = "https://" + target

    try:
        with st.spinner("Checking permission and fetching the page..."):
            html = fetch_page(target)
    except FetchError as e:
        st.error(f"Could not scan: {e}")
    else:
        soup = BeautifulSoup(html, "html.parser")

        results = []
        for name, check in CHECKS:
            findings = check(soup)
            fails = [f for f in findings if f["level"] == "fail"]
            reviews = [f for f in findings if f["level"] == "review"]
            results.append((name, fails, reviews))

        total_fails = sum(len(fails) for _, fails, _ in results)
        total_reviews = sum(len(reviews) for _, _, reviews in results)

        st.subheader(f"Results for {target}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Checks run", len(CHECKS))
        m2.metric("Failures", total_fails)
        m3.metric("To check yourself", total_reviews)

        for i, (name, fails, reviews) in enumerate(results):
            with st.container(border=True, key=f"card_{i}"):
                if fails:
                    st.markdown(f"**{name}** · :red[{len(fails)} failed]")
                    for f in fails:
                        st.markdown(f"- `{f['element']}` {f['message']}")
                else:
                    st.markdown(f"**{name}** · :green[passed]")

                if reviews:
                    with st.expander(f"{len(reviews)} to check yourself"):
                        for r in reviews:
                            st.markdown(f"- `{r['element']}` {r['message']}")

        st.caption("Only the checks above were run. Passing them does not mean this page is accessible.")

st.divider()
st.caption(
    "Respects each site's robots.txt and fetches one page per scan. "
    "Source: github.com/pranav-ysv/accessibility-scanner"
)