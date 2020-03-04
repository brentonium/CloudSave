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

def main():
    print('Hello')
    FILES = (
        'credentials.json',
        'test.txt'
    )
    Folder = 'CloudSaves'
    searchFolder(Folder)

def uploadFile(FILES):
    for filename in FILES:
        metadata = {'name': filename}
        res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Uploaded "%s"' % (filename))

def searchFolder(Folder):
    res = DRIVE.files().list(q="name='CloudSaves'", spaces='drive').execute()
    for file in res.get('files', []):
        # Process change
        print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

    # if len(res) >= 1:
    #     print('Ordner {} gefunden'.format(Folder))
    # else:
    #     createFolder(Folder)


if __name__ == '__main__':
    main()
