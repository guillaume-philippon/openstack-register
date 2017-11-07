"""
Manage all get method for users REST API
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.Backend import OpenLdapUserBackend
from registration.decorators import owner_required


@owner_required
def html(request, username):  # pylint: disable=unused-argument
    """
    Return a HTML rendering for GET request in /users/*username*

    :param request: Web request
    :param username: username of the user
    :return: HTTP
    """
    return render(request, 'users/user/home.html')


def json(request, username):  # pylint: disable=unused-argument
    """
    Return a Json rendering for GET request in /users/*username*

    :param request: Web request
    :param username: username
    :return: JsonResponses
    """
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
def user_information(request, username, data):  # pylint: disable=unused-argument
    """
    To have a easiest permission support, we split user information rendering and we decorate
    function with @owner_required.

    :param request: required for @owner_required decorator
    :param username: required for @owner_required decorator
    :param data: required for @owner_required decorator
    :return: HTTP rendering
    """
    return data
