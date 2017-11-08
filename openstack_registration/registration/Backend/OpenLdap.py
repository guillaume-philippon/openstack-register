"""
Provide support for openldap backend. It abstract all openldap interaction with pyldap module.
"""
# -*- coding: utf-8 -*-
import re

import ldap
import ldap.sasl

from openstack_registration.config import GLOBAL_CONFIG
from openstack_registration.settings import LOGGER

from registration.Backend.Exceptions import AdminGroupDelete, NotValidPassword, NotValidEmail
from registration.utils import encode_password
from registration.exceptions import InvalidX500DN

# Some regular expression to format ldap output
USER_LDAP_REGEXP = r"uid=(.*),{user_ou}".format(user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
GROUP_LDAP_REGEXP = r"cn=(.*),{group_ou}".format(group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
EMAIL_REGEXP = r"([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+"
PASSWORD_REGEXP = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,}"

GROUP_ATTRIBUTES = {
    'admins': 'owner',
    'members': 'uniqueMember',
    'description': 'description',
    'name': 'cn'
}


class OpenLdapBackend(object):  # pylint: disable=too-few-public-methods
    """
    Base class for openldap interaction. It only provide __init__ method that will be inherent by
    sub-classes.
    """
    def __init__(self):
        """
        initialize Backend
        """
        super(OpenLdapBackend, self).__init__()
        self.server = GLOBAL_CONFIG['LDAP_SERVER']
        self.user = GLOBAL_CONFIG['LDAP_USER']
        self.password = GLOBAL_CONFIG['LDAP_PASSWORD']
        self.base_ou = GLOBAL_CONFIG['LDAP_USER_OU']
        self.group_ou = GLOBAL_CONFIG['LDAP_GROUP_OU']
        self.connection = ldap.initialize(self.server)

        try:
            self.connection.simple_bind_s(self.user, self.password)
        except:  # pylint: disable=bare-except
            LOGGER.warning('OpenLdapBackend: Error during openldap connection')


class OpenLdapUserBackend(OpenLdapBackend):
    """
    OpenLdapBackend sub-class to manage user openldap storage.
    """
    def get(self, username='*'):
        """
        Get user information based on *username* filter. By default, the filter is '*' and get()
        will return all user informations. It user _ldap_to_dict() private method to format output.

        As pyldap considere all entry as a list even if they can have only one entry, we reformat
        it to make it easier to manipulate.

        :param username: filter that will be used. By default, value is '*' and user can change it
                         for a specific username.
        :return: list of user
        """
        response = list()
        users = self.connection.search_s(self.base_ou, ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                         "(&(objectClass=person)(uid={uid}))".format(uid=username),
                                         ['uid', 'mail', 'givenName', 'sn', 'cn', 'pager'])
        for _, attributes in users:
            response.append(self._ldap_to_dict(attributes))
        LOGGER.debug('Get user information: %s', response)
        return response

    def create(self, attributes):
        """
        Create user based on attributes.

        :param attributes: user attributes (username / email / firstname / lastname / password)
        :return: void
        """
        user = "uid={username},{user_ou}".format(username=attributes['username'],
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        # Before adding a user, we check if password is strong enough and if email
        # have a valid format.
        if not re.match(PASSWORD_REGEXP, attributes['password']):
            LOGGER.debug('Password %s not match REGEXP %s', attributes['password'], PASSWORD_REGEXP)
            raise NotValidEmail
        if not re.match(EMAIL_REGEXP, attributes['email']):
            LOGGER.debug('Email %s not match REGEXP %s', attributes['email'], EMAIL_REGEXP)
            raise NotValidEmail
        # We generate the "ldif-like" entry. ldap module need to have a specific format, entries
        # must be give as a list of tuple and value must always be a list.
        # We also need to for str for attributes as there are some strange unicode issue.
        # We also need to encode the password.
        user_attributes = [
            ('objectClass', ['organizationalPerson', 'person', 'inetOrgPerson', 'top']),
            ('uid', [str(attributes['username'])]),
            ('mail', [str(attributes['email'])]),
            ('givenName', [str(attributes['firstname'])]),
            ('sn', [str(attributes['lastname'])]),
            ('cn', [str("{} {}".format(attributes['firstname'],
                                       attributes['lastname']))]),
            ('userPassword', [str(encode_password(unicode(attributes['password'])
                                                  .encode(encoding='utf-8')))]),
            ('pager', ['514'])
        ]
        try:
            LOGGER.info('User %s is created with attributes %s', user, attributes)
            self.connection.add_s(user, user_attributes)
        except ldap.INVALID_SYNTAX:  # pylint: disable=no-member
            raise InvalidX500DN('')

    def modify(self, username, attributes):
        """
        Modify user defined by *username*. It will parse all attribute listed in attributes and
        modify it with the value provieded. If password attribute is empty, then, we let the
        current password value as it is.

        :param username: user that will be modified
        :param attributes: attributes of the user
        :return: void
        """
        user = 'uid={username},{user_ou}'.format(username=username,
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        ldif = list()
        for attribute in attributes:
            if attribute == 'email':
                ldif.append((ldap.MOD_REPLACE, 'mail', str(attributes[attribute])))  # pylint: disable=no-member
            elif attribute == 'firstname':
                ldif.append((ldap.MOD_REPLACE, 'givenName', str(attributes[attribute])))  # pylint: disable=no-member
            elif attribute == 'lastname':
                ldif.append((ldap.MOD_REPLACE, 'sn', str(attributes[attribute])))  # pylint: disable=no-member
            elif attribute == 'password':
                if attributes[attribute] != "":
                    password = str(encode_password(unicode(attributes[attribute])
                                                   .encode(encoding='utf-8')))
                    ldif.append((ldap.MOD_REPLACE, 'userPassword', password))  # pylint: disable=no-member
        LOGGER.info('User %s is modify with attributes %s', user, attributes)
        self.connection.modify_s(user, ldif)

    def delete(self, username):
        """
        Delete the user account defined by *username*.

        :param username: user that will be deleted
        :return: void
        """
        user = 'uid={username},{user_ou}'.format(username=username,
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        LOGGER.info('User %s is deleted', user)
        self.connection.delete_s(user)

    @staticmethod
    def _ldap_to_dict(attributes):
        """
        return a list of users based on ldap output. By default ldap module return a list of value
        even there is only one value for the attributes. To make it simple for other
        openstack-registration module to interact with ldap, we format the output to be a dict of
        value

        :param attributes: ldap attributes to format
        :return: dict
        """
        response = {
            'uid': attributes['uid'][0],
            'mail': attributes['mail'][0],
            'firstname': attributes['givenName'][0],
            'lastname': attributes['sn'][0],
            'fullname': attributes['cn'][0]
        }
        # pager is a optional value, so we catch KeyError exception if we have it
        try:
            response['pager'] = attributes['pager'][0]
        except KeyError:
            pass
        return response


class OpenLdapGroupBackend(OpenLdapBackend):
    """
    OpenLdapBackend sub-class to manage group openldap storage.
    """
    def get(self, group='*', attribute=None):
        """
        Get group information based on group filter. By default, group filter is '*' to get all
        groups. If attribute is not None, then we only get *attribute* value of the group.

        It use _ldap_to_dict private method to format output to a easier manipulation.

        :param group: filter, by default '*'.
        :param attribute: target attribute that will be listed
        :return: list
        """
        response = list()
        if attribute is None:
            output = ['cn', 'description']
        else:
            output = [GROUP_ATTRIBUTES[attribute]]
        groups = self.connection.search_s(self.group_ou, ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                          "(&(objectClass=groupOfUniqueNames)"
                                          "(cn={cn}))".format(cn=group),
                                          output)
        for _, attributes in groups:
            response.append(self._ldap_to_dict(attributes))
        LOGGER.debug('Group %s information: %s', group, response)
        return response

    def create(self, attributes):
        """
        Create a group based on attributes value.

        :param attributes: group attributes
        :return: void
        """
        user = "uid={username},{user_ou}".format(username=attributes['username'],
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        group = "cn={name},{group_ou}".format(name=attributes['name'],
                                              group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
        group_attributes = [
            ('objectClass', ['groupOfUniqueNames', 'top']),
            ('cn', str(attributes['name'])),
            ('uniqueMember', user),
            ('owner', user),
            ('description', str(attributes['description']))
        ]
        LOGGER.info('Group %s created with attributes %s', group, attributes)
        self.connection.add_s(group, group_attributes)

    def delete(self, group, attribute=None, value=None):
        """
        Delete a group or a group entry. If attribute is None, then the group will be deleted,
        else, we remove *value* from *attribute*.

        It use _ldap_remove_dn_to_list private method to remove entry.

        :param group: name of the group that will be affected
        :param attribute: attribute that can be affected if defined
        :param value: value that will be removed if defined
        :return: void
        """
        # If delete is ask for a members or admis, then we just remove the dn of user to member list
        if attribute == 'members' or attribute == 'admins':
            LOGGER.info('Group %s delete %s/%s', group, attribute, value)
            self._ldap_remove_dn_to_list(group, attribute, value)
        else:
            # If groupname is LDAP_ADMIN_GROUP we refuse to remove it
            if group == GLOBAL_CONFIG['LDAP_ADMIN_GROUP']:
                raise AdminGroupDelete
            group_ldap = 'cn={group_name},{group_ou}' \
                         ''.format(group_name=group,
                                   group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
            LOGGER.info('Group %s deleted', group)
            self.connection.delete_s(group_ldap)

    def modify(self, group, attribute=None, value=None):
        """
        Modify value of a group or a attribute in a group. Currently, only add *value* in
        *attribute*.

        It use _ldap_add_dn_to_list private method to add a *value* in *attribute*.

        :param group: name of the group that will be affected.
        :param attribute: that will be affected if defined
        :param value: value that will be added if defined
        :return:
        """
        if attribute == 'members' or attribute == 'admins':
            LOGGER.info('Group %s add %s/%s', group, attribute, value)
            self._ldap_add_dn_to_list(group, attribute, value)

    @staticmethod
    def _ldap_to_dict(attributes):
        """
        return a list of users based on ldap output. By default ldap module return a list of value
        even there is only one value for the attributes. To make it simple for other
        openstack-registration module to interact with ldap, we format the output to be a dict of
        value

        :param attributes: ldap attributes to format
        :return: list
        """
        response = dict()
        if 'cn' in attributes:
            response['name'] = attributes['cn'][0]
        if 'description' in attributes:
            response['description'] = attributes['description'][0]
        if 'uniqueMember' in attributes:
            members = list()
            for member in attributes['uniqueMember']:
                members.append(re.sub(USER_LDAP_REGEXP, r'\1', member))
            response['members'] = members
        if 'owner' in attributes:
            admins = list()
            for admin in attributes['owner']:
                admins.append(re.sub(USER_LDAP_REGEXP, r'\1', admin))
            response['admins'] = admins
        return response

    def _ldap_add_dn_to_list(self, cn, attribute, uid):  # pylint: disable=invalid-name
        """
        Add a entry in a openldap group based on attribute.

        :param cn: commun name of the group
        :param attribute: attribute name
        :param uid: uid that will be added to group
        :return: void
        """
        uid_ldap = 'uid={uid},{user_ou}'.format(uid=uid,
                                                user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        cn_ldap = 'cn={cn},{group_ou}'.format(cn=cn,
                                              group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
        self.connection.modify_s(cn_ldap, [(ldap.MOD_ADD,  # pylint: disable=no-member
                                            GROUP_ATTRIBUTES[attribute], uid_ldap)])

    def _ldap_remove_dn_to_list(self, cn, attribute, uid):  # pylint: disable=invalid-name
        """
        Remove a entry in openldap group based on attribute.

        :param cn: commun name of the group
        :param attribute: attribute name
        :param uid: uid that will be added to group
        :return: void
        """
        uid_ldap = 'uid={uid},{user_ou}'.format(uid=uid,
                                                user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        cn_ldap = 'cn={cn},{group_ou}'.format(cn=cn,
                                              group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
        print "Add {} on {} in {}".format(uid_ldap, cn_ldap, GROUP_ATTRIBUTES[attribute])
        self.connection.modify_s(cn_ldap, [(ldap.MOD_DELETE,  # pylint: disable=no-member
                                            GROUP_ATTRIBUTES[attribute], uid_ldap)])
