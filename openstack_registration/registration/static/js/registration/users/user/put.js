/**********************************
* GLOBAL variables initialization *
***********************************/
USER_MODIFICATION_FORM = {
    'username': '#user-edit-username',
    'firstname': '#user-edit-firstname',
    'lastname': '#user-edit-lastname',
    'email': '#user-edit-email'
};
USER_MODIFICATION_BUTTON = '#user-edit-btn';
USER_MODIFICATION_MODAL = '#user-edit-modal';
USERS_URI = '/users/';

USER_PASSWORD_MODIFICATION_FORM = {
    'password': '#user-edit-password',
    'password-check': '#user-edit-password-check'
};
USER_PASSWORD_MODIFICATION_BUTTON = '#user-edit-password-btn';
USER_PASSWORD_MODIFICATION_MODAL = '#user-edit-password-modal';

/******************
* Define function *
*******************/
function modifyUser(csrf){
    console.log(USER_INFORMATION);
    modify_button.modify(csrf, USER_INFORMATION.username).done(function(data){
        $(USER_MODIFICATION_MODAL).modal('hide');
        getUserAttributes();
    });
}

function modifyUserPassword(csrf){
    password_button.modify(csrf, USER_INFORMATION.username).done(function(data){
        $(USER_MODIFICATION_MODAL).modal('hide');
        $(USER_PASSWORD_MODIFICATION_MODAL).modal('hide');
        getUserAttributes();
    });
}

function openEditInfoModal() {
    $(USER_MODIFICATION_FORM.username).text(USER_INFORMATION.username);
    $(USER_MODIFICATION_FORM.firstname).val(USER_INFORMATION.firstname);
    $(USER_MODIFICATION_FORM.lastname).val(USER_INFORMATION.lastname);
    $(USER_MODIFICATION_FORM.email).val(USER_INFORMATION.email);
    $(USER_MODIFICATION_MODAL).modal('show');
}

/***********************
* Code run during load *
************************/
$(function(){
    /* init. object for modification form */
    password = new PasswordField(USER_PASSWORD_MODIFICATION_FORM.password);
    firstname = new StandardField(USER_MODIFICATION_FORM.firstname);
    lastname = new StandardField(USER_MODIFICATION_FORM.lastname);
    email = new EmailField(USER_MODIFICATION_FORM.email);

    /* load stuff for info. modification form. */
    var options = {
        'email': email,
        'lastname': lastname,
        'firstname': firstname,
    };
    modify_button = new SaveButton(USER_MODIFICATION_BUTTON,
                                   options,
                                   USERS_URI);

    /* jshint ignore:start */
    /* "jshint" don t like making function in loop but it s the cleanest way to activate focusout
       trigger w/ jQuery */
    for (let option in USER_MODIFICATION_FORM) {
        $(USER_MODIFICATION_FORM[option]).focusout(function(){
            modify_button.validate();
        });
    }
    /* jshint ignore:end */

    /* load stuff for password modification form. */
    var password_options = {
        'password': password
    };
    password_button = new SaveButton(USER_PASSWORD_MODIFICATION_BUTTON,
                                     password_options,
                                     USERS_URI);

    /* jshint ignore:start */
    /* "jshint" don t like making function in loop but it s the cleanest way to activate focusout
       trigger w/ jQuery */
    for (let option in USER_PASSWORD_MODIFICATION_FORM) {
        $(USER_PASSWORD_MODIFICATION_FORM[option]).focusout(function(){
            password_button.validate();
        });
    }
    /* jshint ignore:end */
});