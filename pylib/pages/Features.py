#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <luke@ubuntu-mate.org>
#               2015-2016 Martin Wimpress <code@flexion.org>
#               2015, Larry Bushey
#

"""
Welcome Page: Features

Informs about what you can do with Ubuntu MATE.
"""

from .. import Common
from time import sleep
import os

_ = Common.setup_translations(__file__, "ubuntu-mate-welcome")


def page_enter(variables):
    """
    Triggered upon opening the page.
    """
    update_page = variables["objects"]["update_page"]
    change_page = variables["objects"]["change_page"]
    ui = variables["objects"]["ui"]

    content = ''
    content += '<div id="content" class="container-fluid entire-page-fade" tabindex="1">' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span12">' \
                '<h2>' + _("Modern and Full-Featured") + '</h2>' \
                '<p>'
    content += _("Ubuntu MATE is a modern computer operating system, with an" \
                "attractive and easy to understand user interface. Its update" \
                "manager keeps not only the operating system itself, but all of its" \
                "installed applications updated to the current release. The" \
                "operating system is more secure, and better supported than" \
                "operating systems that come pre-installed on most home computer" \
                "hardware today.")
    content += '</p>' \
                '</div>' \
                '</div>'

    content += '<h3 class="wow fadeIn">' + _("Pre-Configured Yet Flexible") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/control-centre.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Using Ubuntu MATE provides you with the freedom to run a" \
                    "complete, full-featured operating system, pre-configured with" \
                    "most, if not all, of the applications you will need for your daily" \
                    "computing - or to change anything about the way it looks, the way" \
                    "it works, or the applications it runs to suit your taste.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \

    content += '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Built-In Security") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/system-software-update.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Ubuntu MATE is designed with security in mind. Unlike operating" \
                    "systems that update only once a month, Ubuntu MATE receives" \
                    "updates continuously. The updates include security patches for" \
                    "Ubuntu MATE and all of its components. Security updates for all of" \
                    "its installed applications are also provided on the same schedule." \
                    "This ensures that you have the latest protection for all of your" \
                    "computer's software -- as soon as it's available!")
    content += '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">'

    content += '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/security.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Ubuntu MATE can get viruses and other infections... but it" \
                    "doesn't. Rapid and timely updates ensure that there are very few," \
                    "if any threats to Linux systems like Ubuntu MATE that persist in" \
                    "the wild. In reality, there have been very few \"public\" infections" \
                    "in the last 10 years that can affect Ubuntu MATE. They are no" \
                    "longer a threat to anyone installing or using a modern Linux" \
                    "distribution today. Ubuntu MATE is designed to make it difficult" \
                    "for viruses, root kits and other malware to be installed and run" \
                    "without conscious intervention by you, the user. Even if you do" \
                    "accidentally invite in an infection, chances are it's designed to" \
                    "attack Windows and won't do much, if any damage to Ubuntu MATE.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">'

    content += '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/system-config-securitylevel.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Another significant security feature of Ubuntu MATE is that its" \
                    "users are not administrators by default. Administrators (\"root\"" \
                    "users) on any computer system have permission to do anything they" \
                    "want, including the ability to damage the system.")
    content += '</p>' \
                '<p>'
    content += _("For example, other operating systems look at the name of a file" \
                    "to determine which program should open it, then immediately" \
                    "attempt to open it. That design makes it easy for an intruder to" \
                    "attack a computer. Ubuntu MATE opens a file based on what the file" \
                    "is, not based on its name. So even if a malicious program" \
                    "disguises its identity by using the name \"Last Will and" \
                    "Testament.txt\" Ubuntu MATE will recognize the file as a program." \
                    "The system provides a warning that the file is not a text file," \
                    "but that it is a program that will be run if you give it" \
                    "permission to continue. To be extra secure, Ubuntu MATE requires" \
                    "you to provide your administrator password before that permission" \
                    "is granted. Every single time.")
    content += '</p>' \
                '</div>' \
                '</div>'

    update_page("content", "html", content)

def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]
    pass


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]
    return False
