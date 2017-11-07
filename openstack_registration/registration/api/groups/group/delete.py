"""
Provide support for **DELETE** methods on uri://groups/*group* request.
"""
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from registration.decorators import groupadmin_required, superuser_protection, self_protection
from registration.Backend.OpenLdap import OpenLdapGroupBackend
from registration.Backend.Exceptions import AdminGroupDelete


@groupadmin_required
@superuser_protection
@self_protection
def json(request, group, attribute, value):  # pylint: disable=unused-argument
    """
    It call OpenLdapGroupBackend to delete group or attribute in group.

    If attribute is None, then **group** will be deleted to openldap. Else, we remove **value**
    entry to group. **attribute** is used to add or remove user into a group.

    :param request: Web request required by @groupadmin_required / @superuser_protection /
                    @self_protection
    :param group: group that will be affected
    :param attribute: attribute that will be affected (if not None)
    :param value: value that will be affected (if not None)
    :return: HTTP rendering
    """
    ldap = OpenLdapGroupBackend()
    try:
        ldap.delete(group, attribute, value)
    except AdminGroupDelete:
        raise PermissionDenied
    return JsonResponse({
        'status': 'success'
    })
