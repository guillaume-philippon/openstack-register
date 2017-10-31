# pylint: skip-file
# -*- coding: utf-8 -*-

"""
Methods apply if not exist in specific backends class
"""


class PrototypeBackend(object):  # pylint: disable=too-few-public-methods
    """
    PrototypeBackend is a abstraction of Backend.
    """
    def __init__(self):
        """
        Default init class
        """
        pass

    def add_user(self,  # pylint: disable=too-many-arguments
                 username,
                 email,
                 firstname,
                 lastname,
                 x500dn,
                 password):
        """
        Create a new user
        :param username: username
        :param email: email for the new user
        :param firstname: user first name
        :param lastname: user last name
        :param x500dn: Certificate DN
        :param password: user password
        :return: void
        """
        pass
