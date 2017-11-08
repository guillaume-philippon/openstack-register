"""
Provide support for **POST** methods on uri://users/username request.
"""
import ast

from django.http import JsonResponse
from django.contrib import auth

from openstack_registration.config import GLOBAL_CONFIG
from openstack_registration.settings import LOGGER

from registration.Backend.OpenLdap import OpenLdapUserBackend
from registration.notification.MailNotification import MailNotification


def json(request, username):
    """
    JSON rendering for POST uri://users/*username* request.

    It call OpenLdapUserBackend to create a openldap user and call MailNotification to notify both
    user and administrator when a new account is created. It also, log the user after creation and
    redirect him to its own web page.

    As openstack-registration is based on self-created account process, we don't have any access
    control to this view.

    :param request: Web request which contains user attributes
    :param username: username that will be used for user.
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.users.user.post.json: %s',
                 username)
    ldap = OpenLdapUserBackend()
    notification = MailNotification()

    attributes = {
        'username': username,
        'lastname': request.POST['lastname'],
        'firstname': request.POST['firstname'],
        'password': request.POST['password'],
        'email': request.POST['email']
    }
    ldap.create(attributes)
    if ast.literal_eval(GLOBAL_CONFIG['MAIL_ENABLE']):
        notification.notify(attributes)

    # After creating the user, we automaticaly logged him
    user = auth.authenticate(username=username,
                             password=request.POST['password'])
    # If user is not None, then user is authenticated
    if user is not None:
        auth.login(request, user)
        response = JsonResponse({
            'status': 'success'
        })
    # else the username or password is invalid. It should not happen
    else:
        response = JsonResponse({
            'status': 'failure',
            'message': 'invalid username or password'
        })

    return response
