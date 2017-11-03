"""
This module dispatch the client request to the right view. It dispatch the request depending of:

- uri ( /users or /users/*username*)
- method ( GET / POST / PUT / DELETE )
- format ( json / HTML)

"""
from registration.api.users import get, user


def dispatcher(request, username):
    response = None
    if username is not None:
        response = user.dispatcher.dispatcher(request, username=username)
    else:
        if request.method == 'GET':
            if 'format' in request.GET and request.GET['format'] == 'json':
                response = get.json(request)
            else:
                response = get.html(request)
    return response

