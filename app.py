# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from utils.resume_parser import extract_text
from utils.style_injector import inject_logo, inject_styles
from utils.prompt_builder import build_talingual_gpt_messages

# Load API keys and environment
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    try:
        file = request.files["resume"]
        notes = request.form.get("notes", "")
        config_raw = request.form.get("config", "{}")

        import json
        config = json.loads(config_raw)

        resume_text = extract_text(file)
        messages = build_talingual_gpt_messages(resume_text, notes)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.4,
            max_tokens=2000
        )

        raw_html = response.choices[0].message.content.strip()
        html_with_logo = inject_logo(raw_html)
        styled_html = inject_styles(html_with_logo, config)
        return jsonify({ "formatted_html": styled_html })

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({ "error": "Failed to generate resume.", "details": str(e) }), 500

from flask import request, send_file, jsonify
from playwright.async_api import async_playwright
import asyncio
import uuid
import os
import json
from utils.style_injector import inject_styles, inject_logo
from utils.html_parser import extract_filename_from_html


@app.route("/export-pdf", methods=["POST"])
def export_pdf():
    try:
        data = request.get_json()
        raw_html = data.get("html", "")
        config = data.get("config", {})

        if not raw_html:
            return jsonify({"error": "No HTML content provided."}), 400

        # Inject logo and CSS styles
        # html_with_logo = inject_logo(raw_html)
        styled_html = inject_styles(raw_html, config)

        # Wrap in full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Talingual CV</title>
</head>
<body>
  {styled_html}
</body>
</html>
"""

        # Unique PDF file name
        download_name = extract_filename_from_html(styled_html)
        file_name = f"temp_{uuid.uuid4().hex}.pdf"  # actual file saved locally


        # Inner async function
        async def generate_pdf():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.set_content(full_html)
                await page.pdf(path=file_name, format="A4", margin={"top": "40px", "bottom": "40px", "left": "40px", "right": "40px"})
                await browser.close()

        asyncio.run(generate_pdf())

        return send_file(
            file_name,
            as_attachment=True,
            download_name = download_name,
            mimetype="application/pdf"
        )

    except Exception as e:
        print("[PDF EXPORT ERROR]", str(e))
        return jsonify({"error": "PDF export failed", "details": str(e)}), 500

from flask import request, send_file, jsonify
from utils.html_to_docx import convert_html_to_docx

@app.route("/export-docx", methods=["POST"])
def export_docx():
    try:
        data = request.get_json()
        html = data.get("html", "")
        config = data.get("config", {})

        if not html:
            return jsonify({ "error": "No HTML provided." }), 400

        # Convert HTML to DOCX
        docx_path = convert_html_to_docx(html, config)

        # Generate filename
        from utils.html_parser import extract_filename_from_html
        filename = extract_filename_from_html(html).replace(".pdf", ".docx")

        return send_file(
            docx_path,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


    except Exception as e:
        print("[DOCX EXPORT ERROR]", e)
        return jsonify({ "error": "DOCX export failed", "details": str(e) }), 500

from flask import request, jsonify
from utils.style_injector import inject_styles
from utils.html_to_docx import convert_html_to_docx
from utils.google_upload import get_user_google_credentials, upload_docx_to_drive
from utils.html_parser import extract_filename_from_html

@app.route('/api/open-in-google-docs', methods=['POST'])
def open_in_google_docs():
    try:
        data = request.get_json()
        html = data.get("html", "")
        config = data.get("config", {})

        if not html:
            return jsonify({ "error": "No HTML provided." }), 400

        # Inject styles, skip logo injection (logo already included)
        styled_html = inject_styles(html, config)

        # Convert to DOCX
        docx_path = convert_html_to_docx(styled_html, config)

        # Upload to Google Docs
        creds = get_user_google_credentials()
        url = upload_docx_to_drive(creds, docx_path)

        return jsonify({ "url": url })

    except Exception as e:
        print("[GOOGLE DOCS ERROR]", e)
        return jsonify({ "error": "Failed to open in Google Docs", "details": str(e) }), 500


if __name__ == "__main__":
    app.run(debug=True)
