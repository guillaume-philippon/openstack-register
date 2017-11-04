"""
View module manage interface between user and openstack-registration. It provide a HTTP API based
on REST good practice.
"""
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from registration.datastore.UserInfoAccess import UserInfoAccess

from registration.Backend import OpenLdap
from registration.utils import *  # pylint: disable=unused-wildcard-import, wildcard-import

from registration import api

LOGGER = logging.getLogger("registration")
LOGGER_ERROR = logging.getLogger("registration_error")


def user_is_authenticate(request):
    """
    Return the status of current user

    :param request: Web request
    :return: JSonResponse
    """
    data = dict()
    data['status'] = 'False'
    if request.user.is_authenticated():
        data['status'] = 'True'
        data['user'] = str(request.user)
    return JsonResponse(data)


@login_required()
def user_is_admin(request, spec=None):
    """
    Return True if user is a administrator

    :param spec: ??
    :param request: Web request
    :return: JSonResponse
    """
    data = dict()
    data['admin'] = 'False'
    user = UserInfo.objects.filter(username=request.user)  # pylint: disable=no-member
    is_admin = UserInfoAccess.is_admin(request.user.get_username())

    if spec == 'dataTable':
        data['list'] = {}
        final_list = []
        admin = UserInfo.objects.filter(admin=True)  # pylint: disable=no-member

        for each in admin:
            tmp = {}
            username = each.username
            tmp['uid'] = username
            tmp['icon'] = ''
            final_list.append(tmp)

        data['list'] = final_list
        return JsonResponse(data)

    if spec == 'list':
        data['list'] = {}
        final_list = []
        admin = UserInfo.objects.filter(admin=True)  # pylint: disable=no-member

        for each in admin:
            tmp = {}
            username = each.username
            tmp['uid'] = username
            tmp['icon'] = ''
            final_list.append(tmp)

        data['list'] = final_list
        return data

    if user:
        is_admin = UserInfoAccess.is_admin(request.user.get_username())
        if is_admin is True:
            data['admin'] = 'True'
    if spec == 'python':
        return data
    return JsonResponse(data)


@login_required()
def logs_dispatcher(request):
    """
    make desc.
    :param request: Web request
    :return: void
    """
    if user_is_admin(request, spec='python')['admin'] != 'False':
        if request.method == 'GET'\
                and 'version' in request.GET:
            return logs_get_json(request)
        return logs_get_html(request)
    return redirect('/')


@login_required()
def logs_get_json(request):
    """
    Return the log file
    :param request: Web request
    :return: void
    """
    data = dict()
    log_file = open(GLOBAL_CONFIG['LOG_DIR'] + "/registration.log", "r")
    lines = log_file.readlines()
    log_file.close()
    version = request.GET['version']
    filtered = ''

    if 'filter' in request.GET and request.GET['filter'] != '':
        search = str(request.GET['filter'].encode('utf-8'))
        if version == 'actions':
            for line in lines:
                if line.__contains__(search) \
                        and (line.__contains__("CREATED")
                             or line.__contains__("MODIFIED")
                             or line.__contains__("LOGOUT")
                             or line.__contains__("LOGIN")):
                    filtered = line + filtered
        elif version == 'full':
            for line in lines:
                if line.__contains__(search):
                    filtered = line + filtered
    else:
        if version == 'actions':
            for each in lines:
                if each.__contains__("CREATE") \
                        or each.__contains__("MODIFIED") \
                        or each.__contains__("LOGIN") \
                        or each.__contains__("LOGOUT"):
                    filtered = each + filtered
        elif version == 'full':
            for each in lines:
                filtered = each + filtered
    data['logs'] = filtered
    return JsonResponse(data)


@login_required()
def logs_get_html(request):
    """
    Get log on HTML
    :param request: Web request
    :return: void
    """
    return render(request, 'logs/get.html')


