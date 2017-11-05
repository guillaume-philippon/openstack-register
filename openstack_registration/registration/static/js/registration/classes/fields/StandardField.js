class StandardField {
    constructor(field) {
        this.field = field;
        this.group_suffix = '-group';
        this.regexp = /^.+$/;
    }

    validate() {
        var value = $(this.field).val()
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

    get() {
        return $(this.field).val();
    }
}