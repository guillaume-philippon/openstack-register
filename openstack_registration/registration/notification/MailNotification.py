"""
Provide support for mail notification.
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smtplib import SMTP, SMTP_SSL

from openstack_registration.config import GLOBAL_CONFIG

MAIL_CONTENT = """
Dear {firstname} {lastname},

Your account as been successfully created. You still must belong to a project to use the plateform.
Please, contact your project administrator to be allowed to connect to https://keystone.lal.in2p3.fr.

Information account:
    - domain: stratuslab
    - username: {username}

Support: https://cloud-support.lal.in2p3.fr

---
Openstack Cloud Team
"""


class MailNotification(object):  # pylint: disable=too-few-public-methods
    """
    Provide support to interact with mail server and let openstack-registration notify user when a
    account is created.
    """
    def __init__(self):
        """
        Initialize mail notification object
        """
        self.server = GLOBAL_CONFIG['MAIL_SERVER']
        self.from_header = GLOBAL_CONFIG['MAIL_FROM']
        self.bcc_header = GLOBAL_CONFIG['MAIL_ADMIN']
        if 'MAIL_USERNAME' in GLOBAL_CONFIG:
            self.smtp = SMTP_SSL(self.server)
            self.smtp.login(GLOBAL_CONFIG['MAIL_USERNAME'],
                            GLOBAL_CONFIG['MAIL_PASSWORD'])
        else:
            self.smtp = SMTP(self.server)
        self.subject = "Openstack Registration Message"

    def notify(self, user):
        """
        Sent a mail to user and administrator.

        :param user: user to notify
        :return: void
        """
        # create header
        header = MIMEMultipart()
        header['From'] = self.from_header
        header['To'] = user['email']
        header['Subject'] = self.subject
        header['Bcc'] = self.bcc_header
        header.attach(MIMEText(MAIL_CONTENT.format(**user)))
        recipients = GLOBAL_CONFIG['MAIL_ADMIN'].split(',') + [user['email']]

        # connect to mail server and send the email
        self.smtp.sendmail(GLOBAL_CONFIG['MAIL_FROM'], recipients, header.as_string())
