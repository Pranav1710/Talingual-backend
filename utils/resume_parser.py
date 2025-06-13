# utils/resume_parser.py

import os
from docx import Document
import pdfplumber

def extract_text(file):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])

    elif ext == ".docx":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    return ""
