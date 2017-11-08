"""
Provide RESTful API for uri://*groups* request.
"""
from registration.api.groups import group as groups_group, get as groups_get

from openstack_registration.settings import LOGGER


def dispatcher(request, group=None, attribute=None, value=None):
    """
    dispatcher function is defined on __init__ file to allow a clear call like: ::

        from registration import api
        api.groups.dispatcher

    This dispatcher support:
        - **GET** method: for HTML & JSON rendering
        - forward request like *uri://groups/group*

    :param request: Web request
    :param group: Defined if we have a request like *uri://groups/group*
    :param attribute: Defined if we have a request like *uri://groups/group/attribute*
    :param value: Defined if we have a request like *uri://groups/group/attribute/value*
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.groups.dispatcher: %s uri:/%s',
                 request.method, request.path_info)
    response = None
    if group is not None:
        response = groups_group.dispatcher(request, group=group, attribute=attribute, value=value)
    else:
        if request.method == 'GET':
            if 'format' in request.GET and request.GET['format'] == 'json':
                response = groups_get.json(request)
            else:
                response = groups_get.html(request)
    return response
