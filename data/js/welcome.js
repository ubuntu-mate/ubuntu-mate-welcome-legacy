function WelcomeCtrl($scope) {

}

// Consistent on all pages.
var global_footer_left = '<div id="social" class="pull-left">' +
        '<a href="cmd://link?https://plus.google.com/communities/108331279007926658904" title="Google+"><img src="img/social/google+.svg"></a>' +
        '<a href="cmd://link?https://www.facebook.com/UbuntuMATEedition/" title="Facebook"><img src="img/social/facebook.svg"></a>' +
        '<a href="cmd://link?https://twitter.com/ubuntu_mate" title="Twitter"><img src="img/social/twitter.svg"></a>' +
        '<a href="cmd://link?https://ubuntu-mate.org" title="ubuntu-mate.org"><img src="img/humanity/website.svg"></a>' +
        '<a href="cmd://link?https://ubuntu-mate.org/donate/" title="ubuntu-mate.org/donate/"><img src="img/humanity/donate.svg"></a>' +
      '</div>';

var global_footer_right = '<a href="cmd://quit" class="btn btn-inverse">&zwnj;Close&zwnj;</a>';
var global_scrollToTop = '<a href="#" id="scrollTop" class="navigation-button"><span class="fa fa-chevron-up"></span></a>';

// Global across all pages
$(window).load(function() {
    // Smoothly fade into the page.
    $('.entire-page-fade').fadeIn('medium');
});

// Smoothly fade out of the page.
function smoothOut(target_href) {
    $('.entire-page-fade').fadeOut('medium');
    $('#navigation-title').fadeOut('medium');
    $('.navigation-button').fadeOut('medium');
    setTimeout(function(){
        window.location.href = target_href;
    }, 400);
}

