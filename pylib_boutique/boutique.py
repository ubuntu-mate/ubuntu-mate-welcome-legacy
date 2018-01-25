#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2016-2018 Luke Horwell <code@horwell.me>
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
    Main module for processing application listings and software changes.
"""

import os
import json
import subprocess
import requests
from time import time
from time import sleep

try:
    from pylib import snapsupport as snapsupport
    from pylib import common as common
except ImportError:
    import software_boutique.snapsupport as snapsupport
    import software_boutique.common as common

# Paths
cache_path = os.path.join(os.path.expanduser('~'), ".cache", "software-boutique")
installed_index = os.path.join(os.path.expanduser('~'), ".config", "software-boutique", "installed.json")
data_source = "/usr/share/ubuntu-mate-welcome/"

# Session Details
force_dummy = False
dbg = common.Debugging() # Main application will replace this.
system_arch = str(subprocess.Popen(["dpkg", "--print-architecture"], stdout=subprocess.PIPE).communicate()[0]).strip('\\nb\'')
current_os_version = common.get_distro_version()  # E.g. 18.04
current_os_codename = common.get_distro_name()  # E.g. bionic

# Default Strings (applications should localise these)
string_dict = {
    "details_text": "Details",
    "details_tooltip": "Learn more about this application",
    "install_text": "Install",
    "install_tooltip": "Install this application on your computer",
    "reinstall_text": "",
    "reinstall_tooltip": "Reinstall this application",
    "remove_text": "",
    "remove_tooltip": "Remove this application",
    "launch_text": "Launch",
    "launch_tooltip": "Runs the application",
    "remove_queue": "Remove from queue",
    "remove_queue_tooltip": "Cancels any changes for this application",
    "installing": "Installing...",
    "removing": "Removing...",
    "queued-install": "Will be installed.",
    "queued-remove": "Will be removed.",
    "starting-install": "Starting to install...",
    "starting-remove": "Starting to remove..."
}

class UICallback():
    """
    Triggered while a SoftwareInstallation() class is busy making a change.

    This class is a stub, it only outputs to the terminal.
    The main application should replace this so it works for those UI elements.

    status_text =   Str   E.g. "Updating Cache...", "Unpacking files..."
    percent     =   Int   A value between 0-100. -1 shows no progress bar.
    """
    def update_current_progress(self, status_text, percent=-1):
        print('\033[96m' + "Status Changed: {0} ({1}%)".format(status_text, str(percent)) + '\033[0m')


ui_callback = UICallback() # Until main application replaces this.


# Application Data
def read_index(json_path):
    """
    Reads the specified JSON path and returns it as a dictonary.
    """
    with open(json_path) as f:
        data = json.load(f)
    return(data)


def get_application_details(index_data, category, appid):
    """
    Returns an object holding the details about the application.

    index_data      = Data from index_data[category][appid]
    category        = ID of category from index.
    appid           = ID of application from index.
    """
    app = ApplicationData()
    data = index_data[category][appid]
    app.data = data

    app.appid = appid
    app.categoryid = category
    app.uuid = app.categoryid + "-" + app.appid

    app.name = data.get("name")
    app.summary = data.get("summary")
    app.description = data.get("description")
    app.developer_name = data.get("developer-name")
    app.developer_url = data.get("developer-url")
    app.tags = data.get("tags").split(",")
    app.launch_cmd = data.get("launch-cmd")
    app.proprietary = data.get("proprietary")
    app.urls = data.get("urls")
    app.arch = data.get("arch")
    app.releases = data.get("releases")
    app.method = data.get("method")
    app.post_install = data.get("post-install")
    app.post_remove = data.get("post-remove")

    app.icon_path = os.path.join(cache_path, "metadata", "icons", appid + ".png")

    app.screenshot_filenames = []
    for filename in screenshot_file_listing:
        if filename.startswith(appid + "-"):
            app.screenshot_filenames.append(filename)
    app.screenshot_filenames.sort()

    if app.method == "dummy" or force_dummy:
        app.installation = SoftwareInstallation.Dummy(app)
    elif app.method == "apt":
        app.installation = SoftwareInstallation.PackageKit(app)
    elif app.method == "snap":
        app.installation = SoftwareInstallation.Snappy(app)
    else:
        print(app.method + " is not supported!")
        return None

    app.is_installed = app.installation.is_installed

    return app


class ApplicationData():
    """
    Object that holds details about an application.

    The object is expected to be manipulated outside this class.
    """
    # IDs
    appid = ""
    categoryid = ""
    uuid = ""

    # Holds raw dictonary data
    data = {}

    # Variables from index
    name = ""
    summary = ""
    description = ""
    developer_name = ""
    developer_url = ""
    tags = ""
    launch_cmd = None
    proprietary = False
    alternate_to = None
    urls = {}
    arch = []
    releases = []
    method = "dummy"
    post_install = None
    post_remove = None

    # Variables Computed
    icon_path = ""
    screenshot_filenames = []
    install_date = 0
    install_date_string = ""

    # On-demand classes
    installation = None   # SoftwareInstallation.subclass()

    # On-demand functions
    is_installed = None   # Alias installation.is_installed function


class SoftwareInstallation():
    """
    Manages software installations with different methods.

    Required functions:

        __init__(self)
            Prepares that object, e.g. set up Apt.

            installation_data = Raw JSON of the "installation" group.
                                Depending on the class, this data will be handled differently.

        is_installed(self, params)
            Returns True or False whether the application is considered installed.

            app_obj = AppInfo() object. Can be used for extracting required data, e.g. snap/package name.

        do_install, do_remove (self, params)
            Returns True for a successful change, or False is something failed.

            app_obj = AppInfo() object. Can be used for extracting required data, e.g. snap/package name.

        Functions starting with _ may be used for miscellaneous purposes and can be defined within the class.
            E.g. Apt uses _update_cache() for both on-demand cache refreshing and when installing a new source.
    """

    class Dummy(object):
        """
        Dummy implementation for debugging software changes.
        """
        def __init__(self, app_obj):
            self.app = app_obj
            self.raw_data = app_obj.data.get("installation")

            # This dummy pretends to look busy.

        def is_installed(self):
            # Randomly determine this based on time.
            if int(time()) % 2 == 0:
                return True
            else:
                return False

        def do_install(self):
            for x in range(0, 100, 4):
                ui_callback.update_current_progress(string_dict["installing"], str(x))
                sleep(0.08)
            return True

        def do_remove(self):
            for x in range(0, 100, 12):
                ui_callback.update_current_progress(string_dict["removing"], str(x))
                sleep(0.22)
            return True


    class PackageKit(object):
        """
        Apt implementation using PackageKit as its back-end.
        """
        def __init__(self, app_obj):
            self.app = app_obj
            self.raw_data = app_obj.data.get("installation")

        def is_installed(self):
            return False

        def do_install(self):
            return True

        def do_remove(self):
            return True

        def _update_cache(self):
            return True

        @staticmethod
        def _is_running_ubuntu_mate():
            """
            Determines whether the user is actually running Ubuntu MATE determined if the
            2 main metapackages are installed and whether the session is running MATE.

            => Returns bool
            """
            # FIXME: if ubuntu-mate-desktop or ubuntu-mate-core are not installed and not running MATE => return False
            if os.environ.get('DESKTOP_SESSION') != "mate":
                return False
            else:
                return True

        @staticmethod
        def _is_boutique_subscribed():
            """
            Checks whether Welcome/Software Boutique is subscribed for updates.

            => Returns bool
            """
            ppa_file = "/etc/apt/sources.list.d/ubuntu-mate-dev-ubuntu-welcome-" + current_os_codename + ".list"
            if os.path.exists(ppa_file):
                if os.path.getsize(ppa_file) > 0:
                    return True
            return False

        def _get_instructions_for_this_codename(self):
            """
            Returns the dictonary containing the metadata for the current codename.
            E.g. If we're running 16.04 and there's a "xenial,yakkety" group
                Otherwise, "all" is used.

            => Returns string
            """
            target_key = "all"
            for codenames_raw in self.raw_data.keys():
                codenames = codenames_raw.split(",")
                if current_os_codename in codenames:
                    target_key = codenames_raw
            return(self.raw_data[target_key])

        def _get_package_list(self, install_type):
            """
            Returns a list of packages based on the type of installation.

            install_type    =   Expects "install" and "remove".

            => Returns list
            """
            filtered_index = self._get_instructions_for_this_codename()

            if install_type == "install":
                return(filtered_index["install-packages"])

            elif install_type == "remove":
                return(filtered_index["remove-packages"])

            else:
                return([])


    class PackageKitUpgrades(object):
        """
        Snaps implementation.
        """
        def __init__(self, app_obj):
            self.app = app_obj
            self.raw_data = app_obj.data.get("installation")

        def is_installed(self):
            return True

        def do_install(self):
            return True

        def do_remove(self):
            return True


    class Snappy(object):
        """
        Snaps implementation.
        """
        def __init__(self, app_obj):
            self.app = app_obj
            self.raw_data = app_obj.data.get("installation")
            self.snap_name = self.raw_data["all"]["name"]
            snapsupport.ui_callback = ui_callback

        def is_installed(self):
            return snapsupport.is_installed(self.snap_name)

        def do_install(self):
            try:
                ui_callback.update_current_progress(string_dict["starting-install"], -1)
                snapsupport.snap_install(self.snap_name)
                return True
            except Exception:
                return False

        def do_remove(self):
            try:
                ui_callback.update_current_progress(string_dict["starting-remove"], -1)
                snapsupport.snap_remove(self.snap_name)
                return True
            except Exception:
                return False


def _generate_button_html(action, app_obj, colour_class, fa_icon, text, tooltip):
    """
    Generates a HTML for installation button options.

    action          =   JS command to execute
    app_obj         =   ApplicationData() object
    colour_class    =   Class name for button colour.
    fa_icon         =   True/False whether it should use FA class or use application icon.
    text            =   Text shown on button.
    tooltip         =   Tooltip when hovering button.
    """
    if fa_icon:
        icon_html = "<span class='fa {0}'></span>".format(fa_icon)
    else:
        icon_html = "<img src='{0}'/>".format(app_obj.icon_path)

    # In format: "action?category?appid"
    cmd = "{0}?{1}?{2}".format(action, app_obj.categoryid, app_obj.appid)

    return "<button class='dialog-theme {1}' onclick='cmd(\"{0}\")' title='{4}'>{2} {3}</button>".format(
        cmd, colour_class, icon_html, text, tooltip
    )


def print_more_details_button(app_obj):
    """
    Returns the HTML for the "Details" button.
    """
    return _generate_button_html(
                "details", app_obj, "white", "fa-info-circle", string_dict["details_text"], string_dict["details_tooltip"]
            )


def print_app_installation_buttons(app_obj, queue):
    """
    Returns the HTML for the buttons that determines the installation/launch options.

    app_obj     =   ApplicationData() object
    queue            = Check the queue and show "Remove from queue" if listed.
    """
    html = "<div class='operation-buttons buttons-{0}'>".format(app_obj.uuid)

    # If this software is queued for changes, only show the option to cancel.
    if queue:
        for item in queue:
            if item[1].uuid == app_obj.uuid:
                operation = item[0]
                if operation == "remove":
                    icon = "fa-warning"
                else:
                    icon = "fa-check-circle"

                html += "<div class='queue-plan'><span class='fa {icon}'></span> {text}</div>".format(
                            icon = icon,
                            text = string_dict["queued-" + operation]
                        )
                html += _generate_button_html("drop-queue", app_obj, "white", "fa-clone", string_dict["remove_queue"], string_dict["remove_queue_tooltip"])
                html += "</div>"
                return(html)

    if app_obj.is_installed():
        html += _generate_button_html(
                    "install", app_obj, "yellow", "fa-refresh", string_dict["reinstall_text"], string_dict["reinstall_tooltip"]
                )

        html += _generate_button_html(
                    "remove", app_obj, "red", "fa-trash", string_dict["remove_text"], string_dict["remove_tooltip"]
                )

        # For card view, show icon on the far right.
        if app_obj.launch_cmd:
            html += _generate_button_html(
                        "launch", app_obj, "inverted", None, string_dict["launch_text"], string_dict["launch_tooltip"]
                    )

    else:
        html += _generate_button_html(
                    "install", app_obj, "green", "fa-download", string_dict["install_text"], string_dict["install_tooltip"]
                )

    html += "</div>"
    return(html)
