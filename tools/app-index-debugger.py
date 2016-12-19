#!/usr/bin/env python3

# Copyright 2016 Luke Horwell <lukehorwell37+code@gmail.com>
#
# Ubuntu MATE Welcome is free software: you can redistribute it and/or modify
# it under the temms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ubuntu MATE Welcome is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ubuntu MATE Welcome. If not, see <http://www.gnu.org/licenses/>.
#

""" This utility helps diagnose and output useful information
    about the application.json index used by Welcome.         """

import os
import sys
import signal
import inspect
import json
try:
    from prettytable import PrettyTable
except:
    print("Requires python3-prettytable")
    sys.exit(1)

def load_index():
    global index
    global current_folder
    current_folder = os.path.dirname( os.path.abspath(inspect.getfile(inspect.currentframe())) )
    json_path = os.path.join(current_folder, '../data/js/applications.json' )

    try:
        with open(json_path) as data_file:
            index = json.load(data_file)
    except Exception as e:
        print('Oops. JSON is invalid. The error is around here:')
        print(e)
        sys.exit()


def list_all_apps():
    global index
    t = PrettyTable(["Category", 'Name', 'Main Package', 'Sub-Category', 'Open Source?', 'Arch', 'Releases', 'Works?'])
    categories = list(index.keys())
    categories.sort()

    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            data = [category]

            for key in ["name", "main-package", "subcategory", "open-source", "arch", "releases", "working"]:
                try:
                    data.append(str(index[category][program_id][key]))
                except:
                    # Some categories are missing these fields (e.g. "KnownRepos")
                    data.append("")

            t.add_row(data)
    print(t)
    return


def list_broken():
    global index
    t = PrettyTable(["Category", 'Program ID', 'Notes'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            if not index[category][program_id]['working']:
              try:
                  # If the developer left any notes here.
                  notes = index[category][program_id]['notes']
              except:
                  notes = ''
              t.add_row([category, program_id,  notes])

    print('\nBroken Applications\n')
    print(t)
    return


def list_no_screenshot():
    global index
    t = PrettyTable(["Category", 'Program ID', 'Filename'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            if not category == 'Unlisted':
                try:
                    img = index[category][program_id]['img']
                except:
                    img = 'null'

                if not os.path.exists(os.path.join(current_folder, '../data/img/applications/screenshots/', img + '-1.jpg' )):
                    t.add_row([category, program_id, img + '-1.jpg'])

    print('\nApplications missing screenshots:\n')
    print(t)
    return


def list_missing_arch(arch):
    global index
    t = PrettyTable(["Category", 'Program ID', 'Releases'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            archs = index[category][program_id]['arch'].split(',')
            if not any(arch in archs for word in archs):
                t.add_row([category, program_id,  archs])

    print('\nApplications missing for architecture: ' + arch + '\n')
    print(t)
    return


def list_missing_codename(codename):
    global index
    t = PrettyTable(["Category", 'Program ID', 'Releases'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            releases = index[category][program_id]['releases'].split(',')
            if not any(codename in releases for word in releases):
                t.add_row([category, program_id,  releases])

    print('\nApplications missing for release: ' + codename + '\n')
    print(t)
    return


def list_special_preinstall():
    global index
    t = PrettyTable(["Category", 'Program ID', 'Release', 'Methods'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            try:
                releases = list(index[category][program_id]['pre-install'].keys())
            except:
                continue
            for release in releases:
                if release == 'all':
                    continue
                else:
                    methods = index[category][program_id]['pre-install'][release]['method']
                    t.add_row([category, program_id, release, methods])

    print('\nApplications with separate pre-configurations per release:')
    print(t)
    return


def list_app_sources():
    global index
    t_ppa = PrettyTable(["Category", 'Program ID', 'Method', 'PPA'])
    t_src = PrettyTable(["Category", 'Program ID', 'Method', 'Source File'])
    t_utu = PrettyTable(["Category", 'Program ID'])
    categories = list(index.keys())
    categories.sort()
    categories.remove("KnownRepos")
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            try:
                releases = list(index[category][program_id]['pre-install'].keys())
            except:
                continue
            for release in releases:
                methods = index[category][program_id]['pre-install'][release]['method'].split(',')
                for method in methods:
                    if method == 'ppa':
                        ppa = index[category][program_id]['pre-install'][release]['enable-ppa']
                        t_ppa.add_row([category, program_id, method, ppa])
                    if method == 'manual':
                        source_file = index[category][program_id]['pre-install'][release]['source-file'] + '.list'
                        t_src.add_row([category, program_id, method, source_file])
                    if method == 'skip':
                        t_utu.add_row([category, program_id])

    print('\nApplications that use the Ubuntu archives:')
    print(t_utu)
    print('\nApplications that use PPAs:')
    print(t_ppa)
    print('\nApplications that use external sources:')
    print(t_src)
    return


def process_args():
    args_ok = False
    for arg in sys.argv:
        if arg == '--help':
            help()
        if arg == '--all':
            args_ok = True
            list_all_apps()
            list_broken()
            list_no_screenshot()
            for codename in ['xenial', 'yakkety']:
                list_missing_codename(codename)
            for arch in ['i386', 'amd64', 'arm64', 'armhf']:
                list_missing_arch(arch)
            list_special_preinstall()
            list_app_sources()

        if arg == '--list-index':
            args_ok = True
            list_all_apps()

        if arg == '--list-broken':
            args_ok = True
            list_broken()

        if arg.startswith('--list-missing-codename'):
            codename = str(arg.split('--list-missing-codename=')[1])
            args_ok = True
            list_missing_codename(codename)

        if arg.startswith('--list-missing-arch'):
            arch = str(arg.split('--list-missing-arch=')[1])
            args_ok = True
            list_missing_arch(arch)

        if arg == '--list-special':
            args_ok = True
            list_special_preinstall()

        if arg == '--list-sources':
            args_ok = True
            list_app_sources()

        if arg == '--list-no-screenshot':
            args_ok = True
            list_no_screenshot()

    if not args_ok:
        print('Invalid arguments.')
        help()


def help():
    print('Usage:')
    print(' --all                             Show all lists.')
    print(' --list-index                      List applications in the index.')
    print(' --list-broken                     List applications that are not working.')
    print(' --list-missing-codename=<RELEASE> List applications not present in a release.')
    print(' --list-missing-arch=<ARCH>        List applications not present for an architecture.')
    print(' --list-special                    List applications that pre-install differently on releases.')
    print(' --list-sources                    List each application\'s source (eg. PPA, Ubuntu Archives)')
    print(' --list-no-screenshot              List applications without a screenshot.')
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if not sys.argv:
        help()

    load_index()
    process_args()
