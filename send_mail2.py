import os
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import mimetypes
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def read_emails_from_csv_of_type(filename, email_types=None):
    df = pd.read_csv(filename)
    if email_types is not None:
        df = df[df['type'].isin(email_types)]
    return df['mails'].tolist()


def upload_to_drive(filename):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    
    file_drive = drive.CreateFile({'title': filename, "parents": [{"kind": "drive#fileLink","id": '1pQvgO8gQKy-oXBGiRVVb8XwtdEEhqVz4'}]})
    file_drive.SetContentFile(filename)
    file_drive.Upload()
    
    file_drive.InsertPermission({'type': 'anyone','value': 'anyone','role': 'reader'})
    
    return file_drive['alternateLink']


def send_mail(email_subject, filenames_to_attach, email_types=None, attach_pdf=True):
    if isinstance(filenames_to_attach, str):
        filenames_to_attach = [filenames_to_attach]
    email_sender = 'dpavez@crystal-lagoons.com'
    email_password = 'icqz fpqg boan wrlg'
    filename = 'mails.csv'

    emails = read_emails_from_csv_of_type(filename, email_types)
    subject = email_subject
    body = ''
    dwg_links = ''
    dwg_attached = False

    em = EmailMessage()

    text_part = EmailMessage()
    text_part.set_content('')

    for i, filename_to_attach in enumerate(filenames_to_attach, start=1):
        txt_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.txt')
        with open(txt_filename, 'r') as f:
            body += f'Part {i}:\n' + f.read() + '\n\n'

        dwg_filename = os.path.join('dwg', filename_to_attach + '.dwg')
        if os.path.exists(dwg_filename):
            if os.path.getsize(dwg_filename) > 25 * 1024 * 1024:
                if not dwg_attached:
                    file_link = upload_to_drive(dwg_filename)
                    dwg_links += f'DWG: {file_link}\n'
                    dwg_attached = True
            else:
                if not dwg_attached:
                    mime_type_dwg = 'application'
                    mime_subtype_dwg = 'octet-stream'
                    with open(dwg_filename, 'rb') as f:
                        em.add_attachment(f.read(),
                                        maintype=mime_type_dwg,
                                        subtype=mime_subtype_dwg,
                                        filename=os.path.basename(dwg_filename))
                    dwg_links = ""
                    dwg_attached = True
    body = body + dwg_links
    text_part.set_content(body)
    em.attach(text_part)

    em['From'] = email_sender
    em['To'] = email_sender if isinstance(email_sender, str) else ', '.join(email_sender)
    em['Cc'] = ', '.join(emails)
    em['Subject'] = subject

    for filename_to_attach in filenames_to_attach:
        if attach_pdf:
            pdf_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.pdf')
            mime_type_pdf, _ = mimetypes.guess_type(pdf_filename)
            mime_type_pdf, mime_subtype_pdf = mime_type_pdf.split('/')
            with open(pdf_filename, 'rb') as f:
                em.add_attachment(f.read(),
                                maintype=mime_type_pdf,
                                subtype=mime_subtype_pdf,
                                filename=os.path.basename(pdf_filename))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

# Call the function with required arguments
# send_mail(email_subject, filenames_to_attach)
