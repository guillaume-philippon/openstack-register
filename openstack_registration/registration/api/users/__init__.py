"""
Provide RESTful API for uri://*users* request.
"""
from registration.api.users import user as users_user, get as users_get


def dispatcher(request, username=None):
    """
    dispatcher function is defined on __init__ file to allow a clear call like: ::

      from registration import api
      api.users.dispatcher

    :param request: Web request
    :param username: username
    :return: HTTP rendering
    """
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
