"""
Provide support for **GET** methods on uri://users/*username* request.
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.Backend import OpenLdapUserBackend
from registration.decorators import owner_required

from openstack_registration.settings import LOGGER


@owner_required
def html(request, username):
    """
    HTML rendering for GET uri://users/*username* request. It need:

    - superuser account: as superuser always have access to view
    - owner access: allow a user to have access to its own attributes

    :param request: Web request
    :param username: required by @owner_required decorator
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.users.user.get.html: %s access to %s',
                 request.user.get_username(), username)
    return render(request, 'users/user/home.html')


def json(request, username):
    """
    JSON rendering for GET uri://users/*username* request. It doesn't have any access control. If a
    user not exists, we return a json file with status **UserNotExist** it provide a easy way to
    check if username is available while creating a new account.

    :param request: Web request
    :param username: username
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.users.user.get.json: %s access to %s',
                 request.user.get_username(), username)
    backend = OpenLdapUserBackend()
    user = backend.get(username=username)
    # If the response is empty, then when want to create a new user. So we load register page
    if not user:
        response = {
            'status': 'UserNotExist'
        }
    # else, we display the user information form.
    else:
        response = user_information(request, username=username, data=user)
    return JsonResponse(response, safe=False)


@owner_required
def user_information(request, username, data):
    """
    To have access control on user information, we call user_information from json function. It
    need:

    - superuser account: as superuser always have access to view
    - owner access: allow a user to have access to its own attributes

    :param request: required for @owner_required decorator
    :param username: required for @owner_required decorator
    :param data: data that contains user attributes
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.users.user.put.user_information: %s access to %s',
                 request.user.get_username(), username)
    return data
