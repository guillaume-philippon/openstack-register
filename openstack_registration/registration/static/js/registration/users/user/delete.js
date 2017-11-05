function openDeleteModal() {
    $('#user-delete-modal').modal('show');
}

function deleteUser(csrf) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
             xhr.setRequestHeader("X-CSRFToken",  csrf);
         }
    });
    $.ajax({
        url: location.pahtname,
        type: 'DELETE'
    }).done(function(response){
        $(location).attr('href', '/');
    });
}

function cancelUser() {
    $('#user-delete-modal').modal('hide');
}

