"""
Provide RESTful API for uri://groups/**group** request
"""
from registration.api.groups.group import get as group_get, \
    post as group_post, \
    delete as group_delete


def dispatcher(request, group, attribute):
    """
    dispatcher function is defined on __init__ file to avoid some strange call and have a clear call
    like:
    .. code: python

        from registration import api
        api.users.user.dispatcher

    :param request: Web request
    :param group: group
    :return: HTTP rendering
    """
    response = None
    if request.method == 'GET':
        if 'format' in request.GET and request.GET['format'] == 'json':
            response = group_get.json(request, group=group, attribute=attribute)
        else:
            # We don't have specific view for attribute, so we return the same HTML view than
            # user
            response = group_get.html(request, group=group)
    elif request.method == 'POST':
        response = group_post.json(request, group=group)
    elif request.method == 'DELETE':
        response = group_delete.json(request, group=group)
    return response
