//
// JavaScript specific functions for Welcome
//

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
