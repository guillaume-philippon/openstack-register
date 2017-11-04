/* All login js functions */
var USERNAME_STATUS = false;
var PASSWORD_STATUS = false;
var FIRSTNAME_STATUS = false;
var LASTNAME_STATUS = false;
var AGREEMENT_STATUS = false;
var EMAIL_STATUS = false;

/* Regexp for mail@example.fr */
const EMAIL_REGEXP = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

/* Test if password have at lease
    - 1 low char
    - 1 up char
    - 1 digit
*/
const PASSWORD_REGEXP = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,}$/;

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
        console.log(data)
        if (data.status == 'success') {
            $(location).attr('href', '/users/' + username)
        } else {
            alert(data.message)
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
//        console.log('All register from status are true');
//        console.log('USERNAME_STATUS: ' + USERNAME_STATUS);
//        console.log('PASSWORD_STATUS: ' + PASSWORD_STATUS);
//        console.log('EMAIL_STATUS: ' + EMAIL_STATUS);
//        console.log('FIRSTNAME_STATUS: ' + FIRSTNAME_STATUS);
//        console.log('LASTNAME_STATUS: ' + LASTNAME_STATUS);
//        console.log('AGREEMENT_STATUS: ' + AGREEMENT_STATUS);
        $('#register-btn').removeClass('disabled');
    } else { // Else, we disable it
//        console.log('Some register from status are false');
//        console.log('USERNAME_STATUS: ' + USERNAME_STATUS);
//        console.log('PASSWORD_STATUS: ' + PASSWORD_STATUS);
//        console.log('EMAIL_STATUS: ' + EMAIL_STATUS);
//        console.log('FIRSTNAME_STATUS: ' + FIRSTNAME_STATUS);
//        console.log('LASTNAME_STATUS: ' + LASTNAME_STATUS);
//        console.log('AGREEMENT_STATUS: ' + AGREEMENT_STATUS);
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
    username = $('#register-username').val()
    $.getJSON('/users/' + username, function (data){
        if (data.status == 'UserNotExist') {
            USERNAME_STATUS = true;
            $('#register-username').attr('style', 'border-color:green');
        }
    })
    .error(function(data) {
        USERNAME_STATUS = false;
        $('#register-username').attr('style', 'border-color:red');
    });
    checkRegisterStatus();
}

function checkPassword() {
    /* Retrieve both password */
    first_password = $('#register-password').val();
    second_password = $('#register-password-check').val();

    /* test if passwords are the same & if it match REGEXP */
    if (first_password == second_password && PASSWORD_REGEXP.test(first_password)) {
        $("#register-password").attr('style', 'border-color:green;')
        $("#register-password-check").attr('style', 'border-color:green;')
        PASSWORD_STATUS = true;
    } else {
        $("#register-password").attr('style', 'border-color:red;')
        $("#register-password-check").attr('style', 'border-color:red;')
        PASSWORD_STATUS = false;
    }
    checkRegisterStatus();
}

function checkEmail() {
    email = $('#register-email').val();
    if (EMAIL_REGEXP.test(email)) {
        EMAIL_STATUS = true;
        $("#register-email").attr('style', 'border-color:green;')
    } else {
        EMAIL_STATUS = false;
        $("#register-email").attr('style', 'border-color:red;')
    }
    checkRegisterStatus();
}

function checkFirstName() {
    firstname = $('#register-firstname').val();
    if (FIRSTNAME_REGEXP.test(firstname)) {
        FIRSTNAME_STATUS = true;
        $("#register-firstname").attr('style', 'border-color:green;')
    } else {
        FIRSTNAME_STATUS = false;
        $("#register-firstname").attr('style', 'border-color:red;')
    }
    checkRegisterStatus();
}

function checkLastName() {
    lastname = $('#register-lastname').val();
    if (LASTNAME_REGEXP.test(lastname)) {
        LASTNAME_STATUS = true;
        $("#register-lastname").attr('style', 'border-color:green;')
    } else {
        LASTNAME_STATUS = false;
        $("#register-lastname").attr('style', 'border-color:red;')
    }
    checkRegisterStatus()
}

function checkAgreement() {
    agreement = $('#register-agreement').is(':checked');
    console.log(agreement)
    if (agreement) {
        AGREEMENT_STATUS = true;
    } else {
        AGREEMENT_STATUS = false;
    }
    checkRegisterStatus();
}

/* Check email validity*/
function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}