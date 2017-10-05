function runSplash() {
    var container = $("#triangles");
    var triangles = $("#triangles svg path");
    triangles.hide();
    triangles.each(function() {
        $(this).css({fill: getRandomGrey()});
    });
    container.show();
    animateSplash();
}

var splashSpeed = 750;
var splashFrameDelay = 100;

function animateSplash() {
    setTimeout(function() {
        $(".ani1").fadeIn(splashSpeed);
        $("#splash-logo").addClass("in").show();
        setTimeout(function() {
            $(".ani2").fadeIn(splashSpeed);
            setTimeout(function() {
                $(".ani3").fadeIn(splashSpeed);
                setTimeout(function() {
                    $(".ani4").fadeIn(splashSpeed);
                    setTimeout(function() {
                        $(".ani5").fadeIn(splashSpeed);
                        setTimeout(function() {
                            $(".ani6").fadeIn(splashSpeed);
                            $("#header").show().jAnimateOnce("fadeInDown");
                            $("#footer").show().jAnimateOnce("fadeInUp");
                            setTimeout(function() {
                                $(".ani7").fadeIn(splashSpeed);
                                $("#splash-text").addClass("in").show();
                                setTimeout(function() {
                                    $("#splash-logo").addClass("out");
                                    $("#splash-text").addClass("out");
                                    setTimeout(function() {
                                        continueToPage();
                                    }, 1000);
                                }, 3000);
                            }, splashFrameDelay);
                        }, splashFrameDelay);
                    }, splashFrameDelay);
                }, splashFrameDelay);
            }, splashFrameDelay);
        }, splashFrameDelay);
    }, splashFrameDelay);
}

function getRandomGrey() {
    var colours = ["#565656", "#494949", "#606060", "#585858", "#464646", "#383838", "#5A5A5A"]
    var colour = colours[Math.floor(Math.random()*colours.length)];
    return colour;
}
