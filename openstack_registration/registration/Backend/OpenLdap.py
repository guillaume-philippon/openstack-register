"""
OpenLdap backend support
"""
# -*- coding: utf-8 -*-
import re

import ldap
import ldap.sasl

from registration.Backend.Exceptions import AdminGroupDelete

from registration.utils import encode_password
from registration.exceptions import InvalidX500DN

from openstack_registration.config import GLOBAL_CONFIG

# Some regular expression to format ldap output
USER_LDAP_REGEXP = r"uid=(.*),{user_ou}".format(user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
GROUP_LDAP_REGEXP = r"cn=(.*),{group_ou}".format(group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])

GROUP_ATTRIBUTES = {
    'admins': 'owner',
    'members': 'uniqueMember',
    'description': 'description',
    'name': 'cn'
}


class OpenLdapBackend(object):  # pylint: disable=too-few-public-methods
    """
    Provide commun tools for OpenLDAP backend support.
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
            print 'error during openLdap connection'


class OpenLdapUserBackend(OpenLdapBackend):
    """
    Provide tools to manage user store on LDAP backend.
    """
    def get(self, username='*'):
        """
        Return a list of users based on filter

        :param username: username of user we want to get information
        :return: list or dict
        """
        response = list()
        users = self.connection.search_s(self.base_ou, ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                         "(&(objectClass=person)(uid={uid}))".format(uid=username),
                                         ['uid', 'mail', 'givenName', 'sn', 'cn', 'pager'])
        for _, attributes in users:
            response.append(self._ldap_to_dict(attributes))
        return response

    def create(self, attributes):
        """
        Create a ldap user with all their attributes

        :param attributes: User attributes in dict. format
        :return: void
        """
        user = "uid={username},{user_ou}".format(username=attributes['username'],
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        # We generate the "ldif-like" entry. ldap module need to have a specific format, entries
        # must be give as a list of tuple and value must always be a list.
        # We also need to for str for attributes as there are some strange unicode issue.
        # We also need to encode the password.
        # TODO: Make ajax request must give a encoded password, we should not have the plain one.
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
            self.connection.add_s(user, user_attributes)
        except ldap.INVALID_SYNTAX:  # pylint: disable=no-member
            raise InvalidX500DN('')
        except ldap.SERVER_DOWN:  # pylint: disable=no-member
            pass

    def modify(self, username, attributes):
        """
        Modify a user attributes

        :param username: username will modify
        :param attributes: attributes
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
        self.connection.modify_s(user, ldif)

    def delete(self, username):
        """
        Delete user account

        :param username: username
        :return: void
        """
        user = 'uid={username},{user_ou}'.format(username=username,
                                                 user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
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
    Provide tools to manage a group store on LDAP backend
    """
    def get(self, group='*', attribute=None):
        """
        Return a list of groups based on filter

        :param attribute: If a specific attribute is ask
        :param group: group filter, by default we get all groups
        :return: list of dict
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
        return response

    def create(self, attributes):
        """
        Create a group

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
        self.connection.add_s(group, group_attributes)

    def delete(self, group, attribute=None, value=None):
        """
        Delete group entry

        :param group: group name
        :param attribute: group name
        :param value: group name
        :return: void
        """
        # If delete is ask for a members or admis, then we just remove the dn of user to member list
        if attribute == 'members' or attribute == 'admins':
            self._ldap_remove_dn_to_list(group, attribute, value)
        else:
            # If groupname is LDAP_ADMIN_GROUP we refuse to remove it
            if group == GLOBAL_CONFIG['LDAP_ADMIN_GROUP']:
                raise AdminGroupDelete
            group_ldap = 'cn={group_name},{group_ou}' \
                         ''.format(group_name=group,
                                   group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
            self.connection.delete_s(group_ldap)

    def modify(self, group, attribute=None, value=None):
        """
        Modify value of a group.

        :param group: group name
        :param attribute: attribute name
        :param value: attribute value
        :return:
        """
        if attribute == 'members' or attribute == 'admins':
            self._ldap_add_dn_to_list(group, attribute, value)

    @staticmethod
    def _ldap_to_dict(attributes):
        """
        Format ldap output to be compliant with API.

        :param attributes: attributes to format
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
        Add a dn on a list of DN, useful to add a uniqueMember or a owner to a group

        :param cn:
        :param attribute:
        :param uid:
        :return:
        """
        uid_ldap = 'uid={uid},{user_ou}'.format(uid=uid,
                                                user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        cn_ldap = 'cn={cn},{group_ou}'.format(cn=cn,
                                              group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
        print "Add {} on {} in {}".format(uid_ldap, cn_ldap, GROUP_ATTRIBUTES[attribute])
        self.connection.modify_s(cn_ldap, [(ldap.MOD_ADD,  # pylint: disable=no-member
                                            GROUP_ATTRIBUTES[attribute], uid_ldap)])

    def _ldap_remove_dn_to_list(self, cn, attribute, uid):  # pylint: disable=invalid-name
        """
        Add a dn on a list of DN, useful to add a uniqueMember or a owner to a group

        :param cn:
        :param attribute:
        :param uid:
        :return:
        """
        uid_ldap = 'uid={uid},{user_ou}'.format(uid=uid,
                                                user_ou=GLOBAL_CONFIG['LDAP_USER_OU'])
        cn_ldap = 'cn={cn},{group_ou}'.format(cn=cn,
                                              group_ou=GLOBAL_CONFIG['LDAP_GROUP_OU'])
        print "Add {} on {} in {}".format(uid_ldap, cn_ldap, GROUP_ATTRIBUTES[attribute])
        self.connection.modify_s(cn_ldap, [(ldap.MOD_DELETE,  # pylint: disable=no-member
                                            GROUP_ATTRIBUTES[attribute], uid_ldap)])
