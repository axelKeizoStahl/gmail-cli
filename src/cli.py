from sys import argv
from credentials import getcreds
from gmail import Gmail

gmail_class = Gmail(argv[1], getcreds)
inbox = gmail_class.read(1)
