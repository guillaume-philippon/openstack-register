function openRegisterModal() {
    $('#register-modal').modal('show');
}

$(function(){
    /* Init some variables */
    password = new PasswordField('#register-password');
    email = new EmailField('#register-email');
    username = new UsernameField('#register-username');
    firstname = new StandardField('#register-firstname');
    lastname = new StandardField('#register-lastname');
    agreement = new CheckField('#register-agreement');

    var mandatory_options = {
        'password': password,
        'email': email,
        'username': username,
        'lastname': lastname,
        'firstname': firstname,
        'agreement': agreement
    }

    create_button = new SaveButton('#register-btn', mandatory_options, '/users/', 'username');

    /* load action on focusout */
    $('#register-username').focusout(function () {
        create_button.validate();
    });
    $('#register-password').focusout(function () {
        create_button.validate();
    });
    $('#register-password-check').focusout(function () {
        create_button.validate();
    });
    $('#register-email').focusout(function () {
        create_button.validate();
    });
    $('#register-firstname').focusout(function () {
        create_button.validate();
    });
    $('#register-lastname').focusout(function () {
        create_button.validate();
    });
    $('#register-agreement').change(function () {
        create_button.validate();
    });
});
