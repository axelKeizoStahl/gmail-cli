import os
from mailingactions import *
from readmail import *

class Gmail:
    def __init__(self, email, getcreds):
        self.creds = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.send"]
        self.email = email
        self.getcreds = getcreds

    def read(self, amount):
        credentials = self.getcreds('.', [self.creds[0]])
        mail = read(self.creds, amount)
        return mail

    def search(self, query):
        credentials = self.getcreds(f'{os.path.expanduser("~")}/.googleterm/gmail.readonly', [self.creds[0]])
        search_results = search(credentials, query)
        return search_results

    def create_draft(self, text):
        credentials = self.getcreds(f'{os.path.expanduser("~")}/.googleterm/gmail.compose', [self.creds[1]])
        draft = create_draft(text)
        return draft

    def create_MIME_draft(self, filepath):
        credentials = self.getcreds(f'{os.path.expanduser("~")}/.googleterm/gmail.compose', [self.creds[1]])
        MIME_draft = create_multimediaMIME(filepath)
        return MIME_draft

    def send_message(self, text, receiver, subject):
        credentials = self.getcreds(f'{os.path.expanduser("~")}/.googleterm/gmail.send', [self.creds[2]])
        sent_message = send_message(credentials, self.email, receiver, subject, text)
        return sent_message
