"""
Provide support for all *POST* method to uri://users/*username*. *POST* method will allow
user creation. You will raise AlreadyExist exception if user exist.
"""
from django.http import JsonResponse
from django.contrib import auth

from registration.Backend.OpenLdap import OpenLdap


def json(request, username):  # pylint: disable=unused-argument
    """
    Create a user based on request content and username uri

    :param request: Web request
    :param username: username
    :return: Json rendering
    """
    ldap = OpenLdap()
    attributes = {
        'username': username,
        'lastname': request.POST['lastname'],
        'firstname': request.POST['firstname'],
        'password': request.POST['password'],
        'email': request.POST['email']
    }
    ldap.create_user(attributes)

    # After creating the user, we automaticaly logged him
    user = auth.authenticate(username=username,
                             password=request.POST['password'])
    # If user is not None, then user is authenticated
    if user is not None:
        auth.login(request, user)
        response = JsonResponse({
            'status': 'success'
        })
    # else the username or password is invalid. It should not happen
    else:
        response = JsonResponse({
            'status': 'failure',
            'message': 'invalid username or password'
        })

    return response
