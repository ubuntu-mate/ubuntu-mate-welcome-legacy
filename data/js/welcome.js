// Which page?
current_page = document.location.href.match(/[^\/]+$/)[0];

// Show an error dialog when JavaScript errors occur.
$(window).on("error", function(evt) {
    // Gets JavaScript Event
    var e = evt.originalEvent;
    friendly_txt = "Oops! Welcome encountered an internal error.\n\nPlease tell the Ubuntu MATE Developers so this can fixed right away.";
    if (e.message) {
        alert(friendly_txt + "\n\nError:\n\t" + e.message + "\nLine:\n\t" + e.lineno + "\nFile:\n\t" + e.filename);
    } else {
        alert(friendly_txt + "\n\nError:\n\t" + e.type + "\nElement:\n\t" + (e.srcElement || e.target));
    }
});

// Pass commands to Python
function cmd(instruction) {
    document.title = instruction;
    setTimeout(function(){
        document.title = 'null';
    }, 10);
}

// Global across all pages
$(window).load(function() {
    // Smoothly fade into the page.
    $('.entire-page-fade').jAnimate('pageIn');
    $('.entire-page-fade').show();
    $('#navigation-right').hide();
    $('#navigation-right').fadeIn('medium');
});

// Smoothly fade out of the page.
function smoothPageFade(target_href) {
    $('.entire-page-fade').jAnimate('pageOut');
    $('#navigation-title').fadeOut('medium');
    $('#navigation-right').fadeOut('medium');
    $('.navigation-button').fadeOut('medium');
    setTimeout(function(){
        window.location.href = target_href;
    }, 400);
}

// Back to the top function
function backToTop() {
    $("#content").animate({
        scrollTop: 0
    }, 600);
    $('#scroll-top').addClass('active');
    return false;
};

// When page first opens
$(document).ready(function() {
  $('#menu-button').show();
  $('#menu-button').jAnimateOnce('pageIn');
  $('#navigation-title').show();
  $('#navigation-title').jAnimateOnce('pageIn');

  // Show back to top button on page scroll
  $('#content').scroll(function () {
      if ($(this).scrollTop() > 90) {
          $('#scroll-top').fadeIn();
          $('#scroll-top-always-show').removeClass('disabled');
      } else {
          $('#scroll-top').fadeOut();
          $('#scroll-top').removeClass('active');
          $('#scroll-top-always-show').addClass('disabled');
      }
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
  $('#navigation-sub-title').fadeOut('fast');
  setTimeout(function() {
    $('#navigation-sub-title').html(textToDisplay);
    $('#navigation-sub-title').fadeIn('fast');
  }, 200);
}

// For pages that depend on an internet connection, but Welcome couldn't connect.
function reconnectRetry() {
  cmd('checkInternetConnection');
  if ( ! $('#reconnectFailed').is(':visible') ) {
    $('#reconnectFailed').fadeIn();
  } else {
    $('#reconnectFailed').jAnimateOnce('flash');
  }
}

// Dynamically set the cursor,
function setCursorBusy() {
  $('html').addClass('cursor-wait');
  $('body').addClass('cursor-wait');
  $('a').addClass('cursor-wait');
}

function setCursorNormal() {
  $('html').removeClass('cursor-wait');
  $('body').removeClass('cursor-wait');
  $('a').removeClass('cursor-wait');
}

// Keyboard shortcuts
$('body').bind('keypress', function(e) {
	if ( e.keyCode == 27 ) {  // ESC
    if ( current_page != "index.html" ) {
      smoothPageFade("index.html")
    }
	}
});

///////////////////////////////////////////////////////////////

// Main Menu Only = Animation
if ( current_page == 'index.html' ) {

  // Animate elements of the page
  $('.main-menu-text').fadeIn('medium');
  $('#mate-blur').jAnimateOnce('zoomIn');
  $('#mate-blur').show();

  function exitMenu(target) {
      $("#open-at-start").fadeOut();
      $('#mate-blur').jAnimateOnce('zoomOut');
      smoothPageFade(target)
  }

  // Enable tooltips
  $(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
  });

  // Sssh... You found the little secrets! ;)
  //// Logo starts to animate after a minute.
    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('tada');
    }, 60000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('flip');
    }, 60000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('rotateOut');
    }, 70000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('rotateIn');
    }, 71000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('rollOut');
    }, 80000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('rollIn');
    }, 81000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('zoomOut');
    }, 90000);

    setTimeout(function(){
      $('#main-menu-logo').jAnimateOnce('zoomIn');
    }, 91000);

}