$(document).ready(function() {
  // Animate navigation elements on page load
  $('#menu-button').jAnimateOnce('fadeInLeft');
  $('#navigation-title').jAnimateOnce('fadeInDown');

  // Write shared elements
  $('#footer-left').append(global_footer_left);
  $('#footer-right').append(global_footer_right);
  $('#footer').append(global_scrollToTop);

  // Initialize scroll to the top
  $(window).scroll(function () {
      if ($(this).scrollTop() > 90) {
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

});

// Smoothly fade between two elements (by ID)
function smoothFade(from, to) {
  $(from).fadeOut();
  setTimeout(function(){ $(to).fadeIn(); }, 400 );
}

// Smoothly fade the navigation sub-title
function changeSubtitle(textToDisplay) {
  // Smoothly fade subtitle
  $('#navigation-sub-title').fadeOut();
  setTimeout(function() {
    $('#navigation-sub-title').html(textToDisplay);
    $('#navigation-sub-title').fadeIn();
  }, 400);
}

// For pages that depend on an internet connection, but Welcome couldn't connect.
function reconnectTimeout() {
  if ( ! $('#reconnectFailed').is(':visible') ) {
    $('#reconnectFailed').fadeIn();
  } else {
    $('#reconnectFailed').jAnimateOnce('pulse');
  }
}


// Main Menu Only = Animation
if ( document.location.href.match(/[^\/]+$/)[0] == 'index.html' ) {

  // Animate elements of the page
  $('#mainLogo').jAnimateOnce('rotateIn');
  $('.menuMainText').fadeIn('slow');
  $('#open-at-start').jAnimateOnce('fadeIn');
  setTimeout(function(){
    $('#mate-blur').jAnimateOnce('zoomIn');
    $('#mate-blur').show();
  }, 50);

  function exitMenu(target) {
      // Show a "wait" cursor for the Software page, as there is a slight delay.
      if ( target == 'software.html' ) {
          $('html').css('cursor','wait')
          $('a').css('cursor','wait')
      }

      $('#mate-blur').jAnimateOnce('zoomOut');
      smoothOut(target)
  }

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

  // Enable tooltips
  $(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
  });

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

    function create_canvas() {
      $('#special').html('<canvas id="confetti" width="100%" height="100%" style="z-index: -1000; position: absolute; top: 0px; left: 0px;"></canvas>');
      $('#mainLogo').jAnimateOnce('pulse');
      startConfetti();
    }

    // Internally work with days, months and years as a number.
    function dateAsNumber(day, month, year) {
      // Assumes 'month' parameter is in base 0.
      // day, month   = Required.
      // year         = Optional, set to 'null' to use current year.
      var then = new Date();
      if ( year != null ) {
        then.setYear(year);
      }
      then.setMonth(month-1);
      then.setDate(day);
      var finalNumber = Math.floor( then / (1000 * 60 * 60 * 24) );
      //~ var dateInYears = current + todayAsNumber;
      //~ console.log('** finalNumber: '+finalNumber)
      //~ return dateInYears;
      return finalNumber;
    }

    // What is today?
    var today = new Date();
    var todayAsNumber = dateAsNumber(today.getDate(), today.getMonth()+1, null)

    // Check dates for special events.
    function specialEventCheck(dateNo, title_text, show_confetti, fa_icon) {
      // dateNo        = dateAsNumber(dd, mm, yyyy) function.
      // title_text    = Text to display when date matches.
      // show_confetti = True / False = Celebrate when date matches.
      // fa_icon       = FontAwesome icon to display. Usually 'bell' or 'calendar'.
      var do_show_this = false;
      if ( dateNo == todayAsNumber) {
        // Today is the day!
        var do_show_this = true;
      }
      if ( do_show_this == true ) {
        $('.menuMainText').html("<span class='fa fa-" + fa_icon + "'></span>&nbsp;" + title_text);
        if ( show_confetti == true ) {
          create_canvas();
        }
      }
    }

    // Dates to be checking for.
      // Use 'dd', 'mm' and 'yyyy' variables to re-use code.
      var dd = 0;  var mm = 0;  var yyyy = 0;

      // Official Flavour Status - 26/Feb/2015
      var age = today.getFullYear() - 2015;
      dd = 26; mm = 02; yyyy = null;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-7, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 7 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-6, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 6 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-5, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 5 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-4, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 4 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 3 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;in&zwnj; 2 &zwnj;days time&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "&zwnj;Ubuntu MATE celebrates its official flavour status&zwnj; &zwnj;tomorrow&zwnj;.", true, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "&zwnj;Ubuntu MATE become an official flavour&zwnj; " + age + " &zwnj;years ago today&zwnj;.", true, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; &zwnj;yesterday&zwnj;.", true, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 2 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 3 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+4, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 4 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+5, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 5 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+6, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 6 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+7, "&zwnj;Ubuntu MATE celebrated its official flavour status&zwnj; 7 &zwnj;days ago&zwnj;.", false, 'calendar');

      // Project Birthday - 21/Jun/2014
      var age = today.getFullYear() - 2014;
      dd = 21; mm = 06; yyyy = null;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-7, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old&zwnj; &zwnj;a week today!", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-6, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old in&zwnj; 6 &zwnj;days time&zwnj;!", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-5, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old in&zwnj; 5 &zwnj;days time&zwnj;!", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-4, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old in&zwnj; 4 &zwnj;days time&zwnj;!", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old in&zwnj; 3 &zwnj;days time&zwnj;!", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old in&zwnj; 2 &zwnj;days time&zwnj;!", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "&zwnj;The project will be&zwnj; " + age + " &zwnj;years old&zwnj; &zwnj;tomorrow. Happy Birthday!&zwnj;", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "&zwnj;The project is&zwnj; " + age + " &zwnj;years old today. Happy Birthday!&zwnj;", true, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; &zwnj;yesterday. Happy Birthday!&zwnj;", true, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; 2 &zwnj;days ago&zwnj;.", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; 3 &zwnj;days ago&zwnj;.", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+4, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; 4 &zwnj;days ago&zwnj;.", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+5, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; 5 &zwnj;days ago&zwnj;.", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+6, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; 6 &zwnj;days ago&zwnj;.", false, 'birthday-cake');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+7, "&zwnj;The project turned&zwnj; " + age + " &zwnj;years old&zwnj; &zwnj;last week&zwnj;.", false, 'calendar');

      // Holiday Celebrations
      specialEventCheck(dateAsNumber(31,12,null), "&zwnj;Happy New Year from Ubuntu MATE!&zwnj;", true, 'calendar');
      specialEventCheck(dateAsNumber(01,01,null), "&zwnj;Happy New Year from Ubuntu MATE!&zwnj;", true, 'calendar');

      // 16.04 Alpha 1
      dd = 04; mm = 01; yyyy = 2016;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "Ubuntu MATE 16.04 Alpha 1 &zwnj;will be released in&zwnj; 3 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "Ubuntu MATE 16.04 Alpha 1 &zwnj;will be released in&zwnj; 2 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "Ubuntu MATE 16.04 Alpha 1 &zwnj;will be released tomorrow&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "Ubuntu MATE 16.04 Alpha 1 &zwnj;is released today&zwnj;!", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 1.", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 1.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 1.", false, 'bug');

      // 16.04 Alpha 2
      dd = 28; mm = 01; yyyy = 2016;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "Ubuntu MATE 16.04 Alpha 2 &zwnj;will be released in&zwnj; 3 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "Ubuntu MATE 16.04 Alpha 2 &zwnj;will be released in&zwnj; 2 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "Ubuntu MATE 16.04 Alpha 2 &zwnj;will be released tomorrow&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "Ubuntu MATE 16.04 Alpha 2 &zwnj;is released today&zwnj;!", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 2.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 2.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Alpha 2.", false, 'bug');

      // 16.04 Beta 1
      dd = 25; mm = 02; yyyy = 2016;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "Ubuntu MATE 16.04 Beta 1 &zwnj;will be released in&zwnj; 3 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "Ubuntu MATE 16.04 Beta 1 &zwnj;will be released in&zwnj; 2 &zwnj;days&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "Ubuntu MATE 16.04 Beta 1 &zwnj;will be released tomorrow&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "Ubuntu MATE 16.04 Beta 1 &zwnj;is released today&zwnj;!", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 1.", true, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 1.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 1.", false, 'bug');

      // 16.04 Beta 2
      dd = 24; mm = 03; yyyy = 2016;
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "Ubuntu MATE 16.04 Beta 2 &zwnj;will be released in&zwnj; 3 days.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "Ubuntu MATE 16.04 Beta 2 &zwnj;will be released in&zwnj; 2 days.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "Ubuntu MATE 16.04 Beta 2 &zwnj;will be released tomorrow&zwnj;.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "Ubuntu MATE 16.04 Beta 2 &zwnj;is released today&zwnj;!", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 2.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 2.", false, 'bug');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "&zwnj;Thank you for testing&zwnj; Ubuntu MATE 16.04 Beta 2.", false, 'bug');

      // 16.04 Final Release
      dd = 21; mm = 04; yyyy = 2016; var build = '16.04 LTS'
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-7, "Ubuntu MATE " + build + " &zwnj;will be released a week today&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-6, "Ubuntu MATE " + build + " &zwnj;will be released in&zwnj; 6 days.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-5, "Ubuntu MATE " + build + " &zwnj;will be released in&zwnj; 5 &zwnj;days&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-4, "Ubuntu MATE " + build + " &zwnj;will be released in&zwnj; 4 &zwnj;days&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-3, "Ubuntu MATE " + build + " &zwnj;will be released in&zwnj; 3 &zwnj;days&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-2, "Ubuntu MATE " + build + " &zwnj;will be released in&zwnj; 2 &zwnj;days&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)-1, "Ubuntu MATE " + build + " &zwnj;will be released tomorrow.&zwnj;", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)  , "Ubuntu MATE " + build + " &zwnj;is released today&zwnj;!", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+1, "Ubuntu MATE " + build + " &zwnj;was released yesterday&zwnj;.", true, 'bell');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+2, "Ubuntu MATE " + build + " &zwnj;was released&zwnj; 2 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+3, "Ubuntu MATE " + build + " &zwnj;was released&zwnj; 3 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+4, "Ubuntu MATE " + build + " &zwnj;was released&zwnj; 4 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+5, "Ubuntu MATE " + build + " &zwnj;was released&zwnj; 5 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+6, "Ubuntu MATE " + build + " &zwnj;was released&zwnj; 6 &zwnj;days ago&zwnj;.", false, 'calendar');
      specialEventCheck(dateAsNumber(dd,mm,yyyy)+7, "Ubuntu MATE " + build + " &zwnj;was released last week&zwnj;.", false, 'calendar');

    // To-do as possible improvement: Retrieve events as a list from server.
}


