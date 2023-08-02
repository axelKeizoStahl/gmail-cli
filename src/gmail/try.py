from credentials import getcreds
from gmail import Gmail
import readmail

creds = getcreds('./', ['https://www.googleapis.com/auth/gmail.readonly'])
print(readmail.read(creds, 1))
gmail_class = Gmail("axelkeizo@gmail.com", getcreds)
inbox = gmail_class.read(40)
