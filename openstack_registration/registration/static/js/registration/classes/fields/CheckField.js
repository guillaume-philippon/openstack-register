class CheckField {
    constructor(field) {
        this.field = field;
    }

    validate() {
        var value = $(this.field).is(':checked')
        if (value) {
            return true;
        } else {
            return false;
        }
    }
    get() {
        return $(this.field).val();
    }
}