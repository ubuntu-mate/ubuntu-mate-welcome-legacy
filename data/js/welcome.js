function WelcomeCtrl($scope) {

}

// Scroll to the top
$(document).ready(function () {

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
            $('.floatnav').fadeIn();
        } else {
            $('.scrollup').fadeOut();
            $('.floatnav').fadeOut();
        }
    });

    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });

});