from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os, json, uuid, asyncio, urllib.parse

from playwright.async_api import async_playwright
from utils.resume_parser import extract_text
from utils.style_injector import inject_logo, inject_styles
from utils.prompt_builder import build_talingual_gpt_messages
from utils.html_parser import extract_filename_from_html
from utils.html_to_docx import convert_html_to_docx
from utils.google_upload import get_user_google_credentials, upload_docx_to_drive
from utils.section_filter import filter_sections_by_config
from utils.filename_utils import build_safe_filename


# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers=["Content-Disposition"])

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    try:
        file = request.files["resume"]
        notes = request.form.get("notes", "")
        config_raw = request.form.get("config", "{}")
        config = json.loads(config_raw)
        resume_text = extract_text(file)
        if not resume_text.strip():
            return jsonify({
                "error": "Could not extract text from the uploaded file. Please upload a typed PDF or DOCX file (not a scanned image)."
            }), 400

        messages = build_talingual_gpt_messages(resume_text, notes)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.4,
            max_tokens=2000
        )
        

        raw_html = response.choices[0].message.content.strip()
        html_with_logo = inject_logo(raw_html, config.get("showLogo", True))
        styled_html = inject_styles(html_with_logo, config)

        filtered_html = filter_sections_by_config(styled_html, config.get("showSections", {}))
        return jsonify({ "formatted_html": filtered_html })


    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({ "error": "Failed to generate resume.", "details": str(e) }), 500



