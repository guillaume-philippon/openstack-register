"""
Manage all get method for users REST API
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.Backend import OpenLdapGroupBackend
from registration.decorators import owner_required


def json(request, group):
    """
    Return a HTML rendering for GET request in /users/*username*

    :param request: Web request
    :param group: group of the user
    :return: HTTP rendering
    """
    backend = OpenLdapGroupBackend()
    group = backend.get(group=group)
    print group
    # If the response is empty, then when want to create a new user. So we load register page
    if not group:
        response = JsonResponse({
            'status': 'GroupNotExist'
        })
    # else, we display the user information form.
    else:
        response = JsonResponse(group, safe=False)
    return response
