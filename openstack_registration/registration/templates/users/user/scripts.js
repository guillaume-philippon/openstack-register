$(document).ready(function() {
    getUserAttributes();
    $('#user-edit-password').focusout(function () {
        checkPassword('#user-edit-password', '#user-edit-password-group', '#user-edit-btn');
    });
    $('#user-edit-password-check').focusout(function () {
        checkDualPassword();
    });
    $('#user-edit-email').focusout(function (){
        checkEmail();
    });
});