// Introduction/Features = Animation
if ( document.location.href.match(/[^\/]+$/)[0] == 'introduction.html' || document.location.href.match(/[^\/]+$/)[0] == 'features.html' ) {
  new WOW().init();
}


// Software Page Only = Categories for Apps
if ( document.location.href.match(/[^\/]+$/)[0] == 'software.html' ) {

    // Initial variables.
    var currentCategory;
    var hideNonFree = false;
    var system_info = '';

    // Show the first category.
    currentCategory = '#Intro';
    $(currentCategory).jAnimateOnce('zoomInLeft');
    $(currentCategory).show();

    // Switch to another category.
    function switchCategory(now, next, subtitle) {
        // Smoothly fade subtitle
        changeSubtitle(subtitle);

        // Fade in non-free toggle as it starts hidden, except on the Misc. page,
        // where it's replaced by a command visibility toggle.
        if ( next == '#Misc' ) {
          smoothFade('#nonFreeToggle','#MiscCmd');
        } else {
          smoothFade('#MiscCmd','#nonFreeToggle');
        }

        // Animate out, then animate in next category.
        $(now).fadeOut('fast');
        setTimeout(function() {
          $(now).hide();
          currentCategory = next;
          $(next).show();
          $(next).jAnimateOnce('fadeInDown');
        }, 250);

        // Show all apps again, in case the previous page was filtered.
        $('.app-entry').fadeIn();

        // Reset filters
        selected_filter = 'none';
        $('.filter-box').val('none');
        applyFilter();

        return currentCategory;
    }

    // Show small label while hovering categories.
    function hoverCategoryTab(text,menuItemID) {
      $('#categoryHover').html(text);
      $('#categoryHover').show();

      var x = $(menuItemID).position();
      var length = $('#categoryHover').width();
      $('#categoryHover').css('left', (x.left+24) - (110/2) )
    }

    // A category tab is clicked.
    function changeCategoryTab(id,humanText) {
      switchCategory(currentCategory, id, humanText);
      $('#categoryHover').fadeOut()
    }

    function jumpOneClickServers(appno) {
      changeCategoryTab('#Servers','&zwnj;Servers&zwnj;');
      $('#ServersBtn').tab('show');
      $('html, body').animate({ scrollTop: 0 }, 100)

      // WORKAROUND = Cannot use ' or " strings, use numbers to get target div ID:
      if ( appno == 1 ) {  targetDiv = 'minecraft-server';  }
      if ( appno == 2 ) {  targetDiv = 'x2go-server';  }

      setTimeout(function(){
          $('html, body').animate({
              scrollTop: $('#'+targetDiv).offset().top - 100
          }, 1000);
      }, 1000);
    }

    // Show the popover/tooltips on hover
    $(document).ready(function() {
      $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });
    $('[rel=freedominfo]').popover({
        html : true,
        content: function() {
          return $('#popover_content_wrapper').html();
        }
    });

    // Filtering applications by subcategory and/or proprietary software.
    selected_filter = 'none';

    $("select").change(function(){
        selected_filter = $(this).val();
        applyFilter();
    });

    $('#nonFreeToggle').on('click', function (e) {
        toggleNonFree();
    });

    function applyFilter() {
        window.location.href = 'cmd://filter-apps?' + selected_filter + '?';
    }

    function toggleNonFree() {
        window.location.href = 'cmd://filter-apps?' + selected_filter + '?toggle';
    }


    // Featured Grid - Randomly populate and add applications to the grid.
    var iconID = 0;
    function addToGrid(icon) {
      iconID++;
      $('#featuredGrid').append('<img src="img/applications/'+icon+'.png" id="appIcon' + iconID + '" class="gridHidden" />');
    }

    // Featured Grid - Set classes to create a semi-circle fade effect.
    function initGrid() {
        $('#appIcon1').addClass('gridOuter');
        $('#appIcon2').addClass('gridOuter');
        $('#appIcon3').addClass('gridOuter');
        $('#appIcon4').addClass('gridOuter');
        $('#appIcon5').addClass('gridOuter');
        $('#appIcon8').addClass('gridOuter');
        $('#appIcon9').addClass('gridOuter');
        $('#appIcon12').addClass('gridOuter');
        $('#appIcon13').addClass('gridOuter');
        $('#appIcon14').addClass('gridOuter');
        $('#appIcon15').addClass('gridOuter');
        $('#appIcon16').addClass('gridOuter');

        $('#appIcon6').addClass('gridInner');
        $('#appIcon7').addClass('gridInner');
        $('#appIcon10').addClass('gridInner');
        $('#appIcon11').addClass('gridInner');

        // Gently fade the icons into view.
        setTimeout(function(){ $('#appIcon1').removeClass('gridHidden'); }, 800 );

        setTimeout(function(){ $('#appIcon2').removeClass('gridHidden'); }, 850 );
        setTimeout(function(){ $('#appIcon5').removeClass('gridHidden'); }, 850 );
        setTimeout(function(){ $('#appIcon6').removeClass('gridHidden'); }, 850 );

        setTimeout(function(){ $('#appIcon3').removeClass('gridHidden'); }, 900 );
        setTimeout(function(){ $('#appIcon6').removeClass('gridHidden'); }, 900 );
        setTimeout(function(){ $('#appIcon9').removeClass('gridHidden'); }, 900 );

        setTimeout(function(){ $('#appIcon4').removeClass('gridHidden'); }, 950 );
        setTimeout(function(){ $('#appIcon7').removeClass('gridHidden'); }, 950 );
        setTimeout(function(){ $('#appIcon10').removeClass('gridHidden'); }, 950 );
        setTimeout(function(){ $('#appIcon13').removeClass('gridHidden'); }, 950 );

        setTimeout(function(){ $('#appIcon8').removeClass('gridHidden'); }, 1000 );
        setTimeout(function(){ $('#appIcon11').removeClass('gridHidden'); }, 1000 );
        setTimeout(function(){ $('#appIcon14').removeClass('gridHidden'); }, 1000 );

        setTimeout(function(){ $('#appIcon12').removeClass('gridHidden'); }, 1050 );
        setTimeout(function(){ $('#appIcon15').removeClass('gridHidden'); }, 1050 );

        setTimeout(function(){ $('#appIcon16').removeClass('gridHidden'); }, 1100 );
    }

    // Misc Tab - Show commands if user wishes to know them.
    var showMiscCommands = false;
    $('.miscCmd').hide();

    $('#MiscCmd').click(function() {
      if ( showMiscCommands == false ) {
        // Show the terminal commands.
        showMiscCommands = true;
        $('.miscCmd').fadeIn();
        $("#MiscCheckbox").removeClass("fa-square");
        $("#MiscCheckbox").addClass("fa-check-square");
      } else {
        // Hide the terminal commands.
        showMiscCommands = false;
        $('.miscCmd').fadeOut();
        $("#MiscCheckbox").addClass("fa-square");
        $("#MiscCheckbox").removeClass("fa-check-square");
      }
    });
}


