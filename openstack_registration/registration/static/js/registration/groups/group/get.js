/**************************
* Define GLOBAL variables *
***************************/
GROUP_INFORMATION = null;

/* Define the HTML id that will use for user information show */
GROUP_INFORMATION_FORM = {
    'name': '#group-name',
    'description': '#group-description',
};
GROUP_INFORMATION_USERS = '#group-users';
GROUP_INFORMATION_MEMBERS = '#group-members';
GROUP_INFORMATION_ADMINS = '#group-admins';

/******************
* Define function *
*******************/
function getGroupAttributes() {
    $.getJSON(location.pahtname, {format: 'json'}, function(groups){
        GROUP_INFORMATION = new Group(groups[0]);

        for (let attribute in GROUP_INFORMATION_FORM) {
            $(GROUP_INFORMATION_FORM[attribute]).html(GROUP_INFORMATION[attribute]);
        }
    });
};

/*******************
* During load page *
********************/
$(function(){
    /* Load user information */
    getGroupAttributes();
});
