"""
Provide exceptions for registration.Backend module.
"""


class AdminGroupDelete(Exception):
    """
    Raised when a user try to delete the administrator group.
    """
    pass


class NotGroupAttribute(Exception):
    """
    Raised when a user try to access to a attribute that not exist
    """
    pass


class NotValidPassword(Exception):
    """
    Raised when a password is too weak
    """
    pass


class NotValidEmail(Exception):
    """
    Raised when a password is too weak
    """
    pass
