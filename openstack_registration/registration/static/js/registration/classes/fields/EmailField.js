class EmailField extends StandardField  {
    constructor (field) {
        super(field);
        this.field = field;
        this.regexp = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    }

    /* Validate form field */
    validate() {
        var email = $(this.field).val();
        if (this.regexp.test(email)) {
            $(this.field + this.group_suffix).removeClass('has-error');
            $(this.field + this.group_suffix).addClass('has-success');
            return true;
        } else {
            $(this.field + this.group_suffix).removeClass('has-success');
            $(this.field + this.group_suffix).addClass('has-error');
            return false;
        }
    }
}