@app.route("/export-pdf", methods=["POST"])
def export_pdf():
    try:
        data = request.get_json()
        raw_html = data.get("html", "")
        config = data.get("config", {})
        name_str = data.get("name", "").strip()
        safe_name = build_safe_filename(name_str, extension="pdf")

        if not raw_html:
            return jsonify({ "error": "No HTML content provided." }), 400

        styled_html = inject_styles(raw_html, config)
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Talingual CV</title></head>
<body>{styled_html}</body>
</html>"""

        file_name = f"temp_{uuid.uuid4().hex}.pdf"


        async def generate_pdf():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.set_content(full_html)
                await page.pdf(path=file_name, format="A4", margin={"top": "40px", "bottom": "40px", "left": "40px", "right": "40px"})
                await browser.close()

        asyncio.run(generate_pdf())

        file_response = send_file(
            file_name,
            download_name=safe_name,
            as_attachment=True,
            mimetype="application/pdf"
        )

        response = make_response(file_response)
        encoded = urllib.parse.quote(safe_name)
        response.headers["Content-Disposition"] = f"attachment; filename={encoded}; filename*=UTF-8''{encoded}"

        return response

    except Exception as e:
        print("[PDF EXPORT ERROR]", str(e))
        return jsonify({ "error": "PDF export failed", "details": str(e) }), 500


@app.route("/export-docx", methods=["POST"])
def export_docx():
    try:
        data = request.get_json()
        html = data.get("html", "")
        config = data.get("config", {})
        name_str = data.get("name", "").strip()
        safe_name = build_safe_filename(name_str, extension="docx")


        if not html:
            return jsonify({ "error": "No HTML provided." }), 400

        docx_path = convert_html_to_docx(html, config)


        file_response = send_file(
            docx_path,
            download_name=safe_name,
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        response = make_response(file_response)
        encoded = urllib.parse.quote(safe_name)
        response.headers["Content-Disposition"] = f"attachment; filename={encoded}; filename*=UTF-8''{encoded}"

        return response

    except Exception as e:
        print("[DOCX EXPORT ERROR]", str(e))
        return jsonify({ "error": "DOCX export failed", "details": str(e) }), 500


@app.route('/api/open-in-google-docs', methods=['POST'])
def open_in_google_docs():
    try:
        # Check if user is authenticated
        token = request.cookies.get("google_token")
        if not token:
            return jsonify({ "error": "Not authenticated" }), 401

        data = request.get_json()
        html = data.get("html", "")
        config = data.get("config", {})
        name_str = data.get("name", "").strip()

        if not html:
            return jsonify({ "error": "No HTML provided." }), 400

        # ✅ Format and convert DOCX
        styled_html = inject_styles(html, config)
        docx_path = convert_html_to_docx(styled_html, config)
        safe_name = build_safe_filename(name_str, extension="docx")

        # ✅ Get user's credentials (silently refresh if needed)
        creds = get_user_google_credentials()

        # ✅ Upload to user's Google Drive
        url = upload_docx_to_drive(creds, docx_path, safe_name)

        return jsonify({ "url": url })

    except Exception as e:
        print("[GOOGLE DOCS ERROR]", str(e))

        # Optional: detect unauth error and return 401
        if "User is not authenticated" in str(e):
            return jsonify({ "error": "Not authenticated" }), 401

        return jsonify({ 
            "error": "Failed to open in Google Docs", 
            "details": str(e) 
        }), 500




from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from config import BACKEND_URL, FRONTEND_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

from google_auth_oauthlib.flow import Flow
from flask import jsonify, request
from config import BACKEND_URL, FRONTEND_URL
import urllib.parse

@app.route('/auth-url')
def get_auth_url():
    redirect_to = f"{FRONTEND_URL}/google-auth-success"
    oauth_redirect_uri = f"{BACKEND_URL}/oauth-callback"

    flow = Flow.from_client_secrets_file(
        "client_id.json",
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/userinfo.email"
        ],
        redirect_uri=oauth_redirect_uri
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes=False,
        state=urllib.parse.quote(redirect_to)
    )

    return jsonify({ "auth_url": auth_url })




from flask import request, redirect, make_response
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import urllib.parse, json, requests
from config import FRONTEND_URL, BACKEND_URL

@app.route('/oauth-callback')
def oauth_callback():
    try:
        # Step 1: Read code and state from URL
        code = request.args.get("code")
        redirect_frontend = urllib.parse.unquote(request.args.get("state", ""))
        oauth_redirect_uri = f"{BACKEND_URL}/oauth-callback"

        # Step 2: Start the OAuth flow
        flow = Flow.from_client_secrets_file(
            "client_id.json",
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/userinfo.email"
            ],
            redirect_uri=oauth_redirect_uri
        )

        flow.fetch_token(code=code)
        creds = flow.credentials

        if not creds or not creds.token:
            return "Missing access token", 401

        # Step 3: Fetch user info using the access token
        userinfo_res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={ "Authorization": f"Bearer {creds.token}" }
        )

        if userinfo_res.status_code != 200:
            return f"Userinfo failed: {userinfo_res.text}", 401

        userinfo = userinfo_res.json()

        email = userinfo.get("email", "").strip().lower()
        if not email.endswith("@talingual.com"):
            return f"Access denied: {email}", 403

        # Step 4: Merge existing refresh_token if this one is missing
        new_data = json.loads(creds.to_json())
        existing_token = request.cookies.get("google_token")

        if not new_data.get("refresh_token") and existing_token:
            try:
                existing_data = json.loads(existing_token)
                if existing_data.get("refresh_token"):
                    new_data["refresh_token"] = existing_data["refresh_token"]
            except Exception as e:
                print("⚠️ Could not parse existing token:", e)

        token_to_store = json.dumps(new_data)

        # Step 5: Set the cookie for 30 days
        IS_LOCAL = "localhost" in BACKEND_URL
        response = make_response(redirect(redirect_frontend))
        response.set_cookie(
            "google_token",
            token_to_store,
            max_age=30 * 24 * 60 * 60,
            httponly=True,
            secure=not IS_LOCAL,            # ✅ False on localhost
            samesite="None" if not IS_LOCAL else "Lax"  # ✅ Fix SameSite for dev
        )

        return response

    except Exception as e:
        print("[OAUTH CALLBACK ERROR]", str(e))
        return f"OAuth callback failed: {str(e)}", 500

@app.route("/is-authenticated")
def is_authenticated():
    token = request.cookies.get("google_token")
    if not token:
        return jsonify({ "authenticated": False }), 200
    try:
        creds = Credentials.from_authorized_user_info(json.loads(token))
        return jsonify({ "authenticated": not creds.expired }), 200
    except:
        return jsonify({ "authenticated": False }), 200


if __name__ == "__main__":
    app.run(debug=True)
