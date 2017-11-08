"""
Provide support for **POST** methods on uri://groups/*group* request.
"""
from django.http import JsonResponse

from openstack_registration.settings import LOGGER

from registration.decorators import superuser_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend


@superuser_required
def json(request, group):  # pylint: disable=unused-argument
    """
    JSON rendering for request *uri://groups/group*. It need:

    - superuser account: as superuser have access of all view.

    Call OpenLdapGroupBackend to create a group. The group will have requested user as default
    member & admin.

    :param request: Web request
    :param group: that will be created
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.groups.group.post.json: %s access to %s',
                 request.user.get_username(), group)
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
