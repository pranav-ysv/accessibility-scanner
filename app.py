import streamlit as st
from bs4 import BeautifulSoup

from checks import check_title, check_lang
from fetch import fetch_page, FetchError

# Every check the tool runs. Adding a new check = adding one line here.
CHECKS = [
    ("Page title", check_title),
    ("Page language", check_lang),
]

st.title("Accessibility Scanner")

st.warning(
    "This tool checks one page of a website for two things: whether the page has a title, "
    "and whether it says what language it's written in. "
    "Passing these checks does not mean the site is accessible. A page can fail in many ways this tool never looks at. "
    "It can't see images, forms, videos, colors, keyboard navigation, or any other page on the site, "
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
            failures = check(soup)
            if failures:
                for message in failures:
                    st.error(f"**{name}: failed.** {message}")
            else:
                st.success(f"**{name}: passed.**")
        st.caption("Only the checks above were run. Passing them does not mean this page is accessible.")