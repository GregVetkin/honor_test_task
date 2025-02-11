from abc import ABC, abstractmethod


class MailServerInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def fetch_unread_email_ids(self):
        pass

    @abstractmethod
    def get_email_content(self, email_id):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