@login_required()
def admin_dispatcher(request):  # pylint: disable=too-many-return-statements
    """
    Admin view dispatcher
    :param request: Web request
    :return: void
    """
    if user_is_admin(request, spec='python')['admin'] != 'False':
        if request.method == 'GET':
            if 'format' in request.GET \
                    and 'email' in request.GET \
                    and request.GET['format'] == 'json' \
                    and request.GET['email'] == 'bar':
                return user_get_json(request)
            elif 'format' in request.GET \
                    and 'spec' in request.GET \
                    and request.GET['format'] == 'json' \
                    and request.GET['spec'] == 'dataTable':
                return user_is_admin(request, spec='dataTable')
            elif 'format' in request.GET \
                    and request.GET['format'] == 'json':
                return admin_get_json(request)
            return admin_get_html(request)
        elif request.method == 'PUT':
            return admin_put_json(request)
        elif request.method == 'POST':
            return admin_post_json(request)
    return redirect('/')


@login_required()
def admin_users_dispatcher(request):  # pylint: disable=too-many-return-statements
    """
    TODO: need dispatcher

    :param request: Web request
    :return: void
    """
    if user_is_admin(request, spec='python')['admin'] != 'False':
        ldap = OpenLdap()
        if request.method == 'GET':
            if 'format' in request.GET \
                and 'spec' in request.GET \
                and request.GET['format'] == 'json' \
                    and request.GET['spec'] == 'dataTable':
                data = dict()
                data['users'] = dict()
                list_users = []
                user = dict()
                users = ldap.search_user(uid="foo", mail="bar", pager="all")

                for each in users:
                    user['uid'] = each[1]['uid'][0]
                    user['mail'] = each[1]['mail'][0]
                    try:
                        user['pager'] = {'pager': each[1]['pager'][0], 'state': '', 'display': ''}
                    except KeyError:
                        user['pager'] = dict()
                    list_users.append(user)
                    user = dict()
                data['users'] = list_users
                return JsonResponse(data)
            return api.users.get.html(request)
        elif request.method == 'PUT':
            info = dict()
            data = QueryDict(request.body).dict()
            user = str(data['user'])

            if 'password' in data:
                password = str(data['password'])
                try:
                    attrs = ldap.change_user_password(user, password)
                    LOGGER.info("USER MODIFIED  :: Operator : %s  :: admin changed %s password by"
                                " '%s'", request.user, user, password)
                    return JsonResponse(attrs)
                except:  # pylint: disable=bare-except
                    info['info'] = 'Fail to change your password.'
                    return render(request, 'error_get_html.html', context=info)
            elif 'action' in data:
                action = str(data['action'])
                try:
                    attrs = ldap.modify_user(user, action)
                    LOGGER.info("USER MODIFIED  :: Operator : %s  :: username=%s password"
                                " action=%s", request.user, user, action)
                    return JsonResponse(attrs)
                except:  # pylint: disable=bare-except
                    info['info'] = 'Fail to ' + action + ' user ' + user + '.'
                    return render(request, 'error/get.html', context=info)
    else:
        return redirect('/')


@login_required()
def admin_get_json(request):
    """
    TODO: make description
    :param request: Web request
    :return: void
    """
    data = dict()
    user = UserInfo.objects.filter(username=str(request.user))  # pylint: disable=no-member
    counter = user[0].countForce
    data['counter'] = counter
    return JsonResponse(data)


@login_required()
def admin_post_json(request):
    """
    TODO: make description
    :param request: Web request
    :return: void
    """
    attrs = dict()
    data = QueryDict(request.body).dict()
    group = normalize_string(data['group'])
    desc = normalize_string(data['desc'], option='name')

    if group != unicode(data['group']).encode(encoding='utf-8') \
            or desc != unicode(data['desc']).encode(encoding='utf-8'):
        attrs['group'] = group
        attrs['desc'] = desc
        attrs['status'] = 'change'
    else:
        ldap = OpenLdap()
        exist = ldap.search_group(uid=group)

        if exist != []:
            attrs['status'] = 'already'
        else:
            try:
                ldap.addGroup(group, desc, request.user)
                add_entry_group_info(group)
                LOGGER.info("GROUP CREATED  :: Operator : %s  :: Attributes : name=%s,"
                            " desc=%s ", request.user, group, desc)
                attrs['status'] = 'success'
            except:  # pylint: disable=bare-except
                attrs['status'] = 'fail'
    return JsonResponse(attrs)


