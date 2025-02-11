import email
from collections    import namedtuple
from typing         import List


attachment = namedtuple("Attachment", ["filename", "payload"])


class EmailAttachmentHandler:
    @staticmethod
    def extract_attachments(email_content, allowed_extensions) -> List[attachment]:
        attachments = []

        for response_part in email_content:
            if not isinstance(response_part, tuple):
                continue

            message = email.message_from_bytes(response_part[1])

            for message_part in message.walk():
                if message_part.get_content_maintype() == 'multipart':
                    continue
                if message_part.get('Content-Disposition') is None:
                    continue

                filename = message_part.get_filename()

                if filename and any(filename.endswith(ext) for ext in allowed_extensions):
                    attachments.append(
                        attachment(
                            filename=filename,
                            payload=message_part.get_payload(decode=True)
                        )
                    )

        return attachments
    
