function WelcomeCtrl($scope) {

}

// All Pages - In Transition
$(window).load(function() {
    $('#header').addClass('hideSection');
    $('#content').addClass('hideSection');
    $('#header').fadeIn('fast');
    $('#content').fadeIn('slow');
});


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


// Software Page Only - Categories for Apps
if ( document.location.href.match(/[^\/]+$/)[0] == 'software.html' ) {
    
    // Set the first landing category and animations.
    var currentCategory;
    
    // Show the first category.
    currentCategory = '#Intro';
    $(currentCategory).jAnimateOnce('zoomInRight');
    $(currentCategory).removeClass('hideSection');

    // Switch to another category.
    function switchCategory(now, next) {
        $(now).jAnimateOnce('fadeOut', function(self, effect){
            // Finished exit animation
            $(now).addClass('hideSection');

            // Show next category
            currentCategory = next;
            $(next).removeClass('hideSection');
            $(next).jAnimateOnce('fadeInLeft');
        });
        return currentCategory;
    }

    // Button triggers for functions
    $("#Accessories1").click(function(){ switchCategory(currentCategory, '#Accessories2');  });
    $("#Games1").click(function(){       switchCategory(currentCategory, '#Games2');  });
    $("#Graphics1").click(function(){    switchCategory(currentCategory, '#Graphics2');  });
    $("#Internet1").click(function(){    switchCategory(currentCategory, '#Internet2');  });
    $("#Office1").click(function(){      switchCategory(currentCategory, '#Office2');  });
    $("#Programming1").click(function(){ switchCategory(currentCategory, '#Programming2');  });
    $("#Media1").click(function(){       switchCategory(currentCategory, '#Media2');  });
    $("#SysTools1").click(function(){    switchCategory(currentCategory, '#SysTools2');  });
    $("#UnivAccess1").click(function(){  switchCategory(currentCategory, '#UnivAccess2');  });
    $("#MoreApps1").click(function(){    switchCategory(currentCategory, '#MoreApps2');  });
    $("#MoreAppsL").click(function(){    switchCategory(currentCategory, '#MoreApps2');  });

    // Show the popover on hover
    $('[rel=freedominfo]').popover({
        html : true,
        content: function() {
          return $('#popover_content_wrapper').html();
        }
    });

    // Hide Proprietary Toggle
    $('#nonFreeToggle').on('click', function (e) {
        if ( document.cookie == 'greeted=yes; hideNonFree=yes' ) {
            // Toggle it OFF - Show non-free software.
            document.cookie = "hideNonFree=no";
            $("#nonFreeCheckBox").addClass("fa-square");
            $("#nonFreeCheckBox").removeClass("fa-check-square");
            $('.proprietary').css('display','');
            $('.alternate').css('display','none');
        } else {
            // Toggle it ON - Hide non-free software.
            document.cookie = "hideNonFree=yes";
            $("#nonFreeCheckBox").removeClass("fa-square");
            $("#nonFreeCheckBox").addClass("fa-check-square");
            $('.proprietary').css('display','none');
            $('.alternate').css('display','');
        }
    });

    // Remember proprietary choice when returning.
    if ( document.cookie == 'greeted=yes; hideNonFree=yes' ) {
        // Hide and update check state.
        $("#nonFreeCheckBox").removeClass("fa-square");
        $("#nonFreeCheckBox").addClass("fa-check-square");
        $('.proprietary').css('display','none');
        $('.alternate').css('display','');
    } else {
        // Presume unchecked
        $('.proprietary').css('display','');
        $('.alternate').css('display','none');
    }
}


// Only animate the main menu one-at-a-time once.
function welcomeReturning() {
    $(document).ready(function () {
        $(".fade").removeClass("fade");
        $(".fade-1s").removeClass("fade-1s");
        $(".fade-2s").removeClass("fade-2s");
        $(".fade-3s").removeClass("fade-3s");
        $(".fade-4s").removeClass("fade-4s");
        $(".fade-5s").removeClass("fade-5s");
    });
}
