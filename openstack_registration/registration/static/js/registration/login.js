/* All login js functions */

/* log user, if it s not a success, we shake the modal, if it is, we redirect to user web page */
function login(csrf) {
    var post_data = {
        csrfmiddlewaretoken: csrf,
        username: $('#login-username').val(),
        password: $('#login-password').val()
    }
    $.post('/login',post_data, function(data){
        if (data.status == 'success') {
            $('#login-modal').modal
            $(location).attr('href', '/users/' + post_data['username'])
        } else {
            $('#login-modal').shake(3, 7, 800)
        }
    })
}

/* Allow modal to be shaked */
jQuery.fn.shake = function(intShakes, intDistance, intDuration) {
    this.each(function() {
        for (var x=1; x<=intShakes; x++) {
            $(this).animate({left:(intDistance*-1)}, (((intDuration/intShakes)/4)))
            .animate({left:intDistance}, ((intDuration/intShakes)/2))
            .animate({left:0}, (((intDuration/intShakes)/4)));
        }
    });
    return this;
};