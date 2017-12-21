#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2017 Luke Horwell <luke@ubuntu-mate.org>
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
    run_js = variables["objects"]["run_js"]
    pref = variables["objects"]["pref"]

    # Skip splash
    if pref.read("skip_splash", False):
        _go_to_next_page(variables)

    # Load SVG tags directly into page
    with open(os.path.join(variables["data_path"], "img/welcome/triangles.svg"), "r") as f:
        svg_data = f.read().replace("\n", "").replace("  ", "")
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


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]



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
