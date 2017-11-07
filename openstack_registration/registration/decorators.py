"""
Provide a list of decorators that can be use to grant access to some view.
"""
from functools import wraps
from django.core.exceptions import PermissionDenied

from registration.Backend.OpenLdap import OpenLdapGroupBackend

from openstack_registration.config import GLOBAL_CONFIG


def owner_required(view):
    """
    If the request need user it-self or administrator access to be done , we use @owner_required
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
        if ('username' in kwargs and user == kwargs['username']) \
                or request.user.is_superuser \
                or user == GLOBAL_CONFIG['ADMIN_UID']:
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def superuser_required(view):
    """
    If the request require superuser access, we use @superuser_required decorator

    :param view: The view that will be decorator
    :return: function
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        """
        Wrapper function

        :param request: Web request
        :param args: package view function arguments as a list
        :param kwargs: package view function arguments as a dict
        :return: function
        """
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def groupadmin_required(view):
    """
    If the request require group access, we use @superuser_required decorator

    :param view: The view that will be decorator
    :return: function
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        """
        Wrapper function

        :param request: Web request
        :param args: package view function arguments as a list
        :param kwargs: package view function arguments as a dict
        :return: function
        """
        # if we are a superuser, no question, you have access
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        else:  # else, we ask OpenLdapGroupBackend to see if you are a group admin
            ldap = OpenLdapGroupBackend()
            if 'group' in kwargs:
                group = kwargs['group']
            else:
                group = '*'
            groups = ldap.get(group, attribute='admins')
            # If group is specify, then we let only group admins to access to data
            if groups and group is not None and request.user.get_username() in groups[0]['admins']:
                return view(request, *args, **kwargs)
            else:  # else, we let any group admin to access to data
                for group_index in groups:
                    if request.user.get_username() in group_index['admins']:
                        return view(request, *args, **kwargs)
        # at the end, if nothing match, we raise a PermissionDenied
        raise PermissionDenied
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def superuser_protection(view):
    """
    Make sure we don't try to access a view that can modify superuser

    :param view: The view that will be decorate
    :return: function
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        """
        Wrapper funcion

        :param request: Web request
        :param args: package view function arguments as a list
        :param kwargs: package view function arguments as a dict
        :return: function
        """
        if ('attribute' in kwargs or kwargs['attribute'] is None) \
                and not request.user.is_superuser:
            print "exception"
            raise PermissionDenied
        return view(request, *args, **kwargs)
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def self_protection(view):
    """
    Make sure we don't try to access to delete it-self

    :param view: The view that will be decorate
    :return: function
    """
    @wraps(view)
    def wrap(request, *args, **kwargs):
        """
        Wrapper funcion

        :param request: Web request
        :param args: package view function arguments as a list
        :param kwargs: package view function arguments as a dict
        :return: function
        """
        if 'value' in kwargs and kwargs['value'] == request.user.get_username():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap
