#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2017 Luke Horwell <luke@ubuntu-mate.org>
#

"""
Contains common functions and classes used for Welcome's pages.
"""

import os
import sys
import gettext
from threading import Thread


def parse_html(html):
    """
    Returns a string that is HTML safe for jQuery to use.
    """
    return html.strip().replace('\n', '')


def get_data_source(dbg, bin_path):
    """
    Returns the data path for assets used by the application.
    """
    current_folder = os.path.abspath(os.path.join(os.path.dirname(bin_path)))

    if os.path.exists(os.path.join(current_folder, "data/")):
        dbg.stdout("Using relative path for data source. Non-production testing.", dbg.debug, 2)
        return os.path.join(current_folder, "data/")

    elif os.path.exists("/usr/share/ubuntu-mate-welcome/"):
        dbg.stdout("Using system-wide path for data source.", dbg.debug, 2)
        return "/usr/share/ubuntu-mate-welcome/"

    dbg.stdout("Unable to source the data directory.", dbg.error, 0)
    exit(1)


def setup_translations(bin_path, i18n_app, locale_override=None):
    """
    Initalises translations for the application.

    bin_path = __file__ of the application that is being executed.
    i18n_app = Name of the application's locales.

    Returns the function used for the _ variable.
    """
    whereami = os.path.abspath(os.path.join(os.path.dirname(bin_path)))

    if os.path.exists(os.path.join(whereami, "locale/")):
        # Using relative path
        locale_path = os.path.join(whereami, "locale/")
    else:
        # Using system path or en_US if none found
        locale_path = "/usr/share/locale/"

    if locale_override:
        t = gettext.translation(i18n_app, localedir=locale_path, fallback=True, languages=[locale_override])
    else:
        t = gettext.translation(i18n_app, localedir=locale_path, fallback=True)

    # This is set as the app's global variable: _
    return t.gettext


def spawn_thread(dbg, target, args=()):
    """
    Runs a function in its own thread (daemonized)

    Expects:
    function    Function object
    args        Truple contains arguments (if any)
    """
    dbg.stdout("Spawning thread: {0} (daemon {1}, args={2})".format(target.__name__, True, args), dbg.debug, 2)
    thread = Thread(target=target, args=args)
    thread.daemon = True
    thread.start()
