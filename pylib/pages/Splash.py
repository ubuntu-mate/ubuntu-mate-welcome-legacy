#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2017-2018 Luke Horwell <luke@ubuntu-mate.org>
#

"""
Welcome Page: Splash

Shown to users as soon as they start the application.
"""

from .. import Common
from time import sleep
import os
import random

_ = Common.setup_translations(__file__, "ubuntu-mate-welcome")


def page_enter(variables):
    """
    Triggered upon opening the page.
    """
    update_page = variables["objects"]["update_page"]
    change_page = variables["objects"]["change_page"]
    dbg = variables["objects"]["dbg"]
    run_js = variables["objects"]["run_js"]
    pref = variables["objects"]["pref"]

    # Jump to a different page
    override_initial_page = variables["override_initial_page"]
    if override_initial_page:
        dbg.stdout("Jumping to page: " + override_initial_page, dbg.action, 1)
        change_page(override_initial_page)
        return

    # Skip splash
    if pref.read("skip_splash", False):
        _go_to_next_page(variables)
        return

    # Load SVG tags directly into page
    with open(os.path.join(variables["data_path"], "img/welcome/triangles.svg"), "r") as f:
        svg_data = f.read().replace("\n", "").replace("  ", "")
    update_page("content", "show")
    update_page("content", "append", "<div id='splash'></div>")
    update_page("content", "append", '<div id="triangles" style="display:none">{0}</div>'.format(svg_data))
    update_page("content", "append", '<img id="splash-logo" style="display:none" src="img/welcome/ubuntu-mate-icon.svg"/>')
    update_page("content", "append", '<div id="splash-text" style="display:none">{0}</div>'.format(_("Welcome")))

    update_page("#triangles", "hide")
    update_page("#triangles svg path", "hide")
    run_js("$('#triangles svg path').each(function(){ $(this).css({fill: getRandomGrey() }) });")
    update_page("#triangles", "fadeIn")

    splash_speed = 750
    splash_sleep = 0.1

    for x in range(0,7):
        update_page(".ani" + str(x), "fadeIn", str(splash_speed))

        if x == 6:
            update_page("header", "show")
            update_page("footer", "show")
            update_page("header", "addClass", "in")
            update_page("footer", "addClass", "in")

        sleep(splash_sleep)

    update_page("#splash-logo", "addClass", "in")
    update_page("#splash-logo", "show")
    sleep(0.5)

    update_page("#splash-text", "addClass", "in")
    update_page("#splash-text", "show")
    sleep(3)

    update_page("#splash-logo", "addClass", "out")
    update_page("#splash-text", "addClass", "out")
    sleep(1)

    _go_to_next_page(variables)
    return


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]
    for element in ["header", "footer"]:
        update_page(element, "addClass", "in")
    update_page("body", "removeClass", "splash")
    update_page("content", "fadeOut", variables["page_fade_speed"])
    sleep(variables["page_fade_wait"])
    for element in ["header", "footer"]:
        update_page(element, "show")


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]
    pass

def _go_to_next_page(variables):
    """
    When the splash animation finishes, where to go next?
    """
    pref = variables["objects"]["pref"]
    change_page = variables["objects"]["change_page"]

    # Show the relevant screen based on where Welcome was started
    session_type = variables["session_type"]
    if session_type == "live":
        change_page("welcome_live")
    elif session_type == "guest":
        change_page("welcome_guest")
    else:
        change_page("main_menu")
