/**************************
* Define GLOBAL variables *
***************************/
USER_CREATION_FORM = {
    'username': '#register-username',
    'password': '#register-password',
    'password-check': '#register-password-check',
    'firstname': '#register-firstname',
    'lastname': '#register-lastname',
    'email': '#register-email',
    'agreement': '#register-agreement'
};
USER_CREATION_BUTTON = '#register-btn';
USER_CREATION_URI = '/users/';

function openRegisterModal() {
    $('#register-modal').modal('show');
}

$(function(){
    /* Init some variables */
    password = new PasswordField(USER_CREATION_FORM.password);
    email = new EmailField(USER_CREATION_FORM.email);
    username = new UsernameField(USER_CREATION_FORM.username);
    firstname = new StandardField(USER_CREATION_FORM.firstname);
    lastname = new StandardField(USER_CREATION_FORM.lastname);
    agreement = new CheckField(USER_CREATION_FORM.agreement);

    var mandatory_options = {
        'password': password,
        'email': email,
        'username': username,
        'lastname': lastname,
        'firstname': firstname,
        'agreement': agreement
    };

    create_button = new SaveButton(USER_CREATION_BUTTON,
                                   mandatory_options,
                                   USER_CREATION_URI);

    /* jshint ignore:start */
    /* "jshint" don t like making function in loop but it s the cleanest way to activate focusout
       trigger w/ jQuery */
    for (let attribute in USER_CREATION_FORM) {
        $(USER_CREATION_FORM[attribute]).focusout(function(){
            create_button.validate();
        });
    }
    /* jshint ignore:end */
});
