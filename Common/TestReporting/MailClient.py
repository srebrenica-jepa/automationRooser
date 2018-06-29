#! /usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..Utilities.Logging import PrintMessage


def send_mail(subject, html_body, m_from, m_to):
    message = MIMEMultipart()

    message['Subject'] = subject
    message['From'] = m_from
    message['To'] = ', '.join(m_to)

    message_body = MIMEText(html_body, 'html')
    message.attach(message_body)

    PrintMessage('Sending email to {0}'.format(m_to))

    # Send the message via local SMTP server.
    s = smtplib.SMTP('10.20.50.3')
    # s.set_debuglevel(1)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(message['From'], m_to, message.as_string())
    s.quit()
