"""
Provide support for **GET** methods on uri://groups/ request.
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.decorators import groupadmin_required
from registration.Backend import OpenLdapGroupBackend


@groupadmin_required
def html(request):
    """
    HTML rendering for request *uri://groups/*. It need:

    - superuser account: as superuser always have acces to view
    - groupadmin access: group admin share the same HTML rendering that superusers.

    :param request: Web request
    :return: HTTP rendering
    """
    response = render(request, "groups/home.html")
    return response


@groupadmin_required
def json(request):  # pylint: disable=unused-argument
    """
    JSON rendering for request *uri://groups/*. It need:

    - superuser account: as superuser always have access to view
    - groupadmin access: group admin can have a list of group even they only manage a part of them.
      Of course, they don't have access to groups they don't manage.

    :param request: required for @groupadmin_required decorators
    :return: HTTP rendering
    """
    ldap = OpenLdapGroupBackend()
    return JsonResponse(ldap.get(), safe=None)
