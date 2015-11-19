function WelcomeCtrl($scope) {

}

// Global across all pages
$(window).load(function() {
    $('#header').addClass('hideSection');
    $('#content').addClass('hideSection');
    $('#header').fadeIn('fast');
    $('#content').fadeIn('slow');
});

$(document).ready(function () {

  // Animate navigation elements on page load
    $('#navigation-button').jAnimateOnce('fadeInLeft');
    $('#navigation-title').jAnimateOnce('fadeInDown');

  // Scroll to the top
  $(window).scroll(function () {
      if ($(this).scrollTop() > 100) {
          $('#scrollTop').fadeIn();
      } else {
          $('#scrollTop').fadeOut();
      }
  });

  $('#scrollTop').click(function () {
      $("html, body").animate({
          scrollTop: 0
      }, 600);
      return false;
  });

  // Hover over navigation button
  $('#navigation-button').hover(function() {
    //$('#navigation-menu').html('<img src="img/welcome/ubuntu-mate-gray.svg" width="11px" height="18px" style="object-fit: contain; margin: 0;">');
    $('#navigation-button').html('');
    $('#navigation-button').addClass('navigation-button-hover');
  }, function() {
    $('#navigation-button').removeClass('navigation-button-hover');
    $('#navigation-button').html('<span class="fa fa-chevron-left"></span>');
  });

});


// Main Menu Only = Rotate image on the main menu
if ( document.location.href.match(/[^\/]+$/)[0] == 'index.html' ) {

  // Bounce in logo once
  $('#mainLogo').jAnimateOnce('bounceIn');

  // Have we greeted the user already?
  if ( document.cookie == 'greeted=yes' ) {

    $(document).ready(function () {
      $(".fade").removeClass("fade");
      $(".fade-1s").removeClass("fade-1s");
      $(".fade-2s").removeClass("fade-2s");
      $(".fade-3s").removeClass("fade-3s");
      $(".fade-4s").removeClass("fade-4s");
      $(".fade-5s").removeClass("fade-5s");
    });
  }

  // When Welcome first runs, thank the user.
  if ( document.cookie == '') {
    $('#textChoose').hide();
    $('#textThanks').fadeIn('fast');

    setTimeout(function(){
      $('#textThanks').fadeOut('slow');
    }, 5000);

    setTimeout(function(){
      $('#textChoose').fadeIn('slow');
    }, 5600);

    document.cookie="greeted=yes";
  }

  // Sssh... You found the little secrets! ;)
  //// Logo starts to animate after a minute.
    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('tada');
    }, 60000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('flip');
    }, 60000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('rotateOut');
    }, 70000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('rotateIn');
    }, 71000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('rollOut');
    }, 80000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('rollIn');
    }, 81000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('zoomOut');
    }, 90000);

    setTimeout(function(){
      $('#mainLogo').jAnimateOnce('zoomIn');
    }, 91000);

  //// Ubuntu MATE's Birthday
    // Become official flavour on 26/Feb/2015
    var officialDay = 26; // (1-31)
    var officialMonth = 1; // (0-11)
    var officialYear = 2015;

  //// Celebrate Distro's Birthday
    var today = new Date();
    if ( today.getMonth() == officialMonth ) {
      if ( today.getDate() == officialDay ) {
        var UMAge = today.getFullYear() - officialYear;
        $('#textChoose').html("The distro is officially "+UMAge+" years old today. Happy Birthday!")
        $('#special').html('<canvas id="confetti" width="100%" height="100%" style="z-index: -1000; position: absolute; top: 0px; left: 0px;"></canvas>')
        //~ jQuery.getScript('js/confetti.js'); // This doesn't work! :(
        $('#mainLogo').jAnimateOnce('pulse');
        startConfetti();
      }
    }

  //// Celebrate Distro's Releases
    function checkReleaseDay(dd,mm,yyyy,release) {
      if ( today.getMonth() == mm - 1 ) {
        if ( today.getDate() == dd ) {
          if ( today.getFullYear() == yyyy ) {
            $('#textChoose').html("Today marks the release of Ubuntu MATE "+release+".")
            $('#special').html('<canvas id="confetti" width="100%" height="100%" style="z-index: -1000; position: absolute; top: 0px; left: 0px;"></canvas>')
            //~ jQuery.getScript('js/confetti.js'); // This doesn't work! :(
            $('#mainLogo').jAnimateOnce('pulse');
            startConfetti();
          }
        }
      }
    }

    // Release Dates
    // Possible improvement: Retrieve list from server.
    checkReleaseDay(31,12,2015,'16.04 Alpha 1');
    checkReleaseDay(28,01,2016,'16.04 Alpha 2');
    checkReleaseDay(25,02,2016,'16.04 Beta 1');
    checkReleaseDay(24,03,2016,'16.04 Beta 2');
    checkReleaseDay(21,04,2016,'16.04');
}

