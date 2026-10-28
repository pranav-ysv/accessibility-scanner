# Accessibility Scanner

Try it: https://accessibility-scanner.streamlit.app

Paste in a link to a web page and it tells you what basic accessility problems are and shows you the exact spot on the page and the WCAG rule that it breaks. I built this with small government sites in mind that disabled users might have to access. 

## What it checks

- whether a page has a title
- whether it says what language it is in
- whether the images have text descriptions
- whether form fields have lables
- anything that it cannot label gets flagged as "check this yourself"

## Limitations

- one page at a time
- can't see content added by javascript (only HTML)
- whether a description is helpful