// Introduction/Features = Animation
if ( current_page == 'introduction.html' || current_page == 'features.html' ) {
  new WOW().init();
  new WOW({
    scrollContainer: '#content'
  }).init();
}

// Splash Only - Animation Sequence
if ( current_page == 'splash.html' ) {

  // Scenes - Delayed elements to appear
  $(document).ready(function()
  {
    $('body').show();
    $('#splash-logo').show();
    $('#splash-logo').jAnimateOnce('entrance');
    $('#MATE-Logo').show();
    $('#MATE-Logo').jAnimateOnce('mateRoll');

    $('#MATE-Text1').css('opacity','0');
    $('#MATE-Text2').css('opacity','0');
    $('#MATE-Text1').show();
    $('#MATE-Text2').show();

    setTimeout(function(){
      $('#MATE-Text1').hide();
      $('#MATE-Text1').css('opacity','');
      $('#MATE-Text1').fadeIn(1500);
    }, 250);

    setTimeout(function(){
      $('#MATE-Text2').hide();
      $('#MATE-Text2').css('opacity','');
      $('#MATE-Text2').fadeIn(1500);
    }, 600);

    setTimeout(function(){
      $('#header').show();
      $('#footer').show();
      $('#header').jAnimateOnce('fadeInDown');
      $('#footer').jAnimateOnce('fadeInUp');
    }, 2000);

    setTimeout(function(){
      $('#splash-logo').hide();
      $('#skip-splash').fadeOut();
      if ( quick_splash == true ) {
        $('#white-start').fadeOut('fast');
        continueToPage(false)
      } else {
        $('#splash-welcome').show();
        $('#splash-welcome').jAnimateOnce('zoomInInverse');
        $('#white-start').fadeOut('slow');
      }
    }, 3000);

    setTimeout(function(){
      $('#splash-welcome').fadeOut();
    }, 4500);

    setTimeout(function(){
      continueToPage(false)
    }, 5000);

  });

  // In live sessions, show a "Hello" page instead to introduce ourselves.
  var splashNextPage = 'index'

  function continueToPage(skipped) {
    if ( skipped == true ) {
      $('#splash-logo').fadeOut('fast');
      $('#white-start').fadeOut('fast');
      $('#header').fadeIn('fast');
      $('#footer').fadeIn('fast');
      setTimeout(function(){
          smoothPageFade(splashNextPage + '.html');
      }, 100);
    } else {
      smoothPageFade(splashNextPage + '.html');
    }
  }
}


