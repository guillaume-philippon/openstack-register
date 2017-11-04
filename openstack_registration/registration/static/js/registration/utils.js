/* Regexp for mail@example.fr */
const EMAIL_REGEXP = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

/* Test if password have at lease
    - 1 low char
    - 1 up char
    - 1 digit
*/
const PASSWORD_REGEXP = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,}$/;

/* Display password in clear text or dot format */
function tooglePasswordFieldType(password, icon) {
    if ( $(password).attr('type') == 'password') {
            $(password).attr('type', 'text');
            $(password + '-icon').removeClass('glyphicon-eye-open');
            $(password + '-icon').addClass('glyphicon-eye-close');
    } else {
            $(password).attr('type', 'password');
            $(password + '-icon').removeClass('glyphicon-eye-close');
            $(password + '-icon').addClass('glyphicon-eye-open');
    }
}


/* Change the class of input-group (has-error/has-success) */
function changeGroupClass(group, addClass) {
    if (addClass == 'has-success') {
        removeClass = 'has-error';
    } else {
        removeClass = 'has-success';
    }
    if ($(group).hasClass(removeClass)) {
        $(group).removeClass(removeClass);
        $(group).addClass(addClass);
    }
}


/* Check email validity*/
function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
