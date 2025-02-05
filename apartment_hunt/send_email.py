from email.message import EmailMessage
import ssl
import smtplib

def send_email(url,contact):
    email_sender = 'obraunnn@gmail.com'
    password = 'djbumchmwzvueatu'
    email_receiver = contact

    subject = 'New apartment found'
    body = url

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context_ssl = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context_ssl) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
