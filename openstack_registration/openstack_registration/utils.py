"""
This module is used to provide some usefull function to openstack_registration project
"""
import logging
from logging.handlers import RotatingFileHandler

from openstack_registration.config import GLOBAL_CONFIG


def create_logger(mode,
                  stream_level=logging.INFO,  # pylint: disable=unused-argument
                  file_level=logging.DEBUG):
    """
    Create a logger according to the given level
    :param mode:
    :param stream_level:
    :param file_level:
    :return:
    """
    logger = logging.getLogger("registration")
    logger.setLevel(logging.DEBUG)

    # Use rsyslog to send logs to others
    # handler = logging.handlers.SysLogHandler(address="/dev/log")
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s'
    )

    if mode == 'both':
        # Fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        file_handler = RotatingFileHandler(GLOBAL_CONFIG['LOG_DIR'] + '/registration.log',
                                           'a',
                                           1000000,
                                           1)

        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def create_logger_error(mode,
                        stream_level=logging.INFO,  # pylint: disable=unused-argument
                        file_level=logging.DEBUG):
    """
    Create a logger according to the given level
    :param mode:
    :param stream_level:
    :param file_level:
    :return:
    """
    logger_error = logging.getLogger("registration_error")
    logger_error.setLevel(logging.DEBUG)

    # Use rsyslog to send logs to others
    # handler = logging.handlers.SysLogHandler(address="/dev/log")
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(funcName)s %(lineno)d :: %(message)s'
    )

    if mode == 'both':
        # Fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        file_handler = RotatingFileHandler(GLOBAL_CONFIG['LOG_DIR'] + '/registration.log',
                                           'a',
                                           1000000,
                                           1)

        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger_error.addHandler(file_handler)

    return logger_error
