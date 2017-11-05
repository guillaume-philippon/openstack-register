class StandardField {
    /* init method */
    constructor(field) {
        this.field = field;
        this.group_suffix = '-group';
        this.regexp = /^.+$/;
    }

    /* validate field */
    validate() {
        var value = $(this.field).val();
        if (this.regexp.test(value)) {
            $(this.field + this.group_suffix).removeClass('has-error');
            $(this.field + this.group_suffix).addClass('has-success');
            return true;
        } else {
            $(this.field + this.group_suffix).addClass('has-error');
            $(this.field + this.group_suffix).removeClass('has-success');
            return false;
        }
    }

    /* get form value */
    get() {
        return $(this.field).val();
    }

    /* set value */
    set(value) {
        $(this.field).val(value);
    }
}