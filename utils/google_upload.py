from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import os
from flask import request
import json

def get_user_google_credentials():
    token_json = request.cookies.get("google_token")
    if not token_json:
        raise Exception("Not authenticated")

    creds = Credentials.from_authorized_user_info(json.loads(token_json))

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    return creds


def upload_docx_to_drive(creds, docx_path, filename="Talingual Resume.docx"):
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': filename,
        'mimeType': 'application/vnd.google-apps.document'
    }

    media = MediaFileUpload(
        docx_path,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return f"https://docs.google.com/document/d/{uploaded['id']}/edit"

