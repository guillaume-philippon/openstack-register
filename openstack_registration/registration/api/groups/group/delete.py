"""
Provide support for uri://groups/*group* call with **DELETE** HTTP method
"""
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from registration.decorators import groupadmin_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend
from registration.Backend.Exceptions import AdminGroupDelete


@groupadmin_required
def json(request, group, attribute, value):
    """
    Delete group.

    :param request: Web request
    :param group: groupname to delete
    :param attribute: groupname to delete
    :param value: groupname to delete
    :return: JSonResponse
    """
    ldap = OpenLdapGroupBackend()
    if request.user.get_username() == value:
        raise PermissionDenied
    try:
        if attribute is None and not request.user.is_superuser:
            raise PermissionDenied
        ldap.delete(group, attribute, value)
    except AdminGroupDelete:
        raise PermissionDenied
    return JsonResponse({
        'status': 'success'
    })
