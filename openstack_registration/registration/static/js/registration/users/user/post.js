/* All login js functions */
var USERNAME_STATUS = false;
var PASSWORD_STATUS = false;
var FIRSTNAME_STATUS = false;
var LASTNAME_STATUS = false;
var AGREEMENT_STATUS = false;
var EMAIL_STATUS = false;

/* Firstname & lastname must have at least one char */
const FIRSTNAME_REGEXP = /^.+$/;
const LASTNAME_REGEXP = /^.+$/;

/* log user, if it s not a success, we shake the modal, if it is, we redirect to user web page */
function register(csrf) {
    var post_data = {
        csrfmiddlewaretoken: csrf,
        username: $('#register-username').val(),
        password: $('#register-password').val(),
        firstname: $('#register-firstname').val(),
        lastname: $('#register-lastname').val(),
        email: $('#register-email').val()
    };
    $.post('/users/' + post_data.username, post_data, function(data){
        if (data.status == 'success') {
            $(location).attr('href', '/users/' + username);
        } else {
            alert(data.message);
        }
    });
}

function checkRegisterStatus() {
    /* If all field status are true, then we enable the register button */
    if (USERNAME_STATUS &&
        PASSWORD_STATUS &&
        FIRSTNAME_STATUS &&
        LASTNAME_STATUS &&
        AGREEMENT_STATUS
    ) {
        $('#register-btn').removeClass('disabled');
    } else { /* Else, we disable it */
        if (! $('#register-btn').hasClass('disabled')) {
            $('#register-btn').addClass('disabled');
        }
    }
}

function openRegisterModal() {
    $('#register-modal').modal('show');
    checkRegisterStatus();
}

function checkUsername() {
    username = $('#register-username').val();
    $.getJSON('/users/' + username, function (data){
        if (data.status == 'UserNotExist') {
            USERNAME_STATUS = true;
            changeGroupClass("#register-group-username", "has-success");
        }
    })
    .error(function(data) {
        USERNAME_STATUS = false;
        changeGroupClass("#register-group-username", "has-error");
    });
    checkRegisterStatus();
}

function checkPassword() {
    /* Retrieve both password */
    first_password = $('#register-password').val();
    second_password = $('#register-password-check').val();

    /* If the first password match the regexp, so we accept it */
    if (PASSWORD_REGEXP.test(first_password)) {
        changeGroupClass("#register-group-password", "has-success");
    } else {
        changeGroupClass("#register-group-password", "has-error");
    }

    /* test if passwords are the same & if it match REGEXP */
    if (first_password == second_password && PASSWORD_REGEXP.test(first_password)) {
        changeGroupClass("#register-group-password-check", "has-success");
        PASSWORD_STATUS = true;
    } else {
        changeGroupClass("#register-group-password-check", "has-error");
        PASSWORD_STATUS = false;
    }
    checkRegisterStatus();
}

function checkEmail() {
    email = $('#register-email').val();
    if (EMAIL_REGEXP.test(email)) {
        EMAIL_STATUS = true;
        changeGroupClass("#register-group-email", "has-success");
    } else {
        EMAIL_STATUS = false;
        changeGroupClass("#register-group-email", "has-error");
    }
    checkRegisterStatus();
}

function checkFirstName() {
    firstname = $('#register-firstname').val();
    if (FIRSTNAME_REGEXP.test(firstname)) {
        FIRSTNAME_STATUS = true;
        changeGroupClass("#register-group-firstname", "has-success");
    } else {
        FIRSTNAME_STATUS = false;
        changeGroupClass("#register-group-firstname", "has-error");
    }
    checkRegisterStatus();
}

function checkLastName() {
    lastname = $('#register-lastname').val();
    if (LASTNAME_REGEXP.test(lastname)) {
        LASTNAME_STATUS = true;
        changeGroupClass("#register-group-lastname", "has-success");
    } else {
        LASTNAME_STATUS = false;
        changeGroupClass("#register-group-lastname", "has-error");
    }
    checkRegisterStatus();
}

function checkAgreement() {
    agreement = $('#register-agreement').is(':checked');
    if (agreement) {
        AGREEMENT_STATUS = true;
    } else {
        AGREEMENT_STATUS = false;
    }
    checkRegisterStatus();
}
