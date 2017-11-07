"""
Provide support for all *PUT* method to uri://users/*username*. *PUT* method will allow
user creation. You will raise AlreadyExist exception if user exist.
"""
from django.http import JsonResponse

from registration.decorators import groupadmin_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend


@groupadmin_required
def json(request, group, attribute, value):  # pylint: disable=unused-argument
    """
    Create a user based on request content and username uri

    :param request: Web request
    :param group: username
    :param attribute: attribute name
    :param value: attribute value
    :return: Json rendering
    """
    ldap = OpenLdapGroupBackend()

    # attributes = {
    #     'username': request.user.get_username(),
    #     'name': group,
    #     'description': request.POST['description']
    # }
    # ldap.modify(attributes)
    ldap.modify(group, attribute, value)
    response = JsonResponse({
        'status': 'success'
    })
    return response
