"""
Provide RESTful API for uri://*users* request.
"""
from registration.api.users import user as users_user, get as users_get

from openstack_registration.settings import LOGGER


def dispatcher(request, username=None):
    """
    dispatcher function is defined on __init__ file to allow a clear call like: ::

      from registration import api
      api.users.dispatcher

    This dispatcher support:
        - **GET** method: for HTML & JSON rendering
        - forward request like *uri://groups/group*

    :param request: Web request
    :param username: Defined if we have a request like *uri://users/username*
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.users.dispatcher: %s uri:/%s',
                 request.method, request.path_info)
    response = None
    if username is not None:
        response = users_user.dispatcher(request, username=username)
    else:
        if request.method == 'GET':
            if 'format' in request.GET and request.GET['format'] == 'json':
                response = users_get.json(request)
            else:
                response = users_get.html(request)
    return response
