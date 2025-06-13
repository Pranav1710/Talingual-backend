from google_auth_oauthlib.flow import InstalledAppFlow

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_id.json',  # Make sure this file exists in the same folder
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    creds = flow.run_local_server(port=0)
    
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())

if __name__ == "__main__":
    generate_token()
