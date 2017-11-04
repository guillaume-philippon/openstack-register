/* function to get all users information and populate datable */
function getUsers() {
    $("#table-members").DataTable( {
        ajax: {
            url: location.pathname,
            data: {
                'format': 'json',
            },
            dataSrc: function (users) {
                $.each(users, function(uid, attributes){
                    attributes.icon = '<span class="glyphicon glyphicon-pencil"></span>';
                    attributes.action = 'Actions';
                });
                return users;
            },
        },
        columns: [
            { data: 'icon'},
            { data: 'uid'},
            { data: 'mail'},
        ],
//        order: [[ 0, 'desc' ]],
//        iDisplayLength: 10,
//        stateSave: true,
//        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "ALL"] ],
    });
}