@login_required()
def admin_put_json(request):
    """

    :param request:
    :return:
    """
    ldap = OpenLdap()
    data = QueryDict(request.body).dict()
    user = data['user']
    action = data['action']
    result = dict()
    list_admin = []

    exist = ldap.search_user(uid=user)

    if exist == []:
        result['status'] = 'not exist'
        return JsonResponse(result)
    else:
        dict_admin = user_is_admin(request, spec='list')
        for each in dict_admin['list']:
            list_admin.append(each['uid'])

        if str(user) in list_admin and action == 'add':
            result['status'] = 'already'
            return JsonResponse(result)
        else:
            if action == 'add':
                value = True
                update_count_force(request.user, 'add')
            else:
                if str(request.user) == str(user):
                    data['status'] = "itself"
                    return JsonResponse(data)
                value = False
                update_count_force(request.user, 'remove')
            if value:
                LOGGER.info("ADMIN MODIFIED :: Operator : %s  :: Attributes : user=%s,"
                            " action=promote super admin ", request.user, user)
            else:
                LOGGER.info("ADMIN MODIFIED :: Operator : %s  :: Attributes : user=%s,"
                            " action=dismiss super admin ", request.user, user)
            result = update_entry_user_info(user, value)
            return JsonResponse(result)


@login_required()
def admin_get_html(request):
    """

    :param request:
    :return:
    """
    if user_is_admin(request, spec='python')['admin'] != 'False':
        return render(request, "admin/admin.html")
    return redirect('/')


@login_required()
def user_is_group_admin(request, type=None):  # pylint: disable=redefined-builtin
    """
    make desc.
    :param request: Web request
    :param type: ??
    :return: void
    """
    data = dict()
    group_list = []
    user_list = []
    data['status'] = 'False'
    data['admin'] = 'False'
    user_admin = None

    if request.path_info.split('/')[1] == 'groupAdmin':
        location = request.path_info.split('/')[2]
        user_admin = IsAdmin.objects.filter(group__group_name=location)  # pylint: disable=no-member

    if user_is_admin(request, spec='python')['admin'] != 'False':
        data['status'] = 'True'
        data['admin'] = ['*']

    else:
        is_admin = GroupInfo.objects.filter(administrators__username=request.user)  # pylint: disable=no-member
        if is_admin:
            for each in is_admin:
                group_list.append(str(each.group_name))
            if user_admin:
                for each in user_admin:
                    user_list.append(str(each.administrators))
                data['user'] = user_list
            data['admin'] = group_list
            data['status'] = 'True'

    if type == 'python':
        return data
    return JsonResponse(data)


@login_required()
def modify_group_admin(request, user, group, action):
    """
    make desc.
    :param request: Web request
    :param user: user
    :param group: group
    :param action: action
    :return: void
    """
    data = dict()
    data['status'] = 'false'
    if (user_is_admin(request, spec='python')['admin'] != 'False'
            or (user_is_group_admin(request, type='python')['admin'] != 'False'
                and request.META['HTTP_REFERER'].split('/')[4]
                in user_is_group_admin(request, type='python')['admin'])):
        if user_is_admin(request, spec='python')['admin'] == 'False' \
                and user_is_group_admin(request, type='python')['admin'] != 'False' \
                and request.META['HTTP_REFERER'].split('/')[4] \
                        in user_is_group_admin(request, type='python')['admin'] \
                and str(request.user) == str(user):
            data['status'] = 'itself'
        else:
            if action == 'add':
                add_entry_is_admin(user, group)
                data['action'] = 'added'
                data['status'] = 'true'
            else:
                del_entry_is_admin(user, group)
                data['action'] = 'deleted'
                data['status'] = 'true'
    if 'action' in data:
        if data['action'] == 'added':
            LOGGER.info("GROUP MODIFIED :: Operator : %s  :: Attributes : group=%s, user=%s,"
                        " action=promote group admin ", request.user, group, user)
        elif data['action'] == 'deleted':
            LOGGER.info("GROUP MODIFIED :: Operator : %s  :: Attributes : group=%s, user=%s,"
                        " action=dismiss group admin ", request.user, group, user)
    return JsonResponse(data)


