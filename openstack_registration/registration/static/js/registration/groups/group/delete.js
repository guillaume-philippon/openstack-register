/**************************
* Define GLOBAL variables *
***************************/
GROUP_DELETE_NAME = '#group-delete-name';
GROUP_DELETE_MODAL = '#group-delete-modal';
GROUP_DELETE_URI = '/groups/';

function openDeleteModal(group) {
    $(GROUP_DELETE_MODAL).modal('show');
}

function deleteGroup(csrf) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
             xhr.setRequestHeader("X-CSRFToken",  csrf);
         }
    });
    $.ajax({
        url: GROUP_DELETE_URI + GROUP_INFORMATION.name,
        type: 'DELETE'
    }).done(function(data){
        reloadGroups();
        $(GROUP_DELETE_MODAL).modal('hide');
    });
}

function cancelGroup() {
    $(GROUP_DELETE_MODAL).modal('hide');
}

function reloadGroups() {
     $(GROUP_INFORMATION_TABLE).DataTable().ajax.reload();
}

