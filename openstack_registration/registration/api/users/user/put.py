"""
Provide support for **PUT** methods on uri://users/username request.
"""
import json as core_json

from django.http import JsonResponse

from registration.decorators import owner_required
from registration.Backend.OpenLdap import OpenLdapUserBackend


@owner_required
def json(request, username):  # pylint: disable=unused-argument
    """
    JSON rendering for uri://users/*username* request. It need:

    - superuser account: as superuser always have access to view
    - owner access: allow user to update its own attributes

    It call OpenLdapUserBackend to modify user entry with data embedded in request.

    :param request: Web request
    :param username: user that will be modify
    :return: HTTP rendering
    """
    response = dict()
    ldap = OpenLdapUserBackend()
    attributes = core_json.loads(request.body.decode('utf-8'))
    ldap.modify(username=username, attributes=attributes)
    response = attributes
    return JsonResponse(response)
