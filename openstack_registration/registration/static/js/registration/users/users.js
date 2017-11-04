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
            { data: 'action' },
        ],
//        order: [[ 0, 'desc' ]],
//        iDisplayLength: 10,
//        stateSave: true,
//        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "ALL"] ],
    });
}

function colorLine () {
    var numberOfRows;
    var eachRow;
    eachRow = document.getElementById('users_table').rows;
    numberOfRows = eachRow.length;
    for (var i = 0; i < numberOfRows; i++) {
        if (eachRow[i].className == 'odd') {
            eachRow[i].setAttribute('style', 'background: #f3f3f3');
        }
        else {
            eachRow[i].removeAttribute('style');
        }
    }
}

function changePasswordModal(user) {
    $('#myModalLabel')[0].firstChild.data = 'Change ' + user + ' password:';
    $('#newPasswordLabel')[0].firstChild.data = 'New ' + user + ' password *:';
    $('#passwordLabel')[0].firstChild.data = 'Retype new ' + user + ' password *:';
    $user = user;
    $('#adminModalPassword').modal('show');
}



function changeState(username, action) {
    $.ajaxSetup({
        beforeSend : function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}" );
        }
    });
    $.ajax({
        url: location.pathname,
        type: 'PUT',
        data: { 'format': 'json',
                'user': username,
                'action': action,
        },
        success: function(json) {
            $("#table_id").DataTable().ajax.reload(null, false);
        }
    });
}

function check_actual_password() {
    $.getJSON("/attributes/?format=json", { checkPassword: $('#actualPasswordInput').val() }).done(
        function (json) {
            if (json.status == 'fail') {
                document.getElementById("errorPassword").innerHTML = "This is not your actual password !";
                $oldPassword = 'False';
            }
            else if (json.status == 'success') {
                $oldPassword = 'True';
                enable_change_button();
            }
        }
    );
}

function check_password_constraints() {
    $.getJSON( "/attributes/?format=json", { password: $('#newPasswordInput').val() }).done(
        function(json) {
            if ( json.check == 'character' ) {
               document.getElementById("errorPassword").innerHTML = "Password have to contains at least 8 characters !";
                $newPassword = 'False';
            }
            else if ( json.check == 'require' ) {
                document.getElementById("errorPassword").innerHTML = "Password have to contains lowercase, uppercase, digit, special (at least 3/4) !";
                $newPassword = 'False';
            }
            else if ( json.check == 'success' ) {
                $newPassword = 'True';
                enable_change_button();
            }
        }
    );

    if ( $("#newPasswordInput").val() != $("#reNewPasswordInput").val() ) {
            document.getElementById("errorPassword").innerHTML = "Password aren't matching !";
    }
    else {
        document.getElementById("errorPassword").innerHTML = '';
    }
}

function enable_change_button() {
    if ( ($oldPassword == 'True') && ($newPassword == 'True') && (document.getElementById("errorPassword").innerHTML === '')) {
        $('#changeButton').removeAttr('disabled');
    }
    else {
        $('#changeButton').attr('disabled', 'disabled');
    }
}

function disable_change_button() {
    $('#actualPasswordInput, #newPasswordInput, #reNewPasswordInput').click(function() {
        $('#changeButton').attr('disabled', 'disabled');
    });
}

function change_password() {
    $('#changeButton').click(function() {
        $.ajaxSetup({
            beforeSend : function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}" );
            }
        });
        $.ajax({
            url: location.pathname,
            type: 'PUT',
            data: { 'password': $('#newPasswordInput').val(),
                    'user' : $user,
            },
            success: function(json) {
                if (json.status == 'success') {
                    document.getElementById("errorPassword").innerHTML = 'Password has been changed !';
                    clear_form();
                }
                else {
                    document.getElementById("errorPassword").innerHTML = 'Password have not been changed !';
                }
            },
            error: function() {
            }
        });
    });
}

function hide_see_password() {
    $('#passwordIcon1').click( function() {
        if ( $("#actualPasswordInput").attr('type') == 'password') {
            $("#actualPasswordInput").attr('type', 'text');
            $('#passwordIcon1').attr('title', 'Hide Password');
            $('#passwordIcon1').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-close');
        }
        else {
            $("#actualPasswordInput").attr('type', 'password');
            $('#passwordIcon1').attr('title', 'See Password');
            $('#passwordIcon1').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-open');
        }
    });
    $('#passwordIcon2').click( function() {
        if ( $("#newPasswordInput").attr('type') == 'password') {
            $("#newPasswordInput").attr('type', 'text');
            $('#passwordIcon2').attr('title', 'Hide Password');
            $('#passwordIcon2').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-close');
        }
        else {
            $("#newPasswordInput").attr('type', 'password');
            $('#passwordIcon2').attr('title', 'See Password');
            $('#passwordIcon2').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-open');
        }
    });
    $('#passwordIcon3').click( function() {
        if ( $("#reNewPasswordInput").attr('type') == 'password') {
            $("#reNewPasswordInput").attr('type', 'text');
            $('#passwordIcon3').attr('title', 'Hide Password');
            $('#passwordIcon3').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-close');
        }
        else {
            $("#reNewPasswordInput").attr('type', 'password');
            $('#passwordIcon3').attr('title', 'See Password');
            $('#passwordIcon3').attr('class', 'btn btn-primary input-group-addon glyphicon glyphicon-eye-open');
        }
    });
}

function clear_form() {
    $("#actualPasswordInput").val('');
    $("#newPasswordInput").val('');
    $("#reNewPasswordInput").val('');
    $('#changeButton').attr('disabled', 'disabled');
    $oldPassword = 'False';
    $newPassword = 'False';
}
