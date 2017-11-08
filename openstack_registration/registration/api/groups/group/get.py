"""
Provide support for **GET** methods on uri://groups/*group* request.
"""
from django.shortcuts import render
from django.http import JsonResponse

from openstack_registration.settings import LOGGER

from registration.Backend import OpenLdapGroupBackend
from registration.decorators import groupadmin_required


# We need to have, @ least, groupadmin privilegies to list groups
@groupadmin_required
def json(request, group, attribute):  # pylint: disable=unused-argument
    """
    JSON rendering for request *uri://groups/group*. It need:

    - superuser account: as superuser have access to all view.
    - groupadmin acccess: allow groupadmin to get information of the group they manage. If
      user is not a admin of the group they try to get, so access is denied.

    :param request: Web request
    :param group: group that will be get
    :param attribute: only get this attribute of the group, used to get member list or
                      admin user list.
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.groups.group.get.json: %s access to %s',
                 request.user.get_username(), group)
    backend = OpenLdapGroupBackend()
    group = backend.get(group=group, attribute=attribute)
    # If the response is empty, then when want to create a new user. So we load register page
    if not group:
        response = JsonResponse({
            'status': 'GroupNotExist'
        })
    # else, we display the user information form.
    else:
        response = JsonResponse(group, safe=False)
    return response


@groupadmin_required
def html(request, group):  # pylint: disable=unused-argument
    """
    HTML rendering for GET request in *uri://groups/group*. It need:

    - superuser account: as superuser have access to all view.
    - groupadmin access: return the HTML rendering of group edition

    :param request: Web request
    :param group: group that will be get
    :return: HTTP rendering
    """
    return render(request, 'groups/group/home.html')
