import os


class MailData:
    EMAIL       = '*********@gmail.com'
    PASSWORD    = '**** **** **** ****'
    SERVER      = 'imap.gmail.com'


class DatabaseConfig:
    SERVER      = '127.0.0.1'
    DATABASE    = 'postgres'
    USERNAME    = 'postgres'
    PASSWORD    = 'postgres'
    PROTOCOL    = 'postgresql'
    URL         = f"{PROTOCOL}://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"




DOWNLOAD_FOLDER     = os.path.join(os.getcwd(), 'downloads')
ALLOWED_EXTENSIONS  = {'.xlsx'}


