/**************************
* Define GLOBAL variables *
***************************/
GROUP_INFORMATION = null;

/* Define the HTML id that will use for user information show */
GROUP_INFORMATION_FORM = {
    'name': '#group-name',
    'description': '#group-description',
};
GROUP_INFORMATION_USERS = '#group-users';
GROUP_INFORMATION_MEMBERS = '#group-members';
GROUP_INFORMATION_ADMINS = '#group-admins';

USER_INFORMATION_URI = '/users/';

/******************
* Define function *
*******************/
function getGroupAttributes() {
    $.getJSON(location.pahtname, {format: 'json'}, function(groups){
        GROUP_INFORMATION = new Group(groups[0]);

        for (let attribute in GROUP_INFORMATION_FORM) {
            $(GROUP_INFORMATION_FORM[attribute]).html(GROUP_INFORMATION[attribute]);
        }
    });
}

function getGroupAdmins() {
    $(GROUP_INFORMATION_ADMINS).DataTable({
        ajax: {
            url: location.pathname + '/admins',
            data: {
                format: 'json',
            },
            dataSrc: function (data) {
                members = data[0].admins;
                response = [];
                for (let member = 0; member < members.length; member++){
                    response[member] = {
                        'admins': members[member]
                    };
                }
                return response;
            },
        },
        columns: [
            {
                data: 'admins',
                render: function (data, type, row){
                    return '<a href="#" class="btn btn-danger btn-sm"' +
                           ' onclick="removeUserToMember(\'' + data + '\', \'admins\')">' +
                           '<span class="glyphicon glyphicon-arrow-left"></span>' +
                           '</a>';
                },
                orderable:  false
            },
            { data: 'admins' }
        ],
        paging: false,
        searching: false,
        order: [[1, 'asc']]
    });
}

function getGroupMembers() {
    $(GROUP_INFORMATION_MEMBERS).DataTable({
        ajax: {
            url: location.pathname + '/members',
            data: {
                format: 'json',
            },
            dataSrc: function (data) {
                members = data[0].members;
                response = [];
                for (let member = 0; member < members.length; member++){
                    response[member] = {
                        'members': members[member]
                    };
                }
                return response;
            },
        },
        columns: [
            {
                data: 'members',
                render: function (data, type, row){
                    return '<a href="#" class="btn btn-danger btn-sm"' +
                           ' onclick="removeUserToMember(\'' + data + '\', \'members\')"> ' +
                           '<span class="glyphicon glyphicon-arrow-left"></span>' +
                           '</a>';
                },
                orderable:  false
            },
            { data: 'members' },
            {
                data: 'members',
                render: function (data, type, row){
                    return '<a href="#" class="btn btn-primary btn-sm"' +
                           ' onclick="addUserToMember(\'' + data + '\', \'admins\')"> ' +
                           '<span class="glyphicon glyphicon-arrow-right"></span>' +
                           '</a>';
                },
                orderable:  false
            },
        ],
        paging: false,
        searching: false,
        order: [[1, 'asc']]
    });
}

function getGroupUsers() {
    $(GROUP_INFORMATION_USERS).DataTable({
        ajax: {
            url: USER_INFORMATION_URI,
            data: {
                format: 'json',
            },
            dataSrc: function (users) {
                return users;
            },
        },
        columns: [
            { data: 'uid' },
            {
                data: 'uid',
                render: function (data, type, row){
                    return '<a href="#" class="btn btn-primary btn-sm"' +
                           ' onclick="addUserToMember(\'' + data + '\', \'members\')">' +
                           '<span class="glyphicon glyphicon-arrow-right"></span>' +
                           '</a>';
                },
                orderable:  false
            },
        ],
        paging: false,
        searching: false,
    });
}


/*******************
* During load page *
********************/
$(function(){
    /* Load user information */
    getGroupAttributes();
    getGroupAdmins();
    getGroupMembers();
    getGroupUsers();
});
