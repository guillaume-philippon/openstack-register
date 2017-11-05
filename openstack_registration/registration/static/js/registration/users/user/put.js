function modifyUser(csrf){
    var username = $('#username-info').text();
    modify_button.modify(csrf, username).done(function(data){
        $('#user-edit-modal').modal('hide');
        getUserAttributes();
    });
}

function modifyUserPassword(csrf){
    var username = $('#username-info').text();
    password_button.modify(csrf, username).done(function(data){
        $('#user-edit-modal').modal('hide');
        $('#user-edit-password-modal').modal('hide');
        getUserAttributes();
    });
}

function openEditInfoModal() {
    $('#user-edit-firstname').val($('#firstname-info').text());
    $('#user-edit-lastname').val($('#lastname-info').text());
    $('#user-edit-email').val($('#email-info').text());
    $('#user-edit-modal').modal('show');
}

$(function(){
    // Populate user attributes
    getUserAttributes();

    // initialize object for modification form
    password = new PasswordField('#user-edit-password');
    firstname = new StandardField('#user-edit-firstname');
    lastname = new StandardField('#user-edit-lastname');
    email = new EmailField('#user-edit-email');

    var options = {
        'email': email,
        'lastname': lastname,
        'firstname': firstname,
    };
    modify_button = new SaveButton('#user-edit-btn', options, '/users/');

    var password_options = {
        'password': password
    };
    password_button = new SaveButton('#user-edit-password-btn', password_options, '/users/');

    $('#user-edit-firstname').focusout(function(){
        modify_button.validate();
    });
    $('#user-edit-lastname').focusout(function(){
        modify_button.validate();
    });
    $('#user-edit-email').focusout(function(){
        modify_button.validate();
    });

    /* enable focusout on password field */
    $('#user-edit-password').focusout(function(){
        password_button.validate();
    });
    $('#user-edit-password-check').focusout(function(){
        password_button.validate();
    });
});