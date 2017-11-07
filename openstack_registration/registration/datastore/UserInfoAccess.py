"""
This module manage interaction between openstack-registration function and models. It provide a
abstraction of UserInfo model to be easiest to use.

**This module is obsolete as all information is now in openldap backend**
"""
from registration.models import UserInfo
from openstack_registration.config import GLOBAL_CONFIG


class UserInfoAccess(object):  # pylint: disable=too-few-public-methods
    """
    User info access is a abstraction class of UserInfo model
    """
    def __init__(self):
        """
        Initialisation of UserInfoAccess class. Mainly do nothing
        """
        pass

    @staticmethod
    def is_admin(username):
        """
        Return True if user is a LDAP administrator, there are two ways to be administrator:

            - put *admin* option on config.ini file
            - have *admin* flag on UserInfo django model

        :param username: username of the user we want to check
        :return: Boolean
        """
        response = False
        user = UserInfo.objects.filter(username=username)  # pylint: disable=no-member
        if user:
            response = user[0].admin
        elif username == GLOBAL_CONFIG['ADMIN_UID']:
            response = True
        return response
