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

def write_link_to_txt(txt_filename, link):
    with open(txt_filename, 'a') as f:
        f.write(f'\nLink to DWG file: {link}\n')


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


def send_mail(email_subject, filenames_to_attach, email_types=None, attach_pdf=True, recipients=None):
    if isinstance(filenames_to_attach, str):
        filenames_to_attach = [filenames_to_attach]
    email_sender = 'dpavez@crystal-lagoons.com'
    email_password = 'wzda cjzm ursc whld'
    filename = 'mails.csv'

    #emails = read_emails_from_csv_of_type(filename, email_types)

    subject = email_subject

    body = ''

    dwg_links = ''
    dwg_attached = False
    text_part = EmailMessage()
    text_part.set_content('')


    for i, filename_to_attach in enumerate(filenames_to_attach, start=1):
        # Get the email body from the text file
        txt_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.txt')
        with open(txt_filename, 'r') as f:
            # Add a title before each part
            body += f'Part {i}:\n' + f.read() + '\n\n'
    
    if recipients is None:
        recipients = []
    
    em = EmailMessage()

    em['From'] = email_sender.join(recipients)
    em['To'] = email_sender  # Send to your own email
    #em['Cc'] = ', '.join(emails)  # CC all emails
    em['Subject'] = subject
    em.set_content(body)

    for filename_to_attach in filenames_to_attach:
        if attach_pdf:
            # Construct the paths to the files to attach
            pdf_filename = os.path.join('TEXs', filename_to_attach, filename_to_attach + '.pdf')
            mime_type_pdf, _ = mimetypes.guess_type(pdf_filename)
            mime_type_pdf, mime_subtype_pdf = mime_type_pdf.split('/')
            with open(pdf_filename, 'rb') as f:
                em.add_attachment(f.read(),
                                maintype=mime_type_pdf,
                                subtype=mime_subtype_pdf,
                                filename=os.path.basename(pdf_filename))

        # Attach the DWG file if it exists and no DWG has been attached yet
        if not dwg_attached:
            dwg_filename = os.path.join('dwg', filename_to_attach + '.dwg')
            if os.path.exists(dwg_filename):
                if os.path.getsize(dwg_filename) > 25 * 1024 * 1024:
                    file_link = upload_to_drive(dwg_filename)
                    write_link_to_txt(txt_filename, file_link)
                    os.remove(dwg_filename)
                    dwg_links += f'DWG: {file_link}\n'
                    dwg_attached = True
                    body = body + dwg_links
                    em.set_content(body)



                else:
                    mime_type_dwg = 'application'
                    mime_subtype_dwg = 'octet-stream'  # generic byte stream type
                    with open(dwg_filename, 'rb') as f:
                        em.add_attachment(f.read(),
                                        maintype=mime_type_dwg,
                                        subtype=mime_subtype_dwg,
                                        filename=os.path.basename(dwg_filename))
                    dwg_attached = True  # Update the flag to indicate that a DWG has been attached

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

def send_mail_travel(email_subject, filenames_to_attach, recipients):
    email_sender = 'dpavez@crystal-lagoons.com'
    email_password = 'wzda cjzm ursc whld'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = ', '.join(recipients)
    em['Subject'] = email_subject

    # Set the body of the email
    em.set_content("Please find the attached documents.")

    # Attach files
    for filename_to_attach in filenames_to_attach:
        # Determine the MIME type and subtype
        mime_type, _ = mimetypes.guess_type(filename_to_attach)
        if mime_type is None:  # If the MIME type is not identifiable
            mime_type = 'application/octet-stream'
        mime_type, mime_subtype = mime_type.split('/', 1)

        with open(filename_to_attach, 'rb') as f:
            em.add_attachment(f.read(),
                              maintype=mime_type,
                              subtype=mime_subtype,
                              filename=os.path.basename(filename_to_attach))

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)


def send_travel_request(email_sender, name, area, solicitud):
    # Read users data
    users_df = pd.read_csv('users.csv')

    # Find director's email for the specified area
    director_email = users_df[(users_df['position'] == 'director') & (users_df['area'] == area)]['username'].iloc[0]

    # Find secretary's email
    #secretary_email = users_df[users_df['area'] == 'Secretary']['username'].iloc[0]

    # Subject for the email
    email_subject = f"Travel Request Form from {name}"

    # Find the required files in the formularios_viaje folder
    folder_path = 'formularios_viaje'
    files_to_attach = []
    for file_extension in ['.pdf', '.xlsx', '.png']:
        file_path = os.path.join(folder_path, f"{solicitud}{file_extension}")
        if os.path.exists(file_path):
            files_to_attach.append(file_path)

    # Send the email
    send_mail_travel(email_subject, files_to_attach, recipients=[director_email, email_sender])


def send_travel_resolution(email_sender, name, solicitud, status, comment):
    # Read users data
    users_df = pd.read_csv('users.csv')

    # Find director's email for the specified area
    #director_email = users_df[(users_df['position'] == 'director') & (users_df['area'] == area)]['username'].iloc[0]

    # Find secretary's email
    secretary_email = users_df[users_df['area'] == 'Secretary']['username'].iloc[0]

    # Subject for the email based on approval status
    if status.lower() == 'approved':
        email_subject = f"Approved Travel Request Form from {name}"
    elif status.lower() == 'rejected':
        email_subject = f"Rejected Travel Request Form from {name}"
    else:
        raise ValueError("Invalid status. Status must be 'approved' or 'rejected'.")

    # Find the required files in the formularios_viaje folder
    folder_path = 'formularios_viaje'
    files_to_attach = []
    for file_extension in ['.pdf', '.xlsx', '.png']:
        file_path = os.path.join(folder_path, f"{solicitud}{file_extension}")
        if os.path.exists(file_path):
            files_to_attach.append(file_path)

    # Send the email
    send_mail_travel_status(email_subject, files_to_attach, comment, recipients=[secretary_email, email_sender])


def send_mail_travel_status(email_subject, filenames_to_attach, comment, recipients):
    email_sender = 'dpavez@crystal-lagoons.com'
    email_password = 'wzda cjzm ursc whld'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = ', '.join(recipients)
    em['Subject'] = email_subject

    # Set the body of the email with the provided comment
    em.set_content(comment)

    # Attach files
    for filename_to_attach in filenames_to_attach:
        # Determine the MIME type and subtype
        mime_type, _ = mimetypes.guess_type(filename_to_attach)
        if mime_type is None:  # If the MIME type is not identifiable
            mime_type = 'application/octet-stream'
        mime_type, mime_subtype = mime_type.split('/', 1)

        with open(filename_to_attach, 'rb') as f:
            em.add_attachment(f.read(),
                              maintype=mime_type,
                              subtype=mime_subtype,
                              filename=os.path.basename(filename_to_attach))

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
