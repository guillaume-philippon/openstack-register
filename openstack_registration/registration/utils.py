"""
Some usefull function of registration module
"""
# -*- coding: utf-8 -*-

import os
import hashlib
import unicodedata
import re
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
from datetime import datetime

from registration.models import UserActivation, UserInfo, GroupInfo, IsAdmin

LOGGER = logging.getLogger("registration")


def encode_password(password):
    """
    Encodes the given password as a base64 SSHA hash+salt buffer
    :param password:
    """
    salt = os.urandom(4)

    # hash the password and append the salt
    sha = hashlib.sha1(password)
    sha.update(salt)

    # create a base64 encoded string of the concatenated digest + salt
    digest_salt_b64 = '{}{}'.format(sha.digest(), salt).encode('base64').strip()

    # now tag the digest above with the {SSHA} tag
    tagged_digest_salt = '{{SSHA}}{}'.format(digest_salt_b64)

    return tagged_digest_salt


def check_password(tagged_digest_salt, password):
    """
    Checks the OpenLDAP tagged digest against the given password
    :param tagged_digest_salt:
    :param password:
    """
    # the entire payload is base64-encoded
    assert tagged_digest_salt.startswith('{SSHA}')

    # strip off the hash label
    digest_salt_b64 = tagged_digest_salt[6:]

    # the password+salt buffer is also base64-encoded.  decode and split the
    # digest and salt
    digest_salt = digest_salt_b64.decode('base64')
    digest = digest_salt[:20]
    salt = digest_salt[20:]

    sha = hashlib.sha1(password)
    sha.update(salt)

    return digest == sha.digest()


def check_password_constraints(password):  # pylint: disable: too-many-branches
    """

    :param password:
    :return:
    """
    attributes = {}
    # password = request.GET['password']
    constraint = {'lower': False,
                  'upper': False,
                  'spe': False,
                  'number': False}
    index = 0
    total = 0
    taille = len(password)
    spe = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
           '{', '}', '"', ':', ';', '\', ''', '[', ']', '<', '>']

    while index < taille:
        var = password[index]
        if var.islower():
            constraint['lower'] = True
        if var.isupper():
            constraint['upper'] = True
        if var in spe:
            constraint['spe'] = True
        if var.isdigit():
            constraint['number'] = True
        index += 1

    if constraint['lower']:
        total += 1
    if constraint['upper']:
        total += 1
    if constraint['spe']:
        total += 1
    if constraint['number']:
        total += 1

    if len(password) < 8:
        attributes['check'] = 'character'
    elif total < 3:
        attributes['check'] = 'require'
    elif len(password) >= 8 and total >= 3:
        attributes['check'] = 'success'
    else:
        attributes['check'] = 'error'
    return attributes


def normalize_string(string, option=None):
    """

    :param string:
    :param option:
    :return:
    """
    if option is None or option == 'username':
        return re.sub(r'[\W_]', '',
                      unicodedata.normalize('NFKD', string)
                      .encode('ASCII', 'ignore').lower())
    elif option == 'name':
        return re.sub(r'[\s]', '-',
                      re.sub(r'[^a-zA-Z, -]', '',
                             unicodedata.normalize('NFKD', string)
                             .encode('ASCII', 'ignore').lower()))


