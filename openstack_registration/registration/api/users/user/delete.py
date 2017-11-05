"""
Provide support for uri://users/*username* call with **DELETE** HTTP method
"""
from django.http import JsonResponse
from django.contrib.auth import logout

from registration.decorators import owner_required
from registration.Backend.OpenLdap import OpenLdapUserBackend


@owner_required
def json(request, username):
    """
    Delete user account. We need to be a superuser or user it-self to do it.

    :param request: Web request
    :param username: username to delete
    :return: JSonResponse
    """
    ldap = OpenLdapUserBackend()
    ldap.delete(username)
    # If user the deletion came from user it-self, we logout it. Else, it s done by superuser
    # so we don't need to logout him.
    if request.user.get_username() == username:
        logout(request)
    return JsonResponse({
        'status': 'success'
    })
