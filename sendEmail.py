import requests
import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEBase import MIMEBase
# from email.MIMEText import MIMEText
# from email.Utils import COMMASPACE, formatdate
# from email import Encoders
import os
import datetime


def send_email(user, pwd, recipient, subject, body):
    """INPUT: gmail username, gmail password, a list of recipients, a subject, and a body"""
    gmail_user  = user
    gmail_pwd   = pwd
    FROM        = user
    TO          = recipient if type(recipient) is list else [recipient]
    SUBJECT     = subject
    TEXT        = body

    # prepare actual message
    message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) # start Simple Mail Transfer Protocol server on port 587
        server.ehlo() # establish connection
        server.starttls() # put communication in Transport Layer Security mode, encrypting all data
        server.ehlo() # second time
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.quit()
        print("Mail sent")
    except Exception as e:
        print("failed to send mail, " + str(e))

import smtplib


def send_mail(send_from, send_to, subject, text, files=None, server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()