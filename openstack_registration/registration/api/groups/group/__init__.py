"""
Provide RESTful API for uri://groups/*group* request.
"""
from django.http import JsonResponse

from registration.api.groups.group import get as group_get, \
    post as group_post, \
    delete as group_delete, \
    put as group_put

from openstack_registration.settings import LOGGER


def dispatcher(request, group, attribute, value):
    """
    dispatcher function is defined on __init__ file to allow a clear call like: ::

        from registration import api
        api.groups.group.dispatcher

    This dispatcher support:
        - **GET** method: for HTML & JSON rendering
        - **POST** method: for JSON rendering
        - **DELETE** method: for JSON rendering
        - **PUT**: for JSON rendering

    :param request: Web request
    :param group: group that will be involved in action
    :param attribute: Defined if request like *uri://groups/group/attribute*
    :param value: Defined if request like *uri://groups/group/attribute/value*
    :return: HTTP rendering
    """
    LOGGER.debug('registration.api.groups.group.dispatcher: %s uri:/%s',
                 request.method, request.path_info)
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
        response = group_delete.json(request, group=group, attribute=attribute, value=value)
    elif request.method == 'PUT':
        response = group_put.json(request, group=group, attribute=attribute, value=value)
    else:
        response = JsonResponse({
            'status': 'error',
            'message': 'MethodNotSupported'
        })
    return response
