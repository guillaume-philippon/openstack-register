"""
Provide support for **DELETE** methods on uri://users/username request.
"""
from django.http import JsonResponse
from django.contrib.auth import logout

from registration.decorators import owner_required
from registration.Backend.OpenLdap import OpenLdapUserBackend


@owner_required
def json(request, username):
    """
    JSON rendering for uri://users/*username* request. It need:

    - superuser account: as superuser always have access to view
    - owner account: allow user to delete its account

    :param request: Web request
    :param username: user to delete
    :return: HTTP rendering
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