// Splash Only - Animation Sequence
if ( document.location.href.match(/[^\/]+$/)[0] == 'splash.html' ) {

  // Scenes - Delayed elements to appear
  $(document).ready(function()
  {
    // Override the footer to only display "Skip".
    $('#footer').html("<div class='footer-content'><div class='form'><a onclick='continueToPage(true)' class='btn btn-inverse'>&zwnj;Skip&zwnj;</a></div></div>");

    $('#sceneA').show();
    $('#sceneA').jAnimateOnce('fadeIn');
    $('#splash-multilingual').show();
    $('#splash-multilingual').jAnimateOnce('zoomIn');

    setTimeout(function(){ $('#circle1').fadeOut('medium');}, 2000);
    setTimeout(function(){ $('#circle2').fadeOut('medium');}, 2100);
    setTimeout(function(){ $('#circle3').fadeOut('medium');}, 2200);
    setTimeout(function(){ $('#circle4').fadeOut('medium');}, 2300);
    setTimeout(function(){ $('#circle5').fadeOut('medium');}, 2400);

    setTimeout(function(){
      $('#sceneA').show();
      $('#sceneA').fadeOut();
      $('#splash-multilingual').fadeOut('slow');
    }, 2500);

    setTimeout(function(){
      $('#sceneB').show();
      $('#sceneB').jAnimateOnce('zoomIn');
      $('body').addClass('fadeToMenu');
    }, 3000);

    setTimeout(function(){
      $('body').removeClass('fadeToMenu');
      $('body').css('background-color','#f4f4f4');
    }, 4000);

    setTimeout(function(){
      $('#sceneB').fadeOut();
    }, 5000);

    setTimeout(function(){
      continueToPage(false)
    }, 5300);

  });

  // In live sessions, show a "Hello" page instead to introduce ourselves.
  var splashNextPage = 'index'

  function continueToPage(skipped) {
    if ( skipped == true ) {
      $('body').addClass('fadeToMenu');
      $('#sceneA').fadeOut('medium');
      $('#sceneB').fadeOut('medium');
      $('#splash-multilingual').fadeOut('medium');
      setTimeout(function(){
          smoothOut(splashNextPage + '.html');
      }, 500);
    } else {
      smoothOut(splashNextPage + '.html');
    }

  }

}


