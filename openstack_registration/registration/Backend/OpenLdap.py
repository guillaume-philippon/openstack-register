"""
OpenLdap backend support
"""
# -*- coding: utf-8 -*-

import ldap
import ldap.sasl

from registration.utils import encode_password
from registration.exceptions import InvalidX500DN
from registration.models import UserActivation

from openstack_registration.config import GLOBAL_CONFIG

ATTRIBUTE_BINDING = {
    'email': 'mail',
    'firstname': 'givenName',
    'lastname': 'sn',
    'password': 'userPassword'
}

# TODO: Should be named OpenLdapBackend to avoid miss-lead
class OpenLdap(object):
    """
    OpenLdap Backend support is based on PrototypeBackend
    """
    def __init__(self):
        """
        initialize Backend
        """
        super(OpenLdap, self).__init__()
        self.server = GLOBAL_CONFIG['LDAP_SERVER']
        self.user = GLOBAL_CONFIG['LDAP_USER']
        self.password = GLOBAL_CONFIG['LDAP_PASSWORD']
        self.base_ou = GLOBAL_CONFIG['LDAP_BASE_OU']
        self.connection = ldap.initialize(self.server)

        try:
            self.connection.simple_bind_s(self.user, self.password)
        except:  # pylint: disable=bare-except
            print 'error during openLdap connection'

    def delete_user_from_group(self, user, group):
        """
        Delete user from group
        :param user: user that should be removed
        :param group: group from where the user is removed
        :return:
        """
        dn_user = user.encode('utf-8')
        dn_group = group.encode('utf-8')
        # TODO: WTF !!!
        ok = False  # pylint: disable=invalid-name
        try:
            self.connection.modify_s(dn_group,
                                     [(ldap.MOD_DELETE,  # pylint: disable=no-member
                                       'uniqueMember', dn_user)])
            ok = True  # pylint: disable=invalid-name
        except:  # pylint: disable=bare-except
            print "Error while removing user " + dn_user + " from group " + dn_group
        return ok

    def add_user_from_group(self, user, group):
        """
        Add user to a group
        :param user:
        :param group:
        :return:
        """
        dn_user = user.encode('utf-8')
        dn_group = group.encode('utf-8')
        ok = False  # pylint: disable=invalid-name
        try:
            self.connection.modify_s(dn_group,
                                     [(ldap.MOD_ADD,  # pylint: disable=no-member
                                       'uniqueMember', dn_user)])
            ok = True  # pylint: disable=invalid-name
        except ldap.TYPE_OR_VALUE_EXISTS:  # pylint: disable=no-member
            return False
        except:  # pylint: disable=bare-except
            print "Error while adding user " + dn_user + " from group " + dn_group
        return ok

    # TODO: addGroup should be renamed
    def addGroup(self, group, desc, user): # pylint: disable=invalid-name
        """
        Create a new group
        :param group: group named
        :param desc: description of the group
        :param user: first user of the group
        :return: void
        """
        attributes = []
        # TODO: Base ou for group should be put on configuration file
        dn_group = "cn={},ou=groups,o=cloud".format(str(group))
        attrs = {
            'objectClass': ['groupOfUniqueNames', 'top'],
            'cn': "{}".format(str(group)),
            'uniqueMember': "uid={},ou=users,o=cloud".format(str(user)),
        }
        if desc != "":
            attrs['description'] = str(desc)
        for value in attrs:
            entry = (value, attrs[value])
            attributes.append(entry)
        self.connection.add_s(dn_group, attributes)

    def search_user(self, uid=None, mail=None, attributes=None, password=None, pager=None):  # pylint: disable=too-many-arguments
        """
        Search a user based on some filter
        :param uid: uid of the user
        :param mail: email of the user
        :param attributes: attributes of the user
        :param password: password of the user
        :param pager: status of the user
        :return:
        """
        if uid is not None and mail is not None and pager is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(uid=*))",
                                            ['uid', 'mail', 'pager'])
        if uid is not None and mail is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(uid=*))",
                                            ['uid', 'mail'])
        elif uid is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(uid={}))"
                                            .format(uid),
                                            ['uid'])
        elif mail is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(mail={}))"
                                            .format(mail),
                                            ['mail'])
        elif attributes is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(uid={}))"
                                            .format(attributes),
                                            ['uid', 'mail', 'givenName', 'sn', 'cn'])
        elif password is not None:
            return self.connection.search_s(self.base_ou,
                                            ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                            "(&(objectClass=person)(uid={}))"
                                            .format(password),
                                            ['userPassword'])

    def search_groups(self):
        """
        List all groups
        :return: list
        """
        return self.connection.search_s('ou=groups,o=cloud',
                                        ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                        "(&(objectClass=groupOfUniqueNames)(cn=*))",
                                        ['cn'])

    def search_group(self, uid):
        """
        Search a specific group
        :param uid:
        :return:
        """
        return self.connection.search_s('ou=groups,o=cloud',
                                        ldap.SCOPE_SUBTREE,  # pylint: disable=no-member
                                        "(&(objectClass=groupOfUniqueNames)(cn={}))"
                                        .format(uid),
                                        ['uniqueMember', 'cn', 'description'])

    def modify_user(self, uid, action):
        """
        Modify user entry
        :param uid: uid
        :param action: action that should be done
        :return: void
        """
        attrs = {}
        if action == 'enable':
            pager = "512"
        else:
            pager = "514"
        user_attributes = self.search_user(attributes=uid)
        dn_user = str(user_attributes[0][0])

        update_attrs = [(ldap.MOD_REPLACE, 'pager', pager)]  # pylint: disable=no-member
        try:
            self.connection.modify_s(dn_user, update_attrs)
            attrs['status'] = 'success'
        except:  # pylint: disable=bare-except
            attrs['status'] = 'fail'
        return attrs

    def enable_user(self, uuid):
        """
        Enable user
        :param uuid: uuid of the user
        :return: void
        """
        attrs = {}
        user = UserActivation.objects.filter(link=uuid)  # pylint: disable=no-member

        if user:
            username = user[0].username
            user_attributes = self.search_user(attributes=username)
            dn_user = str(user_attributes[0][0])
            email = str(user_attributes[0][1]['mail'][0])
            firstname = str(user_attributes[0][1]['givenName'][0])
            lastname = str(user_attributes[0][1]['sn'][0])
            update_attrs = [(ldap.MOD_REPLACE, 'pager', '512')]  # pylint: disable=no-member
            attrs['mail'] = email
            attrs['username'] = username
            attrs['firstname'] = firstname
            attrs['lastname'] = lastname

            self.connection.modify_s(dn_user, update_attrs)
            user.delete()
        return attrs

    def change_user_password(self, user, password):
        """
        Change user password
        :param user: user
        :param password: new password
        :return: void
        """
        attrs = {}
        user_attributes = self.search_user(attributes=user)
        dn_user = str(user_attributes[0][0])
        update_attrs = [(ldap.MOD_REPLACE, 'userPassword', password)]  # pylint: disable=no-member
        try:
            self.connection.modify_s(dn_user, update_attrs)
            attrs['status'] = 'success'
        except:  # pylint: disable=bare-except
            attrs['status'] = 'fail'
        return attrs


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
        self.base_ou = GLOBAL_CONFIG['LDAP_BASE_OU']
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
        user = "uid={username},{base_ou}".format(username=attributes['username'],
                                                 base_ou=GLOBAL_CONFIG['LDAP_BASE_OU'])
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
        user = 'uid={username},{base_ou}'.format(username=username,
                                                 base_ou=GLOBAL_CONFIG['LDAP_BASE_OU'])
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
        user = 'uid={username},{base_ou}'.format(username=username,
                                                 base_ou=GLOBAL_CONFIG['LDAP_BASE_OU'])
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
