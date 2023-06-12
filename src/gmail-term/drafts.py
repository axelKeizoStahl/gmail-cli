from __future__ import print_function

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_draft(senderemail, receiveremail, subject,  content):
    creds, _ = google.auth.default()

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message.set_content(content)
        message['To'] = receiveremail
        message['From'] = senderemail
        message['Subject'] = subject

        encoded_meessage = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        draft = service.users().drafts().create(userId="me", body = create_message).execute()

        print(f'Draft id: {draft["id"]}\n Draft message: {draft["message"]}')
    except HttpError as error:
        print(f'An error has occurred: {error}')
        draft = None

    return draft