// Getting Started Only - Index Pane for Selecting Topics
if ( document.location.href.match(/[^\/]+$/)[0] == 'gettingstarted.html' ) {

  function indexOpen() {
    // Is the index already open?
    if ($('#index-menu').is(':visible')) {
      indexClose();
    } else {
      // Open the Index
      $('#index-open').addClass('disabled');
      $('#index-open').prop('disabled', true);
      $("#index-overlay").fadeIn();
      $("#index-menu").show();
      $('#index-menu').jAnimateOnce('fadeInLeft');
    }
  }

  function indexClose() {
    $('#index-open').removeClass('disabled');
    $('#index-open').prop('disabled', false);
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

  // Show initial page and index pane on page load
  changePage('initial','Choose a Topic');
  setTimeout(function() { indexOpen(); }, 500);
  $('#index-open').jAnimateOnce('fadeInDown');

  // Show additional information on the page based on checkbox state.
  $('.dualBootWin').hide();
  $('#showDualBootWin').click(function() {
    if ( $(this).prop('checked') == true ) {
      $('.dualBootWin').fadeIn();
    } else {
      $('.dualBootWin').fadeOut();
    }
  });

  // Graphics Detection
  // Must be executed shortly after page fully loads in order for variables to exist.
  setTimeout(function() {
    $('.graphics-vendor').html(graphicsVendor);
    $('#graphics-pci').html(graphicsGrep);

    // Auto detection alert initially displays "failed".
    if ( graphicsVendor == 'NVIDIA' ) {
      $('#graphics-detected').removeClass('alert-danger');
      $('#graphics-detected').addClass('alert-info');
      $('#graphics-brand').html("&zwnj;NVIDIA Graphics Card Detected.&zwnj;");
      $('#graphics-describe').html("&zwnj;NVIDIA may have drivers for your card that can boost performance for 3D applications and games as well as improved power management.&zwnj;");
      $('#graphics-proprietary').show();
      $('#graphics-open-source').html("<code>nouveau</code> &zwnj;is the open source driver for NVIDIA cards.&zwnj;");
      $('#graphics-nvidia-only').show();

    } else if ( graphicsVendor == "AMD" ) {
      $('#graphics-detected').removeClass('alert-danger');
      $('#graphics-detected').addClass('alert-info');
      $('#graphics-brand').html("&zwnj;AMD Graphics Card Detected.&zwnj;");
      $('#graphics-describe').html("&zwnj;AMD may have drivers for your card that can boost performance for 3D applications and games as well as improved power management.&zwnj;");
      $('#graphics-proprietary').show();
      $('#graphics-open-source').html("<code>radeon</code> &zwnj;is the open source driver for AMD cards.&zwnj;");

    } else if ( graphicsVendor == "Intel" ) {
      $('#graphics-detected').removeClass('alert-danger');
      $('#graphics-detected').addClass('alert-success');
      $('#graphics-brand').html("&zwnj;You're already good to go!&zwnj;");
      $('#graphics-describe').html("&zwnj;Intel's drivers are open source and are maintained in the kernel.&zwnj;");

    } else if ( graphicsVendor == "VirtualBox" ) {
      $('#graphics-detected').removeClass('alert-danger');
      $('#graphics-detected').addClass('alert-info');
      $('#graphics-brand').html("&zwnj;VirtualBox Guest Additions&zwnj;");
      $('#graphics-describe').html("&zwnj;To accelerate graphics performance inside the virtual machine, please install Guest Additions.&zwnj;");

    } else {
      // Obscure graphics chip or something we can't tell.
      $('#graphics-proprietary').show();
      $('.graphics-vendor').html("&zwnj;the manufacturer&zwnj;");
    }
  }, 1000);

  // Expand / Collapse sub-sections to keep it tidy.
  function toggleSub(divID,arrowID) {
    if ( $('#'+divID).is(":visible") ) {
      $('#'+divID).fadeOut();
      $('#'+arrowID).removeClass('fa-chevron-up');
      $('#'+arrowID).addClass('fa-chevron-down');
    } else {
      $('#'+divID).fadeIn();
      $('#'+arrowID).removeClass('fa-chevron-down');
      $('#'+arrowID).addClass('fa-chevron-up');
    }
  }

  // Fetch system specifications if not cached already.
  // Wait a couple of seconds so it doesn't look like application had frozen.
  function init_system_info() {
    $('html').css('cursor','wait')
    setTimeout(function() {
      window.location.href = "cmd://init-system-info";
    }, 1000);
  }

  // Show popovers on hover.
  $(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
  });
  $('[rel=unitsinfo]').popover({
      html : true,
      content: function() {
        return $('#popover_units').html();
      }
  });

}


