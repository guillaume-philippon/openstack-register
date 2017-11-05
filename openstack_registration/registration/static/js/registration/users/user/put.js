var PASSWORD_STATUS = true;
var EMAIL_STATUS = true;

/* Open edit menu for user information */
function openEditInfoModal() {
    $('#user-edit-firstname').val($('#firstname-info').text());
    $('#user-edit-lastname').val($('#lastname-info').text());
    $('#user-edit-email').val($('#email-info').text());
    $('#user-edit-modal').modal('show');
}

/* Update user information */
function updateUserInformations(csrf){
    if ($('#user-edit-password-check').val() === "" &&
        $('#user-edit-password').val() !== "") {
        $('#user-edit-password-check-modal').modal('show');
    } else {
        var data = {
            'firstname': $('#user-edit-firstname').val(),
            'lastname': $('#user-edit-lastname').val(),
            'email': $('#user-edit-email').val(),
            'password': $('#user-edit-password').val()
        };
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                 xhr.setRequestHeader("X-CSRFToken",  csrf);
             }
        });
        $.ajax({
            url: location.pahtname,
            type: 'PUT',
            data: JSON.stringify(data)
        }).done(function(response){
            $('#user-edit-password-check-modal').modal('hide');
            $('#user-edit-modal').modal('hide');
            getUserAttributes();
        });
    }
}

/* Check password validity */
function checkPassword(password_field, group, btn){
    password = $(password_field).val();
    if (password === "") {
        $(group).removeClass('has-success');
        $(group).removeClass('has-error');
        PASSWORD_STATUS = true;
        checkPasswordButton('#user-edit-btn');
    } else {
        if (PASSWORD_REGEXP.test(password)) {
            PASSWORD_STATUS = true;
            changeGroupClass(group, 'has-success');
            checkPasswordButton('#user-edit-btn');
        } else {
            PASSWORD_STATUS = false;
            changeGroupClass(group, 'has-error');
            checkPasswordButton('#user-edit-btn');
        }
    }
}

/* Check if the second password is the same than the first */
function checkDualPassword() {
    first_password = $('#user-edit-password').val();
    second_password = $('#user-edit-password-check').val();
    if (first_password == second_password) {
        changeGroupClass('#user-edit-password-check-group', 'has-success');
        $('#user-edit-password-check-btn').removeClass('disabled');
    } else {
        changeGroupClass('#user-edit-password-check-group', 'has-error');
        $('#user-edit-password-check-btn').addClass('disabled');
    }
}

/* Check email format */
function checkEmail() {
    console.log('test')
    email = $('#user-edit-email').val()
    console.log(EMAIL_REGEXP.test(email))
    if (EMAIL_REGEXP.test(email)) {
        EMAIL_STATUS = true;
        changeGroupClass('#user-edit-group-email', 'has-success');
        checkPasswordButton('#user-edit-btn');
    } else {
        EMAIL_STATUS = false;
        changeGroupClass('#user-edit-group-email', 'has-error');
        checkPasswordButton('#user-edit-btn');
    };
}

/* Enable password button */
function checkPasswordButton(button) {
    if (PASSWORD_STATUS && EMAIL_STATUS) {
        $(button).removeClass('disabled');
    } else {
        $(button).addClass('disabled');
    }
}