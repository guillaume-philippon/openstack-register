"""
Provide RESTful API for uri://users/*username* request
"""
from registration.api.users.user import get as user_get


def dispatcher(request, username):
    """
    dispatcher function is defined on __init__ file to avoid some strange call and have a clear call
    like :
    .. code: python

      from registration import api
      api.users.user.dispatcher

    :param request: Web request
    :param username: username
    :return: HTTP rendering
    """
    response = None
    if request.method == "GET":
        if 'format' in request.GET and request.GET['format'] == 'json':
            response = user_get.json(request, username=username)
        else:
            response = user_get.html(request, username=username)
    return response
