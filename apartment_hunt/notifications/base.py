from ..models.apartment import ApartmentListing  
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib

class Notifier():
    def __init__(self,
                 apartment_list: list[ApartmentListing],
                 user_email: str,
                 price_filter: ApartmentListing.price = 9999,
                 size_filter: ApartmentListing.size = 1,
                 rooms_filter: ApartmentListing.rooms = 1,
                 wbs_filter: ApartmentListing.wbs = 0
                 ):
        self.apartment_list = apartment_list
        self.user_email = user_email
        self.price_filter = price_filter
        self.rooms_filter = rooms_filter
        self.size_filter = size_filter
        self.wbs_filter = wbs_filter

        #self.processing_notifications()

    def send_email(self, url):
        email_sender = 'obraunnn@gmail.com'
        password = 'djbumchmwzvueatu'
        email_receiver = self.user_email

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

    def process_notifications(self):
        counter = 0
        for apartment in self.apartment_list:
            if (apartment.price <= self.price_filter 
            and apartment.size >= self.size_filter
            and apartment.rooms >= self.rooms_filter
            and apartment.wbs <= self.wbs_filter
            and apartment.currently_available == 1
            and apartment.email_sent == 0):
                self.send_email(apartment.url)
                counter = counter + 1
        print(str(counter) + " apartments emailed to " + self.user_email)
