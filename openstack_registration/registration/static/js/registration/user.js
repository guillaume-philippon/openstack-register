/*
Javascript module to manage all user related interaction with openstack-registration.
*/

/* getUserAttributes get information for the logged user. If there are more than one response or the
response is empty, then there are a problem */
function getUserAttributes() {
    $.getJSON(location.pahtname, {format: 'json'}
    ).done(
        function (users) {
            for ( user in users ) {
                $('#usernameInput').val(users[user].uid);
                $('#emailInput').val(users[user].mail);
                $('#firstnameInput').val(users[user].firstname);
                $('#lastnameInput').val(users[user].lastname);
                $('#fullnameInput').val(users[user].fullname);
            }
        }
    );
}

/* toggle disable value for a specific input id */
function toggleInput(field) {
    if ( $('#' + field).prop('disabled')) {
        $('#' + field).prop('disabled', false);
    } else {
        $('#' + field).prop('disabled', true);
    }
    $('#btn-save').addClass('btn-danger')
    $('#btn-save').prop('disabled', false);
}
