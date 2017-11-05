class SaveButton {
    constructor(field, options, uri, uri_selector) {
        this.field = field;
        this.options = options;
        this.uri = uri; // Base uri for creation (/users/ per-example)
        this.uri_selector = uri_selector; // options field to add to the uri for
                                          // creation ('username')
    }

    validate() {
        var opts = this.options;
        var valid = true;

        /* We check if any options is not valide */
        for (let option in opts) {
            /* If field is not valid or previous field is not valid, then we change valid state
             to false */
            var field_class = opts[option]
            if (! (field_class.validate() && valid)) {
                valid = false;
            }
        }

        /* If all options are valid, then we enable button */
        if (valid) {
            $(this.field).removeClass('disabled');
        } else { // Else, we ensure that it is disabled
            $(this.field).addClass('disabled')
        }
    }

    create(csrf) {
        var opts = this.options; // local name for options
        var local_uri = this.uri + opts[this.uri_selector].get(); // Build uri (/users/*username*)
        var post_data = {
            csrfmiddlewaretoken: csrf,
        };
        /* Build post_data based on options */
        for (let option in opts) {
            post_data[option] = opts[option].get();
        }
        /* Ajax request for creation */
        $.post(local_uri, post_data, function(data){
            /* If user created, so we redirect to user information page */
            if (data.status == 'success') {
                $(location).attr('href', local_uri);
            } else { // else, just alert
                alert(data.message);
            }
        });
    }
}