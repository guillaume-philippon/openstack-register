"""
Provide support for **PUT** methods on uri://groups/*group* request.
"""
from django.http import JsonResponse

from openstack_registration.settings import LOGGER

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
    LOGGER.debug('registration.api.groups.group.put.json: %s access to %s',
                 request.user.get_username(), group)
    ldap = OpenLdapGroupBackend()

    ldap.modify(group, attribute, value)
    response = JsonResponse({
        'status': 'success'
    })
    return response
