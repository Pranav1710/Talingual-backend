from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def get_user_google_credentials():
    token_path = 'token.json'
    if not os.path.exists(token_path):
        raise Exception("Google token.json not found. Please run generate_token.py")
    return Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/drive.file'])

def upload_docx_to_drive(creds, docx_path):
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'Talingual Resume',
        'mimeType': 'application/vnd.google-apps.document'
    }
    media = MediaFileUpload(docx_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return f"https://docs.google.com/document/d/{uploaded['id']}/edit"