def send_mail(username, firstname, lastname, user_email, project, admin_mail, action):  # pylint: disable: too-many-branches
    """

    :param username:
    :param firstname:
    :param lastname:
    :param user_email:
    :param admin_mail:
    :param action:
    :return:
    """
    message = ''
    all_rcpt = ''
    header = MIMEMultipart()
    header['From'] = 'no-reply@lal.in2p3.fr'
    header['To'] = user_email
    header['Subject'] = 'OpenStack Registration Message'

    if action == 'add':
        all_rcpt = user_email
        random_string = uuid.uuid4()
        link = "https://registration.lal.in2p3.fr/action/{}".format(random_string)
        message = "Dear {} {}, \n\nYou just created an account on OpenStack@lal.\n" \
                  "Please follow the link to activate your account: \n{}\n\n" \
                  "You can have access to your profile on the registration " \
                  "website but YOU ARE NOT ABLE TO AUTHENTICATE ON THE CLOUD " \
                  "UNTIL ENABLED." \
                  "\n\nDon't reply at this email.\n" \
                  "Support : https://cloud-support.lal.in2p3.fr/"\
                  .format(firstname,
                          lastname,
                          link)
        add_entry_user_activation(random_string, username)

    elif action == 'enable':
        all_rcpt = str(admin_mail).split(',') + [user_email]
        header['Bcc'] = str(admin_mail)
        message = "Dear {} {}, \n\nYour account have been successfully " \
                  "activated.\n" \
                  "You still must belong to a project to use the platform.\n" \
                  "Please contact your project administrator to be allowed " \
                  "to connect to https://keystone.lal.in2p3.fr. \n\n" \
                  "Your domain is 'stratuslab'.\n" \
                  "Your Username is '{}'.\n" \
                  "Project you want to be added : {}\n" \
                  "\n\nDon't reply at this email.\n" \
                  "Support : https://cloud-support.lal.in2p3.fr/"\
                  .format(firstname,
                          lastname,
                          username,
                          project)
        add_entry_user_info(username, datetime.now())

    header.attach(MIMEText(message))
    mail_server = smtplib.SMTP('smtp.lal.in2p3.fr', 25)
    mail_server.sendmail('no-reply@lal.in2p3.fr', all_rcpt, header.as_string())

    mail_server.quit()


def add_entry_user_activation(random_string, user):
    """

    :param random_string:
    :param user:
    :return:
    """
    new_user = UserActivation(link=random_string, username=user)
    new_user.save()


def add_entry_user_info(user, date):
    """

    :param user:
    :param date:
    :return:
    """
    new_user = UserInfo(username=user, last_agreement=date, enabled=True)
    new_user.save()


def add_entry_group_info(group):
    """

    :param group:
    :return:
    """
    new_group = GroupInfo(group_name=group)
    new_group.save()


def add_entry_is_admin(user, group):
    """

    :param user:
    :param group:
    :return:
    """
    user_id = UserInfo.objects.filter(username=user)[0].id  # pylint: disable=no-member
    exist_user = UserInfo.objects.get(id=user_id)  # pylint: disable=no-member
    group_id = GroupInfo.objects.filter(group_name=group)[0].id  # pylint: disable=no-member
    exist_group = GroupInfo.objects.get(id=group_id)  # pylint: disable=no-member
    new_admin = IsAdmin(administrators=exist_user, group=exist_group)
    new_admin.save()


def del_entry_is_admin(user, group):
    """

    :param user:
    :param group:
    :return:
    """
    user_id = UserInfo.objects.filter(username=user)[0].id  # pylint: disable=no-member
    exist_user = UserInfo.objects.get(id=user_id)  # pylint: disable=no-member
    group_id = GroupInfo.objects.filter(group_name=group)[0].id  # pylint: disable=no-member
    exist_group = GroupInfo.objects.get(id=group_id)  # pylint: disable=no-member
    admin = IsAdmin.objects.filter(administrators=exist_user, group=exist_group)  # pylint: disable=no-member
    admin.delete()


def update_entry_user_info(user, value):
    """

    :param user:
    :param value:
    :return:
    """
    data = dict()
    try:
        existing_user = UserInfo.objects.filter(username=user)
        existing_user.update(admin=value)
        data['status'] = 'True'
    except:  # pylint: disable=bare-except
        data['status'] = 'False'
    return data


def update_count_force(user, action):
    """

    :param user:
    :param action:
    :return:
    """
    try:
        existing_user = UserInfo.objects.filter(username=user)
        if action == 'add':
            value = existing_user[0].countForce + 1
        else:
            value = existing_user[0].countForce - 1
        existing_user.update(countForce=value)
    except:  # pylint: disable=bare-except
        pass
