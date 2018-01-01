#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <luke@ubuntu-mate.org>
#               2015-2016 Martin Wimpress <code@flexion.org>
#

"""
Welcome Page: Donate

Provides links on how to donate to support development, as well as
monthly donation reports.
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
