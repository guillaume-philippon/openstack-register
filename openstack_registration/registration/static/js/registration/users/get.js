/**************************
* Define GLOBAL variables *
***************************/
USER_INFORMATION = null;
USER_INFORMATION_URI = '/users/';
//USER_INFORMATION_MODAL = '#user-edit-modal';
//USER_INFORMATION_FORM = {
//    'firstname': '#user-edit-firstname',
//    'lastname': '#user-edit-lastname',
//    'email': '#user-edit-email'
//};

/* function to get all users information and populate datable */
function getUsers() {
    $("#table-members").DataTable( {
        ajax: {
            url: location.pathname,
            data: {
                'format': 'json',
            },
            dataSrc: function (users) {
                return users;
            },
        },
        columns: [
            {
                data: 'uid',
                render: function(data, type, row){
                    return '<p><a href="#" class="btn" onclick="openEditModal(\'' +
                            data + '\')"><span class="glyphicon ' +
                            'glyphicon-pencil"></span></a>' +
                           '<a href="#" class="btn text-danger" onclick="openUserDeleteModal(\'' +
                            data + '\')"><span class="glyphicon ' +
                            'glyphicon-trash"></span></a></p>';
                },
                width: "50px"
            },
            { data: 'uid' },
            { data: 'firstname'},
            { data: 'lastname'},
            { data: 'mail'},
        ],
//        rowHeight": 'auto',
//        order: [[ 0, 'desc' ]],
//        iDisplayLength: 10,
//        stateSave: true,
//        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "ALL"] ],
    });
}

function openUserDeleteModal(username) {
    console.log(USER_DELETE_USERNAME + ' = ' + username);
    USER_INFORMATION = {
        'username': username,
    };
    $(USER_DELETE_USERNAME).text(USER_INFORMATION.username);
    $(USER_DELETE_MODAL).modal('show');
}

function openEditModal(username) {
    $.getJSON(USER_INFORMATION_URI + username, {format: 'json'}, function(data){
        USER_INFORMATION = new User(data[0]);
        $(USER_MODIFICATION_FORM.username).text(USER_INFORMATION.username);
        $(USER_MODIFICATION_FORM.firstname).val(USER_INFORMATION.firstname);
        $(USER_MODIFICATION_FORM.lastname).val(USER_INFORMATION.lastname);
        $(USER_MODIFICATION_FORM.email).val(USER_INFORMATION.email);
    }).done(function(){
        CURRENT_USERNAME = username;
        $(USER_MODIFICATION_MODAL).modal('show');
    });
}

function getUserAttributes() {
    $("#table-members").DataTable().ajax.reload();
}

$(function() {
    getUsers();
});
