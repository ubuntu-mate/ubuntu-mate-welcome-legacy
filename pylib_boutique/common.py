#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2017-2018 Luke Horwell <code@horwell.me>
#
# Software Boutique is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Software Boutique is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Software Boutique. If not, see <http://www.gnu.org/licenses/>.
#

"""
Common functions shared between Software Boutique and the Welcome application.
"""

import os
import gettext
import sys

class Debugging(object):
    """
    Outputs pretty debugging details to the terminal.
    """
    def __init__(self):
        self.verbose_level = 0
        self.override_arch = None
        self.override_codename = None
        self.override_locale = None
        self.simulate_only = None

        # Colours for stdout
        self.error = '\033[91m'
        self.success = '\033[92m'
        self.warning = '\033[93m'
        self.action = '\033[93m'
        self.debug = '\033[96m'
        self.normal = '\033[0m'

    def stdout(self, msg, colour_code='\033[0m', verbosity=0):
        # msg           String containing message for stdout.
        # color         stdout code (e.g. '\033[92m')
        # verbosity     0 = Always shown
        #               1 = -v flag
        #               2 = -vv flag

        if self.verbose_level >= verbosity:
            # Only colourise output if running in a real terminal.
            if sys.stdout.isatty():
                print(colour_code + msg + '\033[0m')
            else:
                print(msg)


def setup_translations(bin_path, i18n_app, locale_override=None):
    """
    Initalises translations for the application.

    bin_path = __file__ of the application that is being executed.
    i18n_app = Name of the application's locales.

    Returns the gettext object commonly assigned to a _ variable.
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

    return t.gettext

def parse_os_release():
    with open("/etc/os-release") as f:
        d = {}
        for line in f:
            k, v = line.rstrip().split("=")
            d[k] = v
    return d


def get_distro_name():
    d = parse_os_release()
    return d["ID"].replace("\"", "")


def get_distro_version():
    d = parse_os_release()
    return d["VERSION"].replace("\"", "")