// Software Page Only = Categories for Apps
if ( document.location.href.match(/[^\/]+$/)[0] == 'software.html' ) {

    // Inital variables.
    var currentCategory;
    var hideNonFree = false;

    // Show the first category.
    currentCategory = '#Intro';
    $(currentCategory).jAnimateOnce('zoomInUp');
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
      if ( hideNonFree == true ) {
          // Toggle it OFF - Show non-free software.
          hideNonFree = false;
          $("#nonFreeCheckBox").addClass("fa-square");
          $("#nonFreeCheckBox").removeClass("fa-check-square");
          $('.proprietary').css('display','');
          $('.alternate').css('display','none');
      } else {
          // Toggle it ON - Hide non-free software.
          hideNonFree = true;
          $("#nonFreeCheckBox").removeClass("fa-square");
          $("#nonFreeCheckBox").addClass("fa-check-square");
          $('.proprietary').css('display','none');
          $('.alternate').css('display','');
      }
    });
}


// Splash Only - Animation Sequence
if ( document.location.href.match(/[^\/]+$/)[0] == 'splash.html' ) {

  // Scenes - Delayed elements to appear
  $(document).ready(function()
  {
    $('#sceneA').removeClass('hideSection');
    $('#sceneA').jAnimateOnce('fadeIn');

    setTimeout(function(){ $('#circle1').fadeOut('medium');}, 1000);
    setTimeout(function(){ $('#circle2').fadeOut('medium');}, 1100);
    setTimeout(function(){ $('#circle3').fadeOut('medium');}, 1200);
    setTimeout(function(){ $('#circle4').fadeOut('medium');}, 1300);
    setTimeout(function(){ $('#circle5').fadeOut('medium');}, 1400);

    setTimeout(function(){
      $('#sceneA').removeClass('hideSection');
      $('#sceneA').fadeOut();
    }, 1500);

    setTimeout(function(){
      $('#sceneB').removeClass('hideSection');
      $('#sceneB').jAnimateOnce('zoomIn');
      $('body').addClass('fadeToMenu');
    }, 2000);

    setTimeout(function(){
      $('body').removeClass('fadeToMenu');
      $('body').css('background-color','#f4f4f4');
    }, 3000);

    setTimeout(function(){
      $('#sceneB').fadeOut();
    }, 4000);

  });
}


// Getting Started Only - Index Pane for Selecting Topics
if ( document.location.href.match(/[^\/]+$/)[0] == 'gettingstarted.html' ) {

  function indexOpen() {
    // Is the index already open?
    if ($('#index-menu').is(':visible')) {
      indexClose();
    } else {
      // Open the Index
      $('#indexOpen').addClass('disabled');
      $('#indexOpen').prop('disabled', true);
      $("#index-overlay").fadeIn();
      $("#index-menu").show();
      $('#index-menu').jAnimateOnce('fadeInLeft');
    }
  }

  function indexClose() {
    $('#indexOpen').removeClass('disabled');
    $('#indexOpen').prop('disabled', false);
    if ($('#index-menu').is(':visible')) {
      $("#index-overlay").fadeOut();
      $('#index-menu').jAnimateOnce('fadeOutLeft',function(){
        $("#index-menu").hide();
      });
    }
  }

  function changePage(id,humanText) {
    // 'id' is one used for <div>.
    // 'humanText' is displayed on navigation's sub title.
    indexClose();
    $('.topicContents').fadeOut();
    $('#navigation-sub-title').fadeOut();

    // Smoothly fade between topics
    setTimeout(function() {
    $('#navigation-sub-title').html(humanText);
    $('#navigation-sub-title').fadeIn();
    $('#'+id).fadeIn();
    }, 500);
  }

  // Show inital page and index pane on page load
  changePage('initial','Choose a Topic');

  setTimeout(function() {
    indexOpen();
  }, 1000);

}
