from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from bs4 import BeautifulSoup, NavigableString, Tag
from io import BytesIO
import base64
import tempfile

def convert_html_to_docx(html: str, config: dict) -> str:
    doc = Document()
    print(config)
    # Style setup
    font = config.get("fontFamily", "Arial")
    size = int(config.get("fontSize", "11px").replace("px", ""))
    spacing = float(config.get("lineSpacing", 1.15))
    logo_width = int(config.get("logoSize", "250px").replace("px", ""))

    style = doc.styles['Normal']
    style.font.name = font
    style.font.size = Pt(size)

    section = doc.sections[0]
    # section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    soup = BeautifulSoup(html, 'html.parser')

    # Insert logo if present
    logo_tag = soup.find("img", class_="resume-logo")
    if logo_tag and "base64" in logo_tag.get("src", ""):
        base64_data = logo_tag["src"].split("base64,")[1]
        logo_bytes = BytesIO(base64.b64decode(base64_data))
        doc.add_picture(logo_bytes, width=Inches(logo_width / 96))  # Convert px to inch
        doc.add_paragraph()

    for elem in soup.find_all(["h2", "p", "ul", "li"], recursive=True):
        if isinstance(elem, NavigableString):
            continue

        text = elem.get_text(strip=True)
        if not text:
            continue

        tag = elem.name

        if tag == "h2":
            para = doc.add_paragraph()
            run = para.add_run(text.upper())
            run.bold = True
            run.font.size = Pt(size + 1)
            para.paragraph_format.space_after = Pt(12)

        elif tag == "p":
            para = doc.add_paragraph()
            run = para.add_run(text)
            run.font.size = Pt(size)
            para.paragraph_format.line_spacing = spacing
            para.paragraph_format.space_after = Pt(4)

        elif tag == "li":
            para = doc.add_paragraph(text, style="List Bullet")
            for run in para.runs:
                run.font.size = Pt(size)
            para.paragraph_format.space_after = Pt(6)
            para.paragraph_format.line_spacing = spacing

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name
