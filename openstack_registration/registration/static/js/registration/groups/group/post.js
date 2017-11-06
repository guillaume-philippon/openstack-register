/**************************
* Define GLOBAL variables *
***************************/
GROUP_CREATE_MODAL = '#create-modal';
GROUP_CREATE_FORM = {
    'name': '#create-name',
    'description': '#create-description'
}
GROUP_CREATE_BUTTON = '#create-btn';
GROUP_CREATE_URI = '/groups/';

$(function(){
    group_name = new GroupNameField(GROUP_CREATE_FORM.name);
    description = new StandardField(GROUP_CREATE_FORM.description);

    var options = {
        'name': group_name,
        'description': description
    };

    create_button = new SaveButton(GROUP_CREATE_BUTTON,
                                   options,
                                   GROUP_CREATE_URI);

    /* jshint ignore:start */
    for (let attribute in GROUP_CREATE_FORM) {
        $(GROUP_CREATE_FORM[attribute]).focusout(function(){
            create_button.validate()
        });
    };
    /* jshint ignore:end */
});