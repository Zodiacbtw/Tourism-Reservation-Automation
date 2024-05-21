import pypyodbc
from pathlib import Path
import win32com.client
from datetime import (datetime)

SERVER_ADI = r"DESKTOP-5HV3O9R\SQLEXPRESS"


def connect_db(server_adi):
    db = pypyodbc.connect(
        'Driver={SQL Server};'
        f'Server={server_adi};'
        'Database=RezervasyonDB;'
        'Trusted_Connection_True;'
    )
    return db.cursor()


imlec = connect_db(SERVER_ADI)

# Outlook bağlantısı
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Dosya bağlantısı
inbox = outlook.GetDefaultFolder(6)

# Mesajları almak
messages = inbox.Items
folders = inbox.Folders

# Output dosyası
output_dir = Path.cwd() / "Output"
output_dir.mkdir(parents=True, exist_ok=True)

current_time = datetime.now()

date_time = current_time.strftime("%m_%d_%Y_%H_%M_%S")
create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def check_email_existence(mail_id):
    imlec.execute("SELECT COUNT(*) FROM RezervasyonTb WHERE MailID = ?", (mail_id,))
    row_count = imlec.fetchone()[0]
    return row_count > 0


def check_new_mails_and_insert_into_db():
    sender_mail_address = "Boş"
    modified_target_folder = ""
    for message in messages:
        mail_id = message.EntryID
        if check_email_existence(mail_id[-10:]):
            print("Bu e-posta zaten var. Alınmayacak.")
            continue
        subject = message.Subject
        body = message.body
        attachments = message.Attachments
        if message.Class == 43:
            sender_mail_address = message.SenderEmailAddress

        # Diğer işlemler buraya
        # Her mesaj için farklı klasör açmak
        target_folder = output_dir / str(mail_id[-7:])
        target_folder.mkdir(parents=True, exist_ok=True)

        # Ekleri kaydetme
        for attachment in attachments:
            modified_target_folder = str(target_folder) + "\\" + str(attachment)
            print(modified_target_folder)
            print(type(modified_target_folder))
            attachment.SaveAsFile(target_folder / str(attachment))

        imlec.execute("insert into RezervasyonTb (FilePath, MailID, SenderMailAddress, IsRead, CreateDate)"
                      " values (?, ?, ?, 0, ?)",
                      (str(modified_target_folder), str(mail_id[-10:]), str(sender_mail_address), current_time))
        imlec.commit()


def select_from_db():
    imlec.execute("SELECT FilePath FROM RezervasyonTb WHERE IsRead = 0")
    rezervasyonlar = imlec.fetchall()
    return rezervasyonlar