def login(request):
    """
    login view is used to log user on openstack-registration. It return a JSonResponse output with
    the status of login

        - **success**: user is logged
        - **failure**: user is not logged

    :param request: Web request
    :return: JSonResponse
    """
    # If user is already authenticated, we return a success status
    if request.user.is_authenticated():
        response = JsonResponse({
            'status': 'success'
        })
    # We use post method to authenticate user. we trap it to compute it.
    elif request.method == "POST":
        user = auth.authenticate(username=request.POST['username'].lower(),
                                 password=request.POST['password'])
        # If user is not None, then user is authenticated
        if user is not None:
            auth.login(request, user)
            LOGGER.info("USER LOGIN     :: User %s is connected from %s",
                        request.user, request.META.get('REMOTE_ADDR'))
            response = JsonResponse({
                'status': 'success'
            })
        # else the username or password is invalid
        else:
            LOGGER.info("LOGIN FAILED   :: Attempt to login with user '%s' from %s",
                        request.POST['username'], request.META.get('REMOTE_ADDR'))
            response = JsonResponse({
                'status': 'failure',
                'message': 'invalid username or password'
            })
    # If it s not a POST method, it s not supported by the view
    else:
        response = JsonResponse({
            'status': 'failure',
            'message': 'method {method} is not supported on login'
                       ' page'.format(method=request.method)
        })
    return response


@login_required()
def logout(request):
    """
    Logout user and redirect to login page
    :param request: HTTP request
    :return: HTTP
    """
    LOGGER.info("USER LOGOUT    :: User %s is disconnected from %s ",
                request.user, request.META.get('REMOTE_ADDR'))
    auth.logout(request)
    return redirect('/')


@login_required()
def groups_dispatcher(request):
    """
    make desc.
    :param request: Web request
    :return: void
    """
    if (user_is_admin(request, spec='python')['admin'] != 'False'
            or (user_is_group_admin(request, type='python')['admin'] != 'False'
                and (request.path_info.split('/')[2]
                     in user_is_group_admin(request, type='python')['admin']
                     or (len(request.META['HTTP_REFERER'].split('/')) == 5
                         and request.META['HTTP_REFERER'].split('/')[4]
                         in user_is_group_admin(request, type='python')['admin'])))):
        if request.method == 'PUT':
            data = QueryDict(request.body).dict()
            user = data['user']
            group = data['group']
            action = data['action']
            return modify_group_admin(request, user, group, action)
        elif request.method == 'GET'\
                and 'format' in request.GET\
                and request.GET['format'] == 'json':
            return groups_get_json(request, spec='all')
        return groups_get_html(request)

    elif request.method == 'GET'\
            and 'format' in request.GET\
            and request.GET['format'] == 'json'\
            and user_is_group_admin(request, type='python')['admin'] != 'False':
        return groups_get_json(request)
    elif request.method == 'GET'\
            and user_is_group_admin(request, type='python')['admin'] != 'False':
        return groups_get_html(request)
    else:
        return redirect('/')


