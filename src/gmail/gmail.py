import readmail
import mailingactions

class Gmail:
    def __init__(self, creds):
        self.creds = creds
    def read(self, amount):
        readmail.read(self.creds, amount)
    def search(self, query):
        readmail.search(creds, query)
    def create_draft(self, text):
        mailingactions.create_draft(self, )
