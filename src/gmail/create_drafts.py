from __future__ import print_function
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_draft(creds, sender, reciever, subject, content):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(content)
        message['To'] = reciever
        message['From'] = sender
        message['Subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {
                'message': {
                    'raw': encoded_message
                }
            }
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        
        print(f"draft_id: {draft['id']}\ndraft_message: {draft['message']}")
    
    except HttpError as error:
        print(f'ERROR: {error}')
        draft=None

    return draft
