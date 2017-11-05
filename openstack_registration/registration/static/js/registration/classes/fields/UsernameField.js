class UsernameField extends StandardField {
    constructor (field) {
        super(field);
        this.field = field;
        this.uri_prefix = '/users/';
    }

    validate() {
        var username = $(this.field).val();
        var uri = this.uri_prefix + username;
        var field_name = this.field;
        var group_field_name = this.field + this.group_suffix;

        return $.getJSON(uri, function (data){
            if (data.status == 'UserNotExist') {
                $(group_field_name).removeClass('has-error');
                $(group_field_name).addClass('has-success');
                return true;
            } else {
                $(group_field_name).addClass('has-error');
                $(group_field_name).removeClass('has-success');
                return false;
            }
        })
        .error(function(data) {
            $(group_field_name).addClass('has-error');
            $(group_field_name).removeClass('has-success');
            return false;
        });
    }
}