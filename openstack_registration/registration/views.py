"""
View module manage interface between user and openstack-registration. It provide a HTTP API based
on REST good practice.
"""
# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth

LOGGER = logging.getLogger("registration")
LOGGER_ERROR = logging.getLogger("registration_error")


def login(request):
    """
    login view is used to log user on openstack-registration. It return a JSonResponse output with
    the status of login

        - **success**: user is logged
        - **failure**: user is not logged

    :param request: Web request
    :return: HTTP rendering
    """
    # If user is already authenticated, we return a success status
    if request.user.is_authenticated():
        response = JsonResponse({
            'status': 'success'
        })
    # We use post method to authenticate user. we trap it to compute it.
    elif request.method == "POST":
        user = auth.authenticate(username=request.POST['username'].lower(),
                                 password=request.POST['password'])
        # If user is not None, then user is authenticated
        if user is not None:
            auth.login(request, user)
            LOGGER.info("USER LOGIN     :: User %s is connected from %s",
                        request.user, request.META.get('REMOTE_ADDR'))
            response = JsonResponse({
                'status': 'success'
            })
        # else the username or password is invalid
        else:
            LOGGER.info("LOGIN FAILED   :: Attempt to login with user '%s' from %s",
                        request.POST['username'], request.META.get('REMOTE_ADDR'))
            response = JsonResponse({
                'status': 'failure',
                'message': 'invalid username or password'
            })
    # If it s not a POST method, it s not supported by the view
    else:
        response = JsonResponse({
            'status': 'failure',
            'message': 'method {method} is not supported on login'
                       ' page'.format(method=request.method)
        })
    return response


@login_required()
def logout(request):
    """
    logout user from application.

    :param request: HTTP request
    :return: HTTP rendergin
    """
    LOGGER.info("USER LOGOUT    :: User %s is disconnected from %s ",
                request.user, request.META.get('REMOTE_ADDR'))
    auth.logout(request)
    return redirect('/')


def home(request):
    """
    Default home page for openstack-registration. If user is already logged, we redirect him to
    it's own interface.

    :param request: Web request
    :return: HTTP rendering
    """
    if request.user.is_authenticated():
        response = HttpResponseRedirect('/users/{}'.format(request.user.get_username()))
    else:
        response = render(request, 'home.html')
    return response


def policies(request):
    """
    Display policies web pages, only available throught html format.

    :param request: Web request
    :return: HTTP rendering
    """
    return render(request, 'policies.html')


def handler403(request):
    """
    Handle 403 error message

    :param request: Web request
    :return: HTTP rendering
    """
    print 'test'
    response = render(request, 'error/handler403.html', status=403)
    return response


def handler500(request):
    """
    Handle 500 error message

    :param request: Web request
    :return: HTTP rendering
    """
    response = render(request, 'error/handler500.html', status=500)
    return response