@login_required()
def group_dispatcher(request):  # pylint: disable=too-many-return-statements
    """

    :param request:
    :return:
    """
    if request.method == 'GET'\
            and 'format' in request.GET\
            and 'email' in request.GET\
            and request.GET['format'] == 'json'\
            and request.GET['email'] == 'bar'\
            and ((user_is_group_admin(request, type='python')['admin'] != 'False'
                  and request.path_info.split('/')[2]
                  in user_is_group_admin(request, type='python')['admin'])
                 or user_is_admin(request, spec='python')['admin'] != 'False'):  # pylint: disable=too-many-boolean-expressions
        return user_get_json(request)
    elif request.method == 'GET'\
            and 'format' in request.GET\
            and request.GET['format'] == 'json'\
            and ((user_is_group_admin(request, type='python')['admin'] != 'False'
                  and request.path_info.split('/')[2]
                  in user_is_group_admin(request, type='python')['admin'])
                 or user_is_admin(request, spec='python')['admin'] != 'False'):  # pylint: disable=too-many-boolean-expressions
        return group_get_json(request)

    elif request.method == 'GET'\
            and ((user_is_group_admin(request, type='python')['admin'] != 'False'
                  and request.path_info.split('/')[2]
                  in user_is_group_admin(request, type='python')['admin'])
                 or user_is_admin(request, spec='python')['admin'] != 'False'):
        return group_get_html(request)

    elif request.method == 'GET'\
            and 'admin' in request.GET\
            and ((user_is_group_admin(request, type='python')['admin'] != 'False'
                  and request.path_info.split('/')[2]
                  in user_is_group_admin(request, type='python')['admin'])
                 or user_is_admin(request, spec='python')['admin'] != 'False'):
        return group_get_json(request)

    elif request.method == 'DEL'\
            and ((user_is_group_admin(request, type='python')['admin'] != 'False'
                  and request.path_info.split('/')[2]
                  in user_is_group_admin(request, type='python')['admin'])
                 or user_is_admin(request, spec='python')['admin'] != 'False'):
        return group_del_json(request)

    elif request.method == 'PUT'\
        and ((user_is_group_admin(request, type='python')['admin'] != 'False'
              and request.path_info.split('/')[2]
              in user_is_group_admin(request, type='python')['admin'])
             or user_is_admin(request, spec='python')['admin'] != 'False'):
        return group_put_json(request)
    return redirect('/')


@login_required()
def group_put_json(request):
    """

    :param request:
    :return:
    """
    status = "False"
    ldap = OpenLdap()
    data = QueryDict(request.body).dict()
    user = data['user']
    group = request.path_info.split('/')[2]

    try:
        dn_user = ldap.search_user(uid=user)[0][0]
        dn_group = ldap.search_group(group)[0][0]
        info = ldap.add_user_from_group(dn_user, dn_group)

        if info:
            status = "True"
            if user_is_admin(request, spec='python')['admin'] != 'False':
                update_count_force(request.user, 'add')
            else:
                status = "False"
            LOGGER.info("GROUP MODIFIED :: Operator : %s  :: Attributes : group=%s, user=%s,"
                        " action=member added", request.user, group, user)
        else:
            status = "already"
    except:  # pylint: disable=bare-except
        status = "not exist"

    data['status'] = status
    return JsonResponse(data)


@login_required()
def group_del_json(request):
    """

    :param request:
    :return:
    """
    ldap = OpenLdap()
    data = QueryDict(request.body).dict()
    user = data['user']

    if str(request.user) == str(user):
        data['status'] = 'itself'
        return JsonResponse(data)
    else:
        group = request.path_info.split('/')[2]
        dn_user = ldap.search_user(uid=user)[0][0]
        dn_group = ldap.search_group(group)[0][0]
        info = ldap.delete_user_from_group(dn_user, dn_group)

        if info:
            status = "True"
            if user_is_admin(request, spec='python')['admin'] != 'False':
                update_count_force(request.user, 'remove')
            try:
                del_entry_is_admin(user, group)
            except:  # pylint: disable=bare-except
                pass
            LOGGER.info("GROUP MODIFIED :: Operator : %s  :: Attributes : group=%s, user=%s, "
                        "action=member deleted", request.user, group, user)
        else:
            status = "False"
        data['status'] = status
        return JsonResponse(data)


