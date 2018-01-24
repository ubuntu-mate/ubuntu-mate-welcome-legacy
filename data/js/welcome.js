//
// JavaScript specific functions for Ubuntu MATE Welcome
//
//--------------------------------------------------------------------
// General
//--------------------------------------------------------------------
// HTML/JS to Python
function cmd(cmd) {
    document.title = cmd;
}

// Jump to the top of page
function backToTop() {
    $("content").animate({
        scrollTop: 0
    }, 600);
    $("#scroll-top").addClass("active");
    return false;
};

// Bind ESC key (27)
$("body").bind("keypress", function(e) {
    if ( e.keyCode == 27 ) {

    }
});

function getRandomGrey() {
    var colours = ["#565656", "#494949", "#606060", "#585858", "#464646", "#383838", "#5A5A5A"]
    var colour = colours[Math.floor(Math.random()*colours.length)];
    return colour;
}

//--------------------------------------------------------------------
// Donate Page
//--------------------------------------------------------------------
// Migration of original code prior to Python page rewrite
function initDonateTable(month_short_string_dict, month_long_string_dict) {
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
        return month_long_string_dict[m];
    }

    // These shorthand month names are seen to the user in the table.
    function numToShortMonth(m) {
        return month_short_string_dict[m];
    }

    // Determine if the date is Jan and set to Dec last year.
    function determineLastMonth() {
        lastMonthID = '#' + today.getFullYear() + '-' + (today.getMonth() - 1);

        // Before January?! Then we mean December last year.
        if ( today.getMonth() - 1 == -1 ) {
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

        // Start of new month? Give 5 days grace before showing the link, just to be sure it's unlikely to be a 404.
        if ( today.getDate() <= 5 ) {
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
    for ( m = 0; m < 10; m++ ) {
        var y = 2014;
        addBlankMonth(m,y);
    }
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
