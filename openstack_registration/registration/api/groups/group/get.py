"""
Manage all get method for users REST API
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.Backend import OpenLdapGroupBackend
from registration.decorators import groupadmin_required


# We need to have, @ least, groupadmin privilegies to list groups
@groupadmin_required
def json(request, group, attribute):
    """
    Return a Json rendering for GET request in /groups/*group*

    :param request: Web request
    :param group: group of the user
    :return: HTTP rendering
    """
    backend = OpenLdapGroupBackend()
    group = backend.get(group=group, attribute=attribute)
    # If the response is empty, then when want to create a new user. So we load register page
    if not group:
        response = JsonResponse({
            'status': 'GroupNotExist'
        })
    # else, we display the user information form.
    else:
        response = JsonResponse(group, safe=False)
    return response


@groupadmin_required
def html(request, group):
    """
    Return a HTML rendering for GET request in /groups/*group*

    :param request: Web request
    :param group: group
    :return: HTTP rendering
    """
    return render(request, 'groups/group/home.html')
