"""
This module provide some usefull decorator for openstack-register
"""
from functools import wraps
from django.core.exceptions import PermissionDenied


def owner_required(view):
    """
    If the request need user it-self or administrator access to be done , we user @owner_required()
    decorator

    :param view: As parameter, we have the view function
    :return: function
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        """
        Wrapper for view function. It check if user is the user it-self or a administrator. If not,
        raise PermissionDenied exception.

        :param request: Web request
        :param args: package view function arguments as a list
        :param kwargs: page view function arguments as a dict
        :return: function
        """
        user = request.user.get_username()
        if user == kwargs['username']\
                or request.user.is_superuser:
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap
