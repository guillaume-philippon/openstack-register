/**************************
* Define GLOBAL variables *
***************************/
GROUP_MEMBER_NAME = 'members';
GROUP_ADMIN_NAME = 'admins';

/*******************
* Define functions *
********************/
function addUserToMember(user, attribute){
        /* Prepare ajax request */
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        });

        return $.ajax({
            url: location.pathname + '/' + attribute + '/' + user,
            type: 'PUT',
        }).done(function(){
            groupReload();
        });

}

function removeUserToMember(user, attribute){
    /* Prepare ajax request */
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
        }
    });

    return $.ajax({
        url: location.pathname + '/' + attribute + '/' + user,
        type: 'DELETE',
    }).done(function(){
        groupReload();
    });
}

function groupReload(){
    $(GROUP_INFORMATION_ADMINS).DataTable().ajax.reload();
    $(GROUP_INFORMATION_MEMBERS).DataTable().ajax.reload();

}