"""

"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from registration.decorators import owner_required


@login_required
def html(request):
    """
    make desc.

    :param request: Web request
    :return: void
    """
    # response = redirect('/')
    # if user_is_admin(request, spec='python')['admin'] != 'False':
    response = render(request, "users/users.html")
    return response


