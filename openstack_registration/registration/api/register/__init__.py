"""
Provide a support for uri://register call
"""
from registration.api.register import get as register_get


def dispatcher(request):
    """
    dispatcher function is defined on __init__ file to avoid some strange call and have a clear call
    like :
    .. code: python

      from registration import api
      api.register.dispatcher

    :param request: Web request
    :return: HTTP rendering
    """
    response = None
    if request.method == 'GET':
        if 'format' in request.GET and request.GET['format'] == 'json':
            response = register_get.json(request)
        else:
            response = register_get.html(request)
    return response
