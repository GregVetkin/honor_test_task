import os
import pandas
import sqlalchemy
from mail.imap              import IMAPMailServer
from config                 import MailData, ALLOWED_EXTENSIONS, DOWNLOAD_FOLDER, DatabaseConfig
from handlers.attachment    import EmailAttachmentHandler
from handlers.file_saver    import FileSaver



def preparations(db_engine):
    with db_engine.begin() as conn:
        conn.execute(sqlalchemy.text(f"""
            CREATE TABLE IF NOT EXISTS created_tables_by_file (
                id          SERIAL PRIMARY KEY,
                file_path   TEXT NOT NULL UNIQUE,
                table_name  TEXT NOT NULL
            );
        """))


def table_exists(table_name, db_engine) -> bool:
    with db_engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(f"""
            SELECT COUNT(*) FROM created_tables_by_file 
            WHERE table_name = :table_name
        """), {"table_name": table_name})
    return result.scalar() > 0



def add_link_table_to_file(table_name, file_path, db_engine):
    with db_engine.begin() as conn:
        conn.execute(sqlalchemy.text(f"""
            INSERT INTO created_tables_by_file (file_path, table_name)
            VALUES (:file_path, :table_name)
        """), {"file_path": file_path, "table_name": table_name})


def excel_file_to_database(excel_file_path, db_engine):
    with pandas.ExcelFile(excel_file_path) as excel:
        for sheet_name in excel.sheet_names:
            its_new_table = not table_exists(sheet_name, db_engine)
            dataframe = pandas.read_excel(excel, sheet_name=sheet_name)
            dataframe.to_sql(sheet_name, con=db_engine, if_exists='append', index=False)
            if its_new_table:
                add_link_table_to_file(sheet_name, excel_file_path, db_engine)





if __name__ == "__main__":
    file_saver  = FileSaver(DOWNLOAD_FOLDER)
    mail_server = IMAPMailServer(MailData.SERVER, MailData.EMAIL, MailData.PASSWORD)
    db_engine   = sqlalchemy.create_engine(DatabaseConfig.URL)
    preparations(db_engine)

    with mail_server as mailbox:
        for email_id in mailbox.fetch_unread_email_ids():
            email_content = mailbox.get_email_content(email_id)
            attachments   = EmailAttachmentHandler.extract_attachments(email_content, ALLOWED_EXTENSIONS)
            for attachment in attachments:
                filepath = file_saver.save_file(attachment.filename, attachment.payload)
                excel_file_to_database(filepath, db_engine)
