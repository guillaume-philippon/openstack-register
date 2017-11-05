
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
                            'glyphicon-pencil"></span></a></p>';
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

function openEditModal(username) {
//    $('#user-edit-firstname').val(row.firstname);
//    $('#user-edit-lastname').val(row.lastname);
//    $('#user-edit-email').val(row.mail);
    $('#user-edit-modal').modal('show');
}