"""
Provide support for all *POST* method to uri://users/*username*. *POST* method will allow
user creation. You will raise AlreadyExist exception if user exist.
"""
from django.http import JsonResponse

from registration.decorators import superuser_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend


@superuser_required
def json(request, group):  # pylint: disable=unused-argument
    """
    Create a user based on request content and username uri

    :param request: Web request
    :param name: username
    :return: Json rendering
    """
    ldap = OpenLdapGroupBackend()

    attributes = {
        'username': request.user.get_username(),
        'name': group,
        'description': request.POST['description']
    }
    ldap.create(attributes)
    response = JsonResponse({
        'status': 'success'
    })
    return response