@login_required()
def group_get_json(request):
    """

    :param request:
    :return:
    """
    data = {}
    ldap = OpenLdap()
    user_list = []

    if 'admin' in request.GET:
        location = request.path_info.split('/')[2]
        user_admin = IsAdmin.objects.filter(group__group_name=location)  # pylint: disable=no-member
        if user_admin:
            for each in user_admin:
                user_list.append(str(each.administrators))
            data['admin'] = user_list

    else:
        attrs = ldap.search_group(request.path_info.split('/')[2])
        data['attrs'] = {}

        for key, value in attrs:  # pylint: disable=unused-variable
            for each in value:
                data['attrs'][each] = value[each]

        if data['attrs']['uniqueMember'] is not '':  # pylint: disable=literal-comparison
            members = user_get_json(request, spec=data['attrs']['uniqueMember'])
            data['members'] = members['members']
            data['admin'] = members['admin']
    return JsonResponse(data)


@login_required()
def group_get_html(request):
    """

    :param request:
    :return:
    """
    return render(request, 'groups/group.html')


@login_required()
def user_get_json(request, spec=None):  #pylint: disable=too-many-branches, too-many-locals
    """

    :param spec:
    :param request:
    :return:
    """
    data = dict()
    ldap = OpenLdap()
    data['attrs'] = dict()
    data['users'] = dict()
    members = []
    final_list = []
    final_dict = dict()
    admin_list = []
    # TODO: What's spec ????
    if spec is not None:
        for uid in spec:
            # TODO: gloops, what's that ugly thing !!!
            attrs = ldap.search_user(attributes=str(uid).split('=')[1].split(',')[0])
            if attrs != []:
                members.append(attrs[0][1])
        for each in members:
            tmp = each
            for key in tmp:
                tmp[key] = tmp[key][0]
            tmp['icon'] = ''
            tmp['admin'] = ''
            final_list.append(tmp)

        # TODO: gloops, what's that ugly thing !!!
        location = request.path_info.split('/')[2]
        user_admin = IsAdmin.objects.filter(group__group_name=location)  # pylint: disable=no-member
        if user_admin:
            for each in user_admin:
                admin_list.append(str(each.administrators))
        data['admin'] = admin_list

        data['members'] = final_list
        return data
    elif 'email' in request.GET:
        # TODO: What's that foo-bar thing !!!
        users = ldap.search_user(uid="foo", mail="bar")
        for each in users:
            members.append(each[1])
        for each in members:
            tmp = each
            final_dict[tmp['uid'][0]] = tmp['mail'][0]
        data['users'] = final_dict
        return JsonResponse(data)

    else:
        attrs = ldap.search_user(attributes=request.user)
        for key, value in attrs:
            for each in value:
                data['attrs'][each] = value[each]
    return JsonResponse(data)


def home(request):
    """
    Default home page for openstack-registration. If user is already logged, we redirect him to
    it's own interface.

    :param request: Web request
    :return: HTTP rendering
    """
    if request.user.is_authenticated():
        response = HttpResponseRedirect('/users/{}'.format(request.user.get_username()))
    else:
        response = render(request, 'home.html')
    return response


@login_required()
def groups_get_html(request):
    """
    make desc.
    :param request: Web request
    :return: void
    """
    data = user_is_group_admin(request, type='python')
    if data['status'] != 'True':
        return redirect('/')
    return render(request, 'groups/groups.html')


@login_required()
def groups_get_json(request, spec=None):
    """
    make desc.
    :param request: Web request
    :param spec: Spec.
    :return: void
    """
    data = dict()
    groups = []

    if spec is not None:
        ldap = OpenLdap()
        groups_value = ldap.search_groups()
        for each in groups_value:
            groups.append(each[1]['cn'][0])
    else:
        is_admin = user_is_group_admin(request, type='python')
        for each in is_admin['admin']:
            groups.append(each)
    data['groups'] = groups
    return JsonResponse(data)


