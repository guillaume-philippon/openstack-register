/**************************
* Define GLOBAL variables *
***************************/
USER_INFORMATION = null;

/* Define the HTML id that will use for user information show */
USER_INFORMATION_FORM = {
    'username': '#username-info',
    'email': '#email-info',
    'firstname': '#firstname-info',
    'lastname': '#lastname-info'
};

/******************
* Define function *
*******************/
function getUserAttributes() {
    $.getJSON(location.pahtname, {format: 'json'}, function (users) {
            /* put all information in a User class */
            USER_INFORMATION = new User(users[0]);

            /* Update the informations field */
            for (let attribute in USER_INFORMATION_FORM) {
                $(USER_INFORMATION_FORM[attribute]).text(USER_INFORMATION[attribute]);
            }
        }
    );
}

/*******************
* During load page *
********************/
$(function(){
    /* Load user information */
    getUserAttributes();
});
