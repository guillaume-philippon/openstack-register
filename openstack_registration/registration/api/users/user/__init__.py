"""
Provide RESTful API for uri://users/*username* request.
"""
from registration.api.users.user import get as user_get
from registration.api.users.user import post as user_post
from registration.api.users.user import put as user_put
from registration.api.users.user import delete as user_delete


def dispatcher(request, username):
    """
    dispatcher function is defined on __init__ file to allow a clear call like: ::

      from registration import api
      api.users.user.dispatcher

    This dispatcher support:
        - **GET** method: for HTML & JSON rendering
        - **POST** method: for JSON rendering
        - **PUT** method: for JSON rendering
        - **DELETE** method: for JSON rendering

    :param request: Web request
    :param username: user that will be involved in action.
    :return: HTTP rendering
    """
    response = None
    if request.method == "GET":
        if 'format' in request.GET and request.GET['format'] == 'json':
            response = user_get.json(request, username=username)
        else:
            response = user_get.html(request, username=username)
    elif request.method == "POST":
        response = user_post.json(request, username=username)
    elif request.method == "PUT":
        response = user_put.json(request, username=username)
    elif request.method == "DELETE":
        response = user_delete.json(request, username=username)
    return response
