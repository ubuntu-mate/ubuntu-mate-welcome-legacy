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
  // Animate navigation elements on page load
  if ( current_page != 'splash-boutique.html' ) {
    if ( current_page != 'software.html') {
      $('#menu-button').show();
      $('#menu-button').jAnimateOnce('pageIn');
      $('#navigation-title').show();
      $('#navigation-title').jAnimateOnce('pageIn');
    }
  }

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

///////////////////////////////////////////////////////////////

// Main Menu Only = Animation
if ( current_page == 'index.html' ) {

  // Animate elements of the page
  $('.main-menu-text').fadeIn('medium');
  $('#open-at-start').jAnimateOnce('fadeIn');
  $('#mate-blur').jAnimateOnce('zoomIn');
  $('#mate-blur').show();

  function exitMenu(target) {
      // Show a "wait" cursor for the Software page, as there is a slight delay.
      if ( target == 'software.html' ) {
          setCursorBusy()
      }

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


// Software Page Only = Categories for Apps
if ( current_page == 'software.html' ) {

    // Do not show navigation elements
    $('#menu-button').hide();
    $('#navigation-title').hide();
    $('#navigation-right').hide();

    // Initial variables.
    var currentCategory = '#boutique-loading';
    var hideNonFree = false;
    var system_info = '';

    // Switch to another category.
    function switchCategory(now, next, subtitle, hideCheckmarks=false) {
        // Smoothly fade subtitle
        changeSubtitle(subtitle);
        $('#content').animate({ scrollTop: 0 }, 500)

        // Remove any other current page highlights
        $('#navigation-queue').removeClass('active');
        $('#navigation-search').removeClass('active');
        $('#navigation-news').removeClass('active');
        $('#navigation-prefs').removeClass('active');

        // Fade in non-free toggle as it starts hidden, except on the Misc. page,
        // where it's replaced by a command visibility toggle.
        if ( next == '#Misc' ) {
          smoothFade('#non-free-toggle','#show-misc-cmds');
        } else if ( hideCheckmarks == true ) {
          $('#non-free-toggle').fadeOut();
          $('#show-misc-cmds').fadeOut();
        } else {
          smoothFade('#show-misc-cmds','#non-free-toggle');
        }

        // Animate out, then animate in next category.
        $(now).fadeOut();
        setTimeout(function() {
          $(now).hide();
          currentCategory = next;
          $(next).fadeIn();
        }, 250);

        // Show all apps again, in case the previous page was filtered.
        $('.app-entry').fadeIn();

        // Reset filters
        selected_filter = 'none';
        $('.filter-box').val('none');
        applyFilter();

        return currentCategory;
    }

    // Display Boutique tab tooltips properly on the page.
    $('[data-toggle=tooltip]').tooltip({container: 'body'});

    // A category tab is clicked.
    function changeCategoryTab(id,humanText) {
      switchCategory(currentCategory, id, humanText);
      $('#categoryHover').fadeOut()
    }

    function jumpOneClickServers(appno) {
      // Python passes 'server_string' variable to allow translation.
      changeCategoryTab('#Servers', server_string);
      $('#ServersBtn').tab('show');
      $('#content').animate({ scrollTop: 0 }, 100)

      // WORKAROUND = Cannot use ' or " strings, use numbers to get target div ID:
      if ( appno == 1 ) {  targetDiv = 'minecraft-server';  }
      if ( appno == 2 ) {  targetDiv = 'x2go-server';  }
      if ( appno == 3 ) {  targetDiv = 'murmur';  }

      setTimeout(function(){
          $('#content').animate({
              scrollTop: $('#'+targetDiv).offset().top - 100
          }, 1000);
      }, 1000);
    }

    // Show the popover/tooltips on hover
    $(document).ready(function() {
      $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });

    // Filtering applications by subcategory and/or proprietary software.
    selected_filter = 'none';

    $("select").change(function(){
        selected_filter = $(this).val();
        applyFilter();
    });

    function applyFilter() {
        cmd('filter-apps?' + selected_filter + '?');
    }

    function toggleNonFree() {
        cmd('filter-apps?' + selected_filter + '?toggle');
    }

    // Featured Grid - Set classes to create a semi-circle fade effect.
    function initGrid() {
        $('#appIcon1').addClass('grid-outer');
        $('#appIcon2').addClass('grid-outer');
        $('#appIcon3').addClass('grid-outer');
        $('#appIcon4').addClass('grid-outer');
        $('#appIcon5').addClass('grid-outer');
        $('#appIcon8').addClass('grid-outer');
        $('#appIcon9').addClass('grid-outer');
        $('#appIcon12').addClass('grid-outer');
        $('#appIcon13').addClass('grid-outer');
        $('#appIcon14').addClass('grid-outer');
        $('#appIcon15').addClass('grid-outer');
        $('#appIcon16').addClass('grid-outer');

        $('#appIcon6').addClass('grid-inner');
        $('#appIcon7').addClass('grid-inner');
        $('#appIcon10').addClass('grid-inner');
        $('#appIcon11').addClass('grid-inner');

        // Gently fade the icons into view.
        setTimeout(function(){ $('#appIcon1').removeClass('grid-hidden'); }, 800 );

        setTimeout(function(){ $('#appIcon2').removeClass('grid-hidden'); }, 850 );
        setTimeout(function(){ $('#appIcon5').removeClass('grid-hidden'); }, 850 );
        setTimeout(function(){ $('#appIcon6').removeClass('grid-hidden'); }, 850 );

        setTimeout(function(){ $('#appIcon3').removeClass('grid-hidden'); }, 900 );
        setTimeout(function(){ $('#appIcon6').removeClass('grid-hidden'); }, 900 );
        setTimeout(function(){ $('#appIcon9').removeClass('grid-hidden'); }, 900 );

        setTimeout(function(){ $('#appIcon4').removeClass('grid-hidden'); }, 950 );
        setTimeout(function(){ $('#appIcon7').removeClass('grid-hidden'); }, 950 );
        setTimeout(function(){ $('#appIcon10').removeClass('grid-hidden'); }, 950 );
        setTimeout(function(){ $('#appIcon13').removeClass('grid-hidden'); }, 950 );

        setTimeout(function(){ $('#appIcon8').removeClass('grid-hidden'); }, 1000 );
        setTimeout(function(){ $('#appIcon11').removeClass('grid-hidden'); }, 1000 );
        setTimeout(function(){ $('#appIcon14').removeClass('grid-hidden'); }, 1000 );

        setTimeout(function(){ $('#appIcon12').removeClass('grid-hidden'); }, 1050 );
        setTimeout(function(){ $('#appIcon15').removeClass('grid-hidden'); }, 1050 );

        setTimeout(function(){ $('#appIcon16').removeClass('grid-hidden'); }, 1100 );
    }

    // Misc Tab - Show commands if user wishes to know them.
    var showMiscCommands = false;
    $('.miscCmd').hide();

    $('#show-misc-cmds').click(function() {
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

    // Smooth transition for footer.
    $('#footer-left').hide();
    $('#footer-left').fadeIn();

    // Toggling right navigation "tabs"
    function resetNavTabs() {
      $('#tabs li').removeClass('active');
      $('#non-free-toggle').fadeOut();
      $('#show-misc-cmds').fadeOut();
    }

    // Toggling to show the Boutique News
    function showNews(subtitle) {
      switchCategory(currentCategory, '#News', subtitle, true);
      resetNavTabs();
      $('#navigation-news').addClass('active');
    }

    // Toggling to show the Search Page
    function showSearch(subtitle) {
      switchCategory(currentCategory, '#Search', subtitle, true)
      resetNavTabs();
      $('#navigation-search').addClass('active');
      $('#search-results').html('');
      $('#search-results').hide();
      $('#search-empty').hide();
      $('#search-total').hide();
      $('#search-terms').val('');
    }

    // Perform a search
    function searchNow() {
      keywords = $('#search-terms').val();
      cmd('search?' + keywords)
    }

    // Search again but include non-free matches.
    function searchAgainNonFree() {
      toggleNonFree()
      searchNow()
    }

    // Toggling to show the Preferences page
    function showPrefs(subtitle) {
      switchCategory(currentCategory, '#Preferences', subtitle, true)
      resetNavTabs();
      $('#navigation-prefs').addClass('active');
    }

    // Toggling to show the Queue page
    function showQueue(subtitle) {
      switchCategory(currentCategory, '#Queue', subtitle, true)
      resetNavTabs();
      $('#navigation-queue').addClass('active');
    }

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


// Splash for Entering Boutique
if ( current_page == 'splash-boutique.html' ) {
    setCursorBusy();
    setTimeout(function() {
      $('#boutique-splash').jAnimate('zoomOutInverse');
    }, 1000);

    $('#Text1').css('opacity','0');
    $('#Text2').css('opacity','0');
    $('#Text1').show();
    $('#Text2').show();

    setTimeout(function(){
      $('#Text1').hide();
      $('#Text1').css('opacity','');
      $('#Text1').fadeIn(750);
    }, 100);

    setTimeout(function(){
      $('#Text2').hide();
      $('#Text2').css('opacity','');
      $('#Text2').fadeIn(750);
    }, 200);
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

    // Smoothly fade between topics
    $('.topicContents').fadeOut();
    $('#current-topic').fadeOut();
    $('#current-icon').fadeOut();
    $('#bottom-navigation').fadeOut();

    setTimeout(function() {
      $('#current-topic').html(title);
      $('#current-topic').fadeIn();
      $('#current-icon').fadeIn();
      $(id).fadeIn();

      $("#current-icon").removeClass();
      $("#current-icon").addClass("fa").addClass(icon);

      // Hide bottom navigation if topics page.
      if ( id == "#initial" ) {
        $('#bottom-navigation').fadeOut();
      } else {
        $('#bottom-navigation').fadeIn();
      }

      // Update prev/next button states
      if ( do_not_update_btn_state == null ) {
        prevPage = $(id).data("prev");
        prevText = $('#'+prevPage).data("title");
        nextPage = $(id).data("next");
        nextText = $('#'+nextPage).data("title");

        if ( prevPage == "none" ) {
          $("#topic-prev").addClass("disabled");
          $("#bottom-topic-prev").hide();
        } else {
          $("#topic-prev").removeClass("disabled");
          $("#bottom-topic-prev").show();
          $("#bottom-topic-prev").attr("title", prevText);
        }

        if ( nextPage == "none" ) {
          $("#topic-next").addClass("disabled");
          $("#bottom-topic-next").hide();
        } else {
          $("#topic-next").removeClass("disabled");
          $("#bottom-topic-next").show();
          $("#bottom-topic-next").attr("title", nextText);
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
    $(".sub-collapse > span").addClass('fa-chevron-down').removeClass('fa-chevron-up');
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
        $('#donationTable tr:last').append('<td id="' + cellID + '" style="text-align:center;"><a onclick="cmd(\'link?https://ubuntu-mate.org/blog/ubuntu-mate-' + numToMonth(m) + '-' + y + '-supporters/\')">' + numToShortMonth(m) + '</a></td>');
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