def policies(request):
    """
    Display policies web pages, only available throught html format.

    :param request: Web request
    :return: HTTP rendering
    """
    return render(request, 'policies.html')


def attributes_dispatcher(request):  # pylint: disable=too-many-statements, too-many-branches, too-many-return-statements
    """
    make desc.
    :param request: Web request
    :return: void
    """
    attributes = {}
    if 'password' in request.GET:
        password = request.GET['password']
        attributes = check_password_constraints(password)
        return JsonResponse(attributes)

    if 'checkPassword' in request.GET:
        ldap = OpenLdap()
        password = unicode(request.GET['checkPassword']).encode(encoding='utf-8')
        uid = str(request.user)
        userPassword = ldap.search_user(password=uid)  # pylint: disable=invalid-name
        userPassword = userPassword[0][1]['userPassword'][0]  # pylint: disable=invalid-name
        checked = check_password(userPassword, password)

        if checked:
            attributes['status'] = 'success'
        else:
            attributes['status'] = 'fail'
        return JsonResponse(attributes)

    if 'changePassword' in request.GET:
        info = dict()
        attributes = QueryDict(request.body).dict()
        ldap = OpenLdap()
        uid = str(request.user)
        password = encode_password(unicode(attributes['changePassword'])
                                   .encode(encoding='utf-8'))
        try:
            attrs = ldap.change_user_password(uid, password)
            LOGGER.info("USER MODIFIED  :: username=%s, action=password changed", request.user)
            return JsonResponse(attrs)
        except:  # pylint: disable=bare-except
            info['info'] = 'Fail to change your password.'
            return render(request, 'error_get_html.html', context=info)
    elif 'passwords' in request.GET:
        password = request.GET['passwords']
        attributes['password'] = encode_password(password)
        return render(request, 'users_get_html.html')

    elif 'uid' in request.GET:
        ldap = OpenLdap()
        uid = normalize_string(request.GET['uid'])
        checked = ldap.search_user(uid=uid)
        attributes['uid'] = uid

        if checked:
            attributes['status'] = 'fail'
        else:
            attributes['status'] = 'success'
        return JsonResponse(attributes)

    elif 'firstname' in request.GET:
        firstname = normalize_string(request.GET['firstname'], option='name')
        lastname = normalize_string(request.GET['lastname'], option='name')
        attributes['firstname'] = firstname
        attributes['lastname'] = lastname
        return JsonResponse(attributes)

    elif 'mail' in request.GET:
        ldap = OpenLdap()
        mail = request.GET['mail']
        checked = ldap.search_user(mail=mail)

        if checked:
            attributes['status'] = 'fail'
        else:
            attributes['status'] = 'success'
        return JsonResponse(attributes)

    elif 'project' in request.GET:
        project = normalize_string(request.GET['project'])
        attributes['project'] = project
        return JsonResponse(attributes)


def activate_user(request):
    """
    make desC.
    :param request: Web request
    :return: void
    """
    uuid = request.path.split('/action/')  # pylint: disable=redefined-outer-name
    uuid.pop(0)
    uuid = str(uuid[0])
    ldap = OpenLdap()
    info = dict()
    try:
        attrs = ldap.enable_user(uuid)
        send_mail(attrs['username'], attrs['firstname'], attrs['lastname'],
                  attrs['mail'], GLOBAL_CONFIG['project'],
                  GLOBAL_CONFIG['admin'], 'enable')
        LOGGER.info("USER MODIFIED  :: user=%s, action=activated", attrs['username'])
    except:  # pylint: disable=bare-except
        info['info'] = 'Your account is already enable or the url is not ' \
                          'valid, please check your mailbox.'
        return render(request, 'error_get_html.html', context=info)
    return render(request, 'home_get_html.html')
