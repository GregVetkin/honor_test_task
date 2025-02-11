import imaplib
from mail.base  import MailServerInterface


class IMAPMailServer(MailServerInterface):
    def __init__(self, server, email, password):
        self.server     = server
        self.email      = email
        self.password   = password
        self.mailbox    = None

    def connect(self):
        self.mailbox = imaplib.IMAP4_SSL(self.server)
        self.mailbox.login(self.email, self.password)
        self.mailbox.select('inbox')

    def close(self):
        if self.mailbox:
            self.mailbox.close()
            self.mailbox.logout()

    def fetch_unread_email_ids(self):
        status, messages = self.mailbox.search(None, 'UNSEEN')
        if status == 'OK':
            return messages[0].split()
        return []

    def get_email_content(self, email_id):
        status, msg_data = self.mailbox.fetch(email_id, '(RFC822)')
        if status == 'OK': 
            return msg_data
        return None