// Getting Started Only - Index Pane for Selecting Topics
if ( current_page == 'gettingstarted.html' ) {
  var nextPage = "initial";
  var prevPage = "initial";

  function changePage(id, do_not_update_btn_state) {
    // 'id' is one used for <div>.
    var id = '#' + id;
    var title = $(id).data("title");
    var icon  = $(id).data("icon");

    if ( id == "#none" ) {
      return
    }

    // Smoothly fade between topics
    $('.topicContents').fadeOut();
    $('#current-topic').fadeOut();
    $('#current-icon').fadeOut();

    setTimeout(function() {
      $('#current-topic').html(title);
      $('#current-topic').fadeIn();
      $('#current-icon').fadeIn();
      $(id).fadeIn();

      $("#current-icon").removeClass();
      $("#current-icon").addClass("fa").addClass(icon);

      // Update prev/next button states
      if ( do_not_update_btn_state == null ) {
        prevPage = $(id).data("prev");
        prevText = $('#'+prevPage).data("title");
        nextPage = $(id).data("next");
        nextText = $('#'+nextPage).data("title");

        if ( prevPage == "none" ) {
          $("#topic-prev").addClass("disabled");
        } else {
          $("#topic-prev").removeClass("disabled");
        }

        if ( nextPage == "none" ) {
          $("#topic-next").addClass("disabled");
        } else {
          $("#topic-next").removeClass("disabled");
        }

        // Gather system specs if applicable.
        if ( id == "#specs" ) {
          InitSystemInfo();
        }
      }
    }, 500);
  }

  // On page entry, animate the topic subheading.
  $('#topic-subheading').show().jAnimateOnce('fadeInDown');
  $("#topic-subheading").children().fadeIn('fast');

  function exitPage() {
    $("#topic-subheading").children().fadeOut('fast');
    $('#topic-subheading').slideUp();
    smoothPageFade('index.html');
  }

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
    $('.graphics-pci').html(graphicsGrep);

    // Auto detection alert initially displays "failed".
    if ( graphicsVendor == 'NVIDIA' ) {
      $('.graphics-nvidia').show()
      $('.graphics-unknown').hide()
      $('#graphics-open-driver-name').html('nouveau');
      $('#graphics-proprietary').show();

    } else if ( graphicsVendor == "AMD" ) {
      $('.graphics-amd').show()
      $('.graphics-unknown').hide()
      $('#graphics-open-driver-name').html('radeon');
      //~ $('#graphics-proprietary').show();

    } else if ( graphicsVendor == "Intel" ) {
      $('.graphics-intel').show()
      $('.graphics-unknown').hide()

    } else if ( graphicsVendor == "VirtualBox" ) {
      $('.graphics-vbox').show()
      $('.graphics-unknown').hide()

    } else {
      // Obscure graphics chip or something we can't tell.
      $('#graphics-proprietary').show();
    }
  }, 1000);

  // Expand / Collapse sub-sections to keep it tidy.
  function toggleSub(divID, arrowID) {
    $(".sub-collapse > h3 > span").addClass('fa-chevron-down').removeClass('fa-chevron-up');
    alreadyOpen = $("#"+divID).is(":visible");
    $(".drivers-section").slideUp("fast");
    if ( alreadyOpen == false ) {
      $("#"+divID).slideDown('fast');
      $('#'+arrowID).removeClass('fa-chevron-down');
      $('#'+arrowID).addClass('fa-chevron-up');
    }
  }

  // Fetch system specifications if not cached already.
  function InitSystemInfo() {
    setCursorBusy()
    // Wait a second to allow a smooth fade animation.
    setTimeout(function() {
      cmd("init-system-info");
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
if ( current_page == 'donate.html' ) {

  // Some translatable short hand strings are passed via Python.
  // The slight delay allows these variables to be loaded to JS before building the supporters table.
  setTimeout(function() {
      var today = new Date();
      var cellID = '2014-0';

      // Add a Year = (New Row)
      function addYear(year) {
        $('#donationTable').append('<tr><th style="text-align:center" id="' + year + '">' + year + '</th>');
      }

      // Add a Month = (New Column)
      function addMonth(m,y) {
        cellID = y + '-' + m;
        $('#donationTable tr:last').append('<td id="' + cellID + '" style="text-align:center;"><button class="link" onclick="cmd(\'link?https://ubuntu-mate.org/blog/ubuntu-mate-' + numToMonth(m) + '-' + y + '-supporters/\')">' + numToShortMonth(m) + '</button></td>');
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

      // These shorthand month names are seen to the user in the table.
      function numToShortMonth(m) {
        switch (m) {
          case 0:
            return short_jan;
            break;
          case 1:
            return short_feb;
            break;
          case 2:
            return short_mar;
            break;
          case 3:
            return short_apr;
            break;
          case 4:
            return short_may;
            break;
          case 5:
            return short_jun;
            break;
          case 6:
            return short_jul;
            break;
          case 7:
            return short_aug;
            break;
          case 8:
            return short_sep;
            break;
          case 9:
            return short_oct;
            break;
          case 10:
            return short_nov;
            break;
          case 11:
            return short_dec;
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
  }, 1000);

}

