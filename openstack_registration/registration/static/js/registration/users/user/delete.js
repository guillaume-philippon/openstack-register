/**************************
* Define GLOBAL variables *
***************************/
USER_DELETE_USERNAME = '#user-delete-username';
USER_DELETE_MODAL = '#user-delete-modal';
USER_DELETE_URI = '/users/';

function openDeleteModal() {
    $(USER_DELETE_MODAL).modal('show');
}

function deleteUser(csrf) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
             xhr.setRequestHeader("X-CSRFToken",  csrf);
         }
    });
    $.ajax({
        url: USER_DELETE_URI + USER_INFORMATION.username,
        type: 'DELETE'
    }).done(function(response){
        $(location).attr('href', location.pathname);
    });
}

function cancelUser() {
    $(USER_DELETE_MODAL).modal('hide');
}

