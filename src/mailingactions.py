from __future__ import print_function
import base64
import os
import mimetypes
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


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
        
        return (f"draft_id: {draft['id']}\ndraft_message: {draft['message']}")
    
    except HttpError as error:
        return str(error)
        draft=None


def create_multimediaMIME(creds, filename, sender, reciever, subject, content):
    try:
        service = build('gmail', 'v1', credentials=creds)
        mime_message = EmailMessage()

        mime_message['To'] = reciever
        mime_message['Form'] = sender
        mime_message['Subject'] = subject

        mime_message.setcontent(content)
        
        type_subtype, _ = mimetypes.guess_type(filename)
        maintype, subtype = type_subtype.split('/')
        
        with open(filename, 'rb') as fp:
            data = fp.read
        mime_message.add_attachment(data, maintype, subtype)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_draft_request_body = {
            'message': {
                'raw': encoded_message
            }
        }

        draft = service.users().drafts().create(userId="me", body=create_draft_request_body).execute()
        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
    return draft

def build_file_part(file):
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        with open(file, 'rb'):
            msg = MIMEText('r', _subtype=sub_type)
    elif main_type == 'image':
        with open(file, 'rb'):
            msg = MIMEImage('r', _subtype=sub_type)
    elif main_type == 'audio':
        with open(file, 'rb'):
            msg = MIMEAudio('r', _subtype=sub_type)
    else:
        with open(file, 'rb'):
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    return msg


def send_message(creds, sender, reciever, subject, content):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(content)
        message['To'] = reciever
        message['From'] = sender
        message['Subject'] = subject # subject header matches if replying

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encoded_message}

        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message
