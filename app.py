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

st.title("Accessibility Scanner")

st.warning(
    "This tool checks one page of a website for four things: whether the page has a title, "
    "whether it says what language it's written in, whether images have text descriptions, "
    "and whether form fields have labels. "
    "Passing these checks does not mean the site is accessible. A page can fail in many ways this tool never looks at. "
    "It can't tell whether a description or label is accurate, can't see content added by JavaScript, "
    "and doesn't check videos, colors, keyboard navigation, or any other page on the site, "
    "so real people, including people who use screen readers, still need to test it."
)

url = st.text_input("Page URL", placeholder="https://www.example.gov")

if st.button("Scan"):
    try:
        with st.spinner("Checking permission and fetching the page..."):
            html = fetch_page(url.strip())
    except FetchError as e:
        st.error(f"Could not scan: {e}")
    else:
        soup = BeautifulSoup(html, "html.parser")
        st.subheader("Results")

        for name, check in CHECKS:
            findings = check(soup)
            fails = [f for f in findings if f["level"] == "fail"]
            reviews = [f for f in findings if f["level"] == "review"]

            if fails:
                st.error(f"**{name}: {len(fails)} failed**")
                for f in fails:
                    st.markdown(f"- `{f['element']}` {f['message']}")
            else:
                st.success(f"**{name}: passed**")

            if reviews:
                with st.expander(f"{name}: {len(reviews)} to check yourself"):
                    for r in reviews:
                        st.markdown(f"- `{r['element']}` {r['message']}")

        st.caption("Only the checks above were run. Passing them does not mean this page is accessible.")