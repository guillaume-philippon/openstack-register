class CheckField extends StandardField {
    constructor(field) {
        super(field);
        this.field = field;
    }

    validate() {
        var value = $(this.field).is(':checked');
        if (value) {
            return true;
        } else {
            return false;
        }
    }
}