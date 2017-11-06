"""
This module manage configuration file

    - /etc/register.cfg (for compatibility)
    - /etc/openstack-register/config.ini
    - $HOME/.register.ini
"""
import ConfigParser
import os

CONFIG_FILES = (
    '/etc/register.cfg',
    '/etc/openstack-register/config.ini',
    os.path.expanduser('~') + '/.register.cfg'
)
"""
All the file that will be parse to generate the openstack-registration configuration. The last
file listed have the highest priority
"""

GLOBAL_CONFIG = {
    # [auth]
    'LDAP_SERVER': 'ldap://127.0.0.1',
    'LDAP_BASE_OU': 'ou=users,o=cloud',
    'LDAP_GROUP_OU': 'ou=groups,o=cloud',

    # [django]
    'DJANGO_SECRET_KEY': 'This should be change',  # Should be declare to allow doc generation

    # [main]
    'DEBUG_LVL': '1',
    'LOG_DIR': '/var/log/openstack-registration/',
    'REGISTRATION_URL': 'http://127.0.0.1',

    # [mailing]
    'MAIL_FROM': 'no-reply@example.com'
}
"""
**GLOBAL_CONFIG** is used to share configuration between all django-apps / modules.
"""

AUTH_OPTIONS = {
    'LDAP_SERVER': 'server',
    'LDAP_USER': 'bind_dn',
    'LDAP_PASSWORD': 'password',
    'LDAP_BASE_OU': 'user_search',
    'LDAP_GROUP_OU': 'group_search'
}
"""
    - **LDAP_SERVER**: hostname of ldap server (file option: *server*)
    - **LDAP_USER**: DN of ldap user (file option: *bind_dn*)
    - **LDAP_PASSWORD**: password of ldap user (file option: *password*)
    - **LDAP_BASE_OU**: The base search for user in ldap
    - **LDAP_GROUP_OU**: The base search for group in ldap

"""

MAIN_OPTIONS = {
    'DEBUG_LVL': 'debug_lvl',
    'LOG_DIR': 'logdir',
    'REGISTRATION_URL': 'register_url',
    'ADMIN_UID': 'admin'
}
"""

    - **DEBUG_LVL**: debug level (file option: *debug_lvl*)
    - **LOG_DIR**: log directory where log file will be put (file option: *logdir*)
    - **REGISTRATION_URL**: URL of registration server (file option: *register_url*)

"""

MAILING_OPTIONS = {
    'MAIL_ADMIN': 'admin',
    'MAIL_FROM': 'from',
    'MAIL_SERVER': 'server'
}
"""

    - **MAIL_ADMIN**: mail of administrators (file options: *admin*)
    - **MAIL_FROM**: mail From field when mail will be sent (file options: *from*)
    - **MAIL_SERVER**: smtp server (file option: *server*)

"""

DJANGO_OPTIONS = {
    'DJANGO_SECRET_KEY': 'secret_key'
}
"""

    - **DJANGO_SECRET_KEY**: Secret key that will be used by django (file option: *secret_key*)

"""

SECTIONS = {
    'auth': AUTH_OPTIONS,
    'main': MAIN_OPTIONS,
    'mailing': MAILING_OPTIONS
}
"""
**SECTION** provide the list of options (per section) that will be parsed to load the configuration.

    - **auth**: options for section [auth]
    - **main**: options for section [main]
    - **mailing**: options for section [mailing]

"""


def load_config_option(config, section):
    """
    Overwrite the current GLOBAL_CONFIG w/ new values

    :param config: Configuration file we read
    :param section: The section of config. we compute
    :return: void
    """
    options = SECTIONS[section]
    for option in options:
        try:
            GLOBAL_CONFIG[option] = config.get(section,
                                               options[option])
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass


def load_config():
    """
    Load configuration

    :return: void
    """
    config = ConfigParser.RawConfigParser()

    for config_file in CONFIG_FILES:
        config.read(config_file)
        for section in SECTIONS:
            load_config_option(config, section)
