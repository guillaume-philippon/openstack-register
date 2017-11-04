$(function(){
    $('#register-username').focusout(function () {
        checkUsername();
    });
    $('#register-password').focusout(function () {
        checkPassword();
    });
    $('#register-password-check').focusout(function () {
        checkPassword();
    });
    $('#register-email').focusout(function () {
        checkEmail();
    });
    $('#register-firstname').focusout(function () {
        checkFirstName();
    });
    $('#register-lastname').focusout(function () {
        checkLastName();
    });
    $('#register-agreement').focusout(function () {
        checkAgreement();
    });

});
