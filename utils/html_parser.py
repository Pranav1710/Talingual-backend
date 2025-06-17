import re

def extract_filename_from_html(html: str) -> str:
    match = re.search(r"<p>\s*Name:\s*(.+?)\s*</p>", html, re.IGNORECASE)
    if match:
        full_name = match.group(1).strip()
        # Replace whitespace with underscore
        safe_name = re.sub(r"\s+", "_", full_name)

        # Remove characters that are unsafe in filenames (except Unicode letters and digits)
        # Allow: letters, digits, underscores
        safe_name = re.sub(r"[^\w\d_]", "", safe_name, flags=re.UNICODE)
        return f"{safe_name}.pdf"

    return "talingual_resume.pdf"
