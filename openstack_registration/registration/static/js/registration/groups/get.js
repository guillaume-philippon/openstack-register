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
                GROUP_INFORMATION = groups;
                return groups;
            },
        },
        columns: [
            {
                data: 'name',
                render: function(data, type, row) {
                    return '<p><a href="/groups/' + data + '" class="btn"> ' +
                            '<span class="glyphicon ' +
                            'glyphicon-pencil"></span></a>' +
                           '<a href="#" class="btn text-danger" onclick="openGroupDeleteModal(\'' +
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

function openGroupDeleteModal(group) {
    $(GROUP_DELETE_NAME).text(group);
    GROUP_INFORMATION = {
        'name': group
    };
    $(GROUP_DELETE_MODAL).modal('show');
}

function openGroupCreateModal() {
    $(GROUP_CREATE_MODAL).modal('show');
}

$(function(){
    getGroups();
});