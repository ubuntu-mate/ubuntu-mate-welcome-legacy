#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv2.
#
# Copyright (C) 2017-2018 Luke Horwell <luke@ubuntu-mate.org>
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
    ui = variables["objects"]["ui"]

    update_page("header", "show")
    update_page("footer", "show")
    update_page("main", "show")

    update_page("content", "append", ui.print_button("Normal", "quit", None, "normal"))


    #~ update_page("body", "append", "<script>cmd('test')</script>")


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]

    print("Exit")
    pass


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]

    #~ if cmd == "test":
        #~ return True
