import re

def extract_filename_from_html(html: str) -> str:
    """
    Extracts the first <p>Name: ...</p> and returns a safe filename like john_doe_resume.pdf
    """
    match = re.search(r"<p>\s*Name:\s*(.+?)\s*</p>", html, re.IGNORECASE)
    if match:
        full_name = match.group(1).strip()
        # safe_name = "_".join(full_name.lower().split())
        print(full_name)
        return f"{full_name}.pdf"
    return "talingual_resume.pdf"
