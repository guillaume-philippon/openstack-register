"""
Provide support for **GET** methods on uri://users/ request.
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.decorators import superuser_required, groupadmin_required
from registration.Backend import OpenLdapUserBackend

from openstack_registration.settings import LOGGER


@superuser_required
def html(request):
    """
    HTML rendering for uri://*users*. It need superuser privilegies to access it

    :param request: Web request
    :return: HTTP rendering
    """
    response = render(request, "users/home.html")
    return response


@groupadmin_required
def json(request):  # pylint: disable=unused-argument
    """
    JSON rendering for uri://*users*. It need:

    - superuser account: a superuser account always have access to all view
    - groupadmin access: a group admin is a user that can add / remove user from a group. So, he
      need to list all users available.

    :param request: required by @groupadmin_required decorator
    :return: JSON rendering
    """
    LOGGER.debug('%s get whole list of users', request.user.get_username())
    ldap = OpenLdapUserBackend()
    return JsonResponse(ldap.get(), safe=None)
