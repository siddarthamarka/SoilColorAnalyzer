from google.oauth2 import service_account
from googleapiclient.discovery import build
import io, os
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials/service_account.json'

def download_images_from_drive(folder_id, download_path):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    query = f"'{folder_id}' in parents and mimeType contains 'image/'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    downloaded_files = []
    for file in files:
        file_id = file['id']
        file_name = file['name']
        file_path = os.path.join(download_path, file_name)

        request = service.files().get_media(fileId=file_id)
        with open(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        downloaded_files.append(file_path)
    return downloaded_files
