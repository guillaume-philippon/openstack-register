/**************************
* Define GLOBAL variables *
***************************/
GROUP_INFORMATION = null;
GROUP_INFORMATION_URI = '/groups/';
GROUP_INFORMATION_TABLE = '#table-groups';



function getGroups() {
    $(GROUP_INFORMATION_TABLE).DataTable({
        ajax: {
            url: GROUP_INFORMATION_URI,
            data: {
                'format': 'json',
            },
            dataSrc: function(groups){
                return groups;
            },
        },
        columns: [
            {
                data: 'name',
                render: function(data, type, row) {
                    return '<p><a href="#" class="btn" onclick="openEditModal(\'' +
                            data + '\')"><span class="glyphicon ' +
                            'glyphicon-pencil"></span></a>' +
                           '<a href="#" class="btn text-danger" onclick="openUserDeleteModal(\'' +
                            data + '\')"><span class="glyphicon ' +
                            'glyphicon-trash"></span></a></p>';
                },
                width: "50px"
            },
            { data: 'name' },
            { data: 'description' }
        ],
    });
}

function openGroupCreateModal() {
    $(GROUP_CREATE_MODAL).modal('show')
}

$(function(){
    getGroups();
})