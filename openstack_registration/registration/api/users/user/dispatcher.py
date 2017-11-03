"""
This module dispatch the client request to the right view. It dispatch the request depending of:

- method ( GET / POST / PUT / DELETE )
- format ( json / HTML)

"""
from registration.api.users.user import get


def dispatcher(request, username):
    response = None
    if request.method == "GET":
        if 'format' in request.GET and request.GET['format'] == 'json':
            response = get.json(request, username=username)
        else:
            response = get.html(request, username=username)
    return response
