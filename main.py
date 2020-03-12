from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
DRIVE = build('drive', 'v3', credentials=creds)

def uploadFile(FILES, Folder):
    for filename in FILES:
        folderId = getFolderId(Folder)
        file_metadata = {
            'name': filename,
            'parents': folderId
        }
        res = DRIVE.files().create(body=file_metadata, media_body=filename, fields='id').execute()
        if res:
            print('Uploaded "{}" to "{}"'.format(filename, Folder))

def getFolderId(Folder):
    # Searches only for folders based on the passed name
    res = DRIVE.files().list(q='name="{}" and mimeType="{}" and trashed=false'.format(Folder, 'application/vnd.google-apps.folder'), spaces='drive').execute()
    for file in res.get('files', []):
        return file.get('id') # Finds Folder, returns id
    return createFolder(Folder) # Doesnt find the folder, creates it, returns id

def createFolder(Folder):
    file_metadata = {
        'name': Folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE.files().create(body=file_metadata, fields='id').execute()
    print('Created Folder "{}"'.format(Folder))
    return file.get('id')

def main():
    FILES = (
        'credentials.json',
        'test.txt'
    )
    Folder = 'CloudSaves'
    uploadFile(FILES, Folder)

if __name__ == '__main__':
    main()
