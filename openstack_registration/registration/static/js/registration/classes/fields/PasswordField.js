/*

*/
class PasswordField {
    /* Provide needed stuff to manipulate password field
        - validate entry
        - toogle the field from password to input to make password readeable
    */
    constructor (field) {
        this.field = field;
        this.check_suffix = '-check';
        this.group_suffix = '-group';
        this.icon_suffix = '-icon';
        this.regexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*).{8,}$/;
//        $(this.field).focusout(function () {
//            $(this.field).validate();
//        });
//        $(this.field + this.check_suffix).focusout(function () {
//            $(this.field).validate();
//        });
    }

    validate() {
        /* get password entries */
        var first_password = $(this.field).val()
        var second_password = $(this.field + this.check_suffix).val()

        if (this.regexp.test(first_password)) {
            // If password match the regular expression, so we change the input-group class
            // to has-success
            $(this.field + this.group_suffix).removeClass('has-error');
            $(this.field + this.group_suffix).addClass('has-success');
            if (first_password == second_password) {
                // If the second password match the first (and first match the reg. exp.), then
                // we change input-group to has-success
                $(this.field + this.check_suffix + this.group_suffix).removeClass('has-error')
                $(this.field + this.check_suffix + this.group_suffix).addClass('has-success')
                return true;
            } else {
                // else, we make sure that input-group for check-password is in error
                $(this.field + this.check_suffix + this.group_suffix).removeClass('has-success')
                $(this.field + this.check_suffix + this.group_suffix).addClass('has-error')
                return false;
            }
        } else {
            $(this.field + this.group_suffix).removeClass('has-success')
            $(this.field + + this.group_suffix).addClass('has-error')
            $(this.field + this.check_suffix + this.group_suffix).removeClass('has-success')
            $(this.field + this.check_suffix + this.group_suffix).addClass('has-error')
            return false;
        }
    }

    tooglePasswordVisible(isCheck) {
        var icon_to_swap = this.field + this.icon_suffix;
        var field_to_swap = this.field;
        if (isCheck) {
            icon_to_swap = this.field + this.check_suffix + this.icon_suffix;
            field_to_swap = this.field + this.check_suffix;
        }
        if ( $(field_to_swap).attr('type') == 'password') {
                $(field_to_swap).attr('type', 'text');
                $(icon_to_swap).removeClass('glyphicon-eye-open');
                $(icon_to_swap).addClass('glyphicon-eye-close');
        } else {
                $(field_to_swap).attr('type', 'password');
                $(icon_to_swap).removeClass('glyphicon-eye-close');
                $(icon_to_swap).addClass('glyphicon-eye-open');
        }
    }
    get() {
        return $(this.field).val();
    }
}