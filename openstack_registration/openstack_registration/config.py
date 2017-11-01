"""
This module manage configuration file
* /etc/register.cfg (for compatibility)
* /etc/openstack-register/config.ini
* $HOME/.register.ini
"""
import ConfigParser
import os

# List of possible configuration file, last item has highest priority
CONFIG_FILES = (
    '/etc/register.cfg',
    '/etc/openstack-register/config.ini',
    os.path.expanduser('~') + '/.register.cfg'
)

# Default value for GLOBAL_CONFIG
GLOBAL_CONFIG = {
    # [auth]
    'LDAP_SERVER': 'ldap://127.0.0.1',
    'LDAP_BASE_OU': 'ou=users,o=cloud',

    # [main]
    'DEBUG_LVL': '1',
    'LOG_DIR': '/var/log/openstack-registration/',
    'REGISTRATION_URL': 'http://127.0.0.1',

    # [mailing]
    'MAIL_FROM': 'no-reply@example.com'
}

# Options for [auth] section
AUTH_OPTIONS = {
    'LDAP_SERVER': 'server',
    'LDAP_USER': 'bind_dn',
    'LDAP_PASSWORD': 'password',
    'LDAP_BASE_OU': 'user_search'
}

# Options for [main] section
MAIN_OPTIONS = {
    'DEBUG_LVL': 'debug_lvl',
    'LOG_DIR': 'logdir',
    'REGISTRATION_URL': 'register_url'
}

# Options for [mailing]section
MAILING_OPTIONS = {
    'admin': 'admin',
    'MAIL_FROM': 'from',
    'MAIL_SERVER': 'server'
}

# List all sections and options associated
SECTIONS = {
    'auth': AUTH_OPTIONS,
    'main': MAIN_OPTIONS,
    'mailing': MAILING_OPTIONS
}


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
