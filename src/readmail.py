from googleapiclient.discovery import build
from datetime import datetime

#  SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def read(creds, amount, label='INBOX', date=None):
    service = build('gmail', 'v1', credentials=creds)
    if not date:
        date = datetime.now().date()
    date = datetime.strptime(str(date), '%Y-%m-%d').date()
    date = date.strftime('%y-%m-%dT00:00:00Z')
    query = f'before:{date}'
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    return [ service.users().messages().get(userId='me', id=message['id']).execute() for message in messages]


def search(creds, string, amount=10):
    service = build('gmail', 'v1', credentials=creds)
    string = f'"{string}"'
    results = service.users().messages.list(userId='me', q=string, maxResults = amount).execute()
    messages = results.get('messages', [])
    return [service.users().messages().get(userId='me', id=message['id']).execute() for message in messages]
