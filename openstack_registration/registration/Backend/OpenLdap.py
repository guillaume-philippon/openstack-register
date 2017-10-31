"""
OpenLdap backend support
"""
# -*- coding: utf-8 -*-

import ldap
import ldap.sasl

from registration.Backend.PrototypeBackend import PrototypeBackend

from openstack_registration.config import GLOBAL_CONFIG

from registration.exceptions import InvalidX500DN  # pylint: disable=ungrouped-imports
from registration.models import UserActivation


# TODO: Should be named OpenLdapBackend to avoid miss-lead
class OpenLdap(PrototypeBackend):
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

    def add_user(self, username, email, firstname, lastname, x500dn, password):  # pylint: disable=too-many-arguments
        """
        Create a new user this its attributes
        :param username: username of new user
        :param email: email of the user
        :param firstname: first name of the user
        :param lastname: last name of the user
        :param x500dn: DN certificate
        :param password: password
        :return: void
        """
        attributes = []
        # TODO: ou base should be used from GLOBAL_CONFIG
        dn_user = "uid={},ou=users,o=cloud".format(username)
        attrs = {
            'objectClass': ['organizationalPerson', 'person', 'inetOrgPerson', 'top'],
            'uid': username,
            'mail': email,
            'givenName': firstname,
            'sn': lastname,
            'cn': "{} {}".format(firstname, lastname),
            'userPassword': str(password),
            'pager': '514',
            'seeAlso': str(x500dn)
        }

        for value in attrs:
            entry = (value, attrs[value])
            attributes.append(entry)

        try:
            self.connection.add_s(dn_user, attributes)
        except ldap.INVALID_SYNTAX:  # pylint: disable=no-member
            raise InvalidX500DN('')
        except:  # pylint: disable=bare-except
            exit(1)

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
