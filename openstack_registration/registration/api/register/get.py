"""
Provide support to all **GET** method called on uri://register
"""
from django.shortcuts import render
from django.http import JsonResponse, QueryDict

from registration.utils import encode_password
from registration.Backend import OpenLdap
from registration.exceptions import InvalidX500DN

from openstack_registration.config import GLOBAL_CONFIG


def html(request):
    """
    Return a HTTP response for register

    :param request: Web request
    :return: HTTP
    """
    return render(request, 'register/get.html')


def json(request):
    """
    Return a Json Response for register

    :param request: Web request
    :return: JSonResponse
    """
    attributes = dict()
    if 'adduser' in request.GET:
        attributes = QueryDict(request.body).dict()
        add_user(request, attributes)
    elif 'cert' in request.GET:
        if 'SSL_CLIENT_S_DN' in request.META:
            attributes['DN'] = request.META['SSL_CLIENT_S_DN']
    return JsonResponse(attributes)


# TODO: To remove
def add_user(request, attributes):  # pylint: disable=unused-argument
    """
    make desc.
    :param request: Web request
    :param attributes: attributes
    :return: void
    """
    GLOBAL_CONFIG['project'] = ''
    ldap = OpenLdap()
    username = str(attributes['username'])
    email = str(attributes['email'])
    firstname = str(attributes['firstname'])
    lastname = str(attributes['lastname'])
    x500dn = str(attributes['x500dn'])
    GLOBAL_CONFIG['project'] = str(attributes['project'])
    password = encode_password(unicode(attributes['password']).encode(encoding='utf-8'))

    try:
        ldap.add_user(username, email, firstname, lastname, x500dn, password)
        # LOGGER.info("USER CREATED   :: Operator : %s  :: Attributes : username=%s, firstname=%s,"
        #             " lastname=%s, email=%s ", request.user, username, firstname, lastname, email)
    except InvalidX500DN:
        exit(1)
