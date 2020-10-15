$(document).ready(function() {
    var get_login_user = '{{request.user.username}}'

    console.log(get_login_user);

    demo.initChartist();

    $.notify({
        icon: 'fa fa-user',
        message: " Welcome to Chess.Live " + get_login_user

    }, {
        type: 'info',
        timer: 10000
    });

});