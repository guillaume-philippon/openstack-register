"""
Provide RESTful API for uri://groups request based on:

- **method**: (GET / POST / PUT / DELETE)
- **format**: (json / HTTP)

"""
from registration.api.groups import group as groups_group, get as groups_get


def dispatcher(request, group=None, attribute=None, value=None):
    """
    dispatcher function is defined on __init__ file to avoid some strange call and have a clear call
    like:
    .. code: python

        from registration import api
        api.groups.dispatcher

    :param attribute: specific attribute is ask
    :param request: Web request
    :param group: group
    :param value: group
    :return: HTTP rendering
    """
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
