"""
Manage all get method for users REST API
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from registration.Backend import OpenLdap


@login_required()
def html(request):
    """
    Return a HTML rendering for GET request in /users/*username*

    :param request: Web request
    :return: HTTP
    """
    return render(request, 'users/user.html')


@login_required()
def json(request, username):
    """
    Return a Json rendering for GET request in /users/*username*

    :param request: Web request
    :param username: username
    :return: JsonResponse
    """
    if request.user == username:
        backend = OpenLdap()
        response = backend.get(username=username)
    else:
        raise PermissionDenied
    return JsonResponse(response, safe=False)
