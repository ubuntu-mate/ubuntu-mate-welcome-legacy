#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv2.
#
# Copyright (C) 2017-2018 Luke Horwell <code@horwell.me>
#

"""
Welcome Page: Main Menu

The main menu for the application.
"""

from .. import Common
from time import sleep
import os
import sys

_ = Common.setup_translations(__file__, "ubuntu-mate-welcome")


def page_enter(variables):
    """
    Triggered upon opening the page.
    """
    update_page = variables["objects"]["update_page"]
    change_page = variables["objects"]["change_page"]
    pref = variables["objects"]["pref"]
    ui = variables["objects"]["ui"]
    fade_speed = variables["page_fade_speed"]

    # === Header ===
    update_page("#header-left", "html", "<h1 id='header-title'>{0}</h1>".format(_("Main Menu")))
    update_page("#header-left", "fadeIn", fade_speed)

    # === Content ===
    content_html = "<div id='menu-logo'>"
    #~ content_html += "<img id='um-logo' src='img/welcome/ubuntu-mate-icon.svg' />"
    content_html += "<img id='um-ubuntu-text' src='img/welcome/logo-text-ubuntu.svg' />"
    content_html += "<img id='um-MATE-text' src='img/welcome/logo-text-MATE.svg' />"
    content_html += "<div id='um-version'>{0}</div>".format(variables["os_version"])
    content_html += "</div>"

    # Determine text to show.
    if pref.read("opened_times", 0) < 3:
        #. Shown when application has been opened for the first few times.
        intro_text = _("Choose an option to discover your new operating system.")
    else:
        #. Shown when application has been opened in the past.
        intro_text = _("Where would you like to go?")

    content_html += "<h4 id='menu-text'>" + intro_text + "</h4>"

    # Prepare columns of page
    left_column = "<div class='left-column'>"
    middle_column = "<div class='middle-column'>"
    right_column = "<div class='right-column'>"

    # Main Menu buttons
    main_row = "<div class='row main-menu'>"
    main_row += "<div class='left'>" + ui.print_button(_("Getting Started"), "change-page?getting_started", "img/fa5/coffee.svg", "normal", _("Topics about best practices setting up after a fresh installation")) + "</div>"
    main_row += "<div class='middle'>" +ui.print_button(_("Customise"), "change-page?customise", "img/fa5/paint-brush.svg", "normal", _("Make Ubuntu MATE look and feel your way")) + "</div>"
    main_row += "<div class='right'>" +ui.print_button(_("Software Boutique"), "start-boutique", "img/welcome/boutique-mono.svg", "normal", _("Find software that works great on Ubuntu MATE")) + "</div>"

    left_column += ui.print_button(_("Introduction"), "change-page?introduction", "img/fa5/graduation-cap.svg", "normal", _("Get a brief introduction to the world of Ubuntu MATE"))
    left_column += ui.print_button(_("Features"), "change-page?features", "img/fa5/tasks.svg", "normal", _("Find out what things you can do!"))

    middle_column += ui.print_button(_("Community"), "change-page?community", "img/fa5/users.svg", "normal", _("Connect with other Ubuntu MATE users for feedback and help"))
    middle_column += ui.print_button(_("Get Involved"), "change-page?get_involved", "img/fa5/hand.svg", "normal", _("Find out how you can help the project grow"))

    right_column += ui.print_button(_("Shop"), "change-page?shop", "img/fa5/shopping-cart.svg", "normal", _("Style yourself while finanically helping Ubuntu MATE"))
    right_column += ui.print_button(_("Donate"), "change-page?donate", "img/fa5/heart.svg", "normal", _("Find out how a little bit goes a long way"))

    # Add end tags for columns and append to content HTML buffer
    for html in [main_row, left_column, middle_column, right_column]:
        html += "</div>"
        content_html += html

    update_page("content", "html", content_html)
    update_page("content", "fadeIn", fade_speed)

    # === Footer ===
    #~ update_page("body", "append", "<script>cmd('test')</script>")


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]
    Common.page_exit_global(variables)


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]

    #~ if cmd == "test":
        #~ return True
