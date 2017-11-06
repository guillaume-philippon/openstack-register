"""
Provide support for uri://groups/*group* call with **DELETE** HTTP method
"""
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from registration.decorators import superuser_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend
from registration.Backend.Exceptions import AdminGroupDelete

@superuser_required
def json(request, group):
    """
    Delete group.

    :param request: Web request
    :param groupname: groupname to delete
    :return: JSonResponse
    """
    ldap = OpenLdapGroupBackend()
    try:
        ldap.delete(group)
    except AdminGroupDelete:
        raise PermissionDenied
    return JsonResponse({
        'status': 'success'
    })
