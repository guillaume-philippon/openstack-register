"""
Provide support for all *POST* method to uri://users/*username*. *POST* method will allow
user creation. You will raise AlreadyExist exception if user exist.
"""
import json as core_json

from django.http import JsonResponse

from registration.decorators import owner_required
from registration.Backend.OpenLdap import OpenLdapUserBackend


@owner_required
def json(request, username):  # pylint: disable=unused-argument
    """
    Create a user based on request content and username uri

    :param request: Web request
    :param username: username
    :return: Json rendering
    """
    response = dict()
    ldap = OpenLdapUserBackend()
    attributes = core_json.loads(request.body.decode('utf-8'))
    ldap.modify(username=username, attributes=attributes)
    response = attributes
    return JsonResponse(response)
