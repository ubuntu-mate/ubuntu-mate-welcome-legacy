#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <luke@ubuntu-mate.org>
#               2015-2016 Martin Wimpress <code@flexion.org>
#

"""
Welcome Page: Shop

Provides details on purchasing Ubuntu MATE branded merchanise and products.
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
    ui = variables["objects"]["ui"]

    content = ''
    content += ui.print_title(_("Buy from the Boutique"))

    content += '<img src="img/shop/laptop.png">' \
                '<img src="img/shop/badge.png"/>' \
                '<img src="img/shop/flash-drive.png"/>' \
                '<img src="img/shop/mug.png"/>' \
                '<img src="img/shop/shirt.png"/>' \

    content += ui.print_paragraph(_("The Ubuntu MATE Boutique sells everything from computers " \
                "that come pre-installed with Ubuntu MATE to clothing and " \
                "apparel that are all Ubuntu MATE branded. Every item sold pays " \
                "a small commission to the Ubuntu MATE project."))

    update_page("content", "html", content)
    Common.page_enter_global(variables, _("Shop"))


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    Common.page_exit_global(variables)


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]
    return False
