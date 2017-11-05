class UsernameField {
    constructor (field) {
        this.field = field;
        this.group_suffix = '-group';
        this.uri_prefix = '/users/'
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
            console.log('error')
            $(group_field_name).addClass('has-error');
            $(group_field_name).removeClass('has-success');
            return false;
        });
    }

    get() {
        return $(this.field).val();
    }
}