function WelcomeCtrl($scope) {

}

// "Slide in" navigation bar when page loads.
$(document).ready(function() {
    var $nav = $('#navigation');
    $nav.css('left', -$nav.outerWidth());
    $nav.show();
    $nav.delay(250).animate({ left: 0 }, 500);
});


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