// Donate Only = Links for donations and spendings per month.
if ( document.location.href.match(/[^\/]+$/)[0] == 'donate.html' ) {

  var today = new Date();
  var cellID = '2014-0';

  // Add a Year = (New Row)
  function addYear(year) {
    $('#donationTable').append('<tr><th style="text-align:center" id="' + year + '">' + year + '</th>');
  }

  // Add a Month = (New Column)
  function addMonth(m,y) {
    cellID = y + '-' + m;
    $('#donationTable tr:last').append('<td id="' + cellID + '" style="text-align:center;"><a href="cmd://link?https://ubuntu-mate.org/blog/ubuntu-mate-' + numToMonth(m) + '-' + y + '-supporters/">' + numToShortMonth(m) + '</a></td>');
  }

  // Add a Blank Month = (New Column, Empty)
  function addBlankMonth(m,y) {
    cellID = y + '-' + m;
    $('#donationTable tr:last').append('<td id="' + cellID + '" style="text-align:center;"></td>');
  }

  // Close the Row
  function endYear() {
    $('#donationTable tr:last').append("</tr>");
  }

  // Convert month number to long/short string.
  // These are used for determining the URL.
  function numToMonth(m) {
    switch (m) {
      case 0:
        return 'january';
        break;
      case 1:
        return 'february';
        break;
      case 2:
        return 'march';
        break;
      case 3:
        return 'april';
        break;
      case 4:
        return 'may';
        break;
      case 5:
        return 'june';
        break;
      case 6:
        return 'july';
        break;
      case 7:
        return 'august';
        break;
      case 8:
        return 'september';
        break;
      case 9:
        return 'october';
        break;
      case 10:
        return 'november';
        break;
      case 11:
        return 'december';
        break;
    }
  }

  function numToShortMonth(m) {
    switch (m) {
      case 0:
        return '&zwnj;Jan&zwnj;';
        break;
      case 1:
        return '&zwnj;Feb&zwnj;';
        break;
      case 2:
        return '&zwnj;Mar&zwnj;';
        break;
      case 3:
        return '&zwnj;Apr&zwnj;';
        break;
      case 4:
        return '&zwnj;May&zwnj;';
        break;
      case 5:
        return '&zwnj;Jun&zwnj;';
        break;
      case 6:
        return '&zwnj;Jul&zwnj;';
        break;
      case 7:
        return '&zwnj;Aug&zwnj;';
        break;
      case 8:
        return '&zwnj;Sep&zwnj;';
        break;
      case 9:
        return '&zwnj;Oct&zwnj;';
        break;
      case 10:
        return '&zwnj;Nov&zwnj;';
        break;
      case 11:
        return '&zwnj;Dec&zwnj;';
        break;
    }
  }

  // Determine if the date is Jan and set to Dec last year.
  function determineLastMonth() {
    lastMonthID = '#' + today.getFullYear() + '-' + (today.getMonth() - 1);

    // Before January?! Then we mean December last year.
    if ( today.getMonth()-1 == -1 ) {
      lastMonthID = '#' +  (today.getFullYear() - 1) + '-11';
    }
    return lastMonthID;
  }

  // Shade Recent Months
  function shadeCells() {
    // Determine current and last month
    currentMonthID = '#' + today.getFullYear() + '-' + today.getMonth();
    lastMonthID = determineLastMonth();

    // Shade today's month, year and show text (as it's a blank cell).
    $(currentMonthID).css('background-color','#87A556');
    $(currentMonthID).css('color','#fff');
    $(currentMonthID).css('font-weight','bold');
    $(currentMonthID).html(numToShortMonth(today.getMonth()));

    currentYearID = '#'+today.getFullYear();
    $(currentYearID).css('background-color','#87A556');
    $(currentYearID).css('color','#fff');
    $(currentYearID).css('font-weight','bold');

    // Lightly shade last month.
    $(lastMonthID).css('background-color','#CBD6BA');
    $(lastMonthID).css('color','#000');
    $(lastMonthID).css('font-weight','bold');

    // Start of new month? Give 3 days grace before showing the link, just to be sure it's unlikely to be a 404.
    if ( today.getDate() <= 3 ) {
      if ( ! today.getMonth()-1 == -1 ) {
        $(lastMonthID).html('<span class="fa fa-clock-o"></span> '+numToShortMonth(today.getMonth()-1));
      } else {
        $(lastMonthID).html('<span class="fa fa-clock-o"></span> '+numToShortMonth(11));
      }
    }
  }

  ////////////////////////////////

  // Donations started at the end of 2014.
  addYear('2014');
  for ( m = 0; m < 10; m++ ) { var y = 2014; addBlankMonth(m,y); }
  addMonth(10,2014);
  addMonth(11,2014);
  endYear();

  // Determine each year's blog posts since 2015
  for (y = 2015; y < today.getFullYear()+1; y++) {
    addYear(y);
    // Determine each month in that year
    for (m = 0; m < 12; m++) {
      if ( today.getFullYear() == y && today.getMonth() < m ) {
        addBlankMonth(m,y);
      } else {
        addMonth(m,y);
      }
    }
    endYear();
    shadeCells();
  }

}


// Entering Software Only Mode
if ( document.location.href.match(/[^\/]+$/)[0] == 'software-only.html' ) {
    $('html').css('cursor','wait')
}

