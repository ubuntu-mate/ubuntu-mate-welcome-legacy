#! /usr/bin/python3

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

import os, sys, signal, inspect, json
from prettytable import PrettyTable
""" Requires package: python3-prettytable if not already installed. """

def load_index():
    global index
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
            data = [
                    category,
                    index[category][program_id]['name'],
                    index[category][program_id]['main-package'],
                    index[category][program_id]['subcategory'],
                    str(index[category][program_id]['open-source']),
                    index[category][program_id]['arch'],
                    index[category][program_id]['releases'],
                    str(index[category][program_id]['working']),
                  ]
            t.add_row(data)
    print(t)
    return


def validate_apps():
    global index
    print('Scanning index for consistency...')
    t = PrettyTable(["Category", 'Program ID', 'Variable', 'Fault'])
    categories = list(index.keys())
    categories.sort()
    for category in categories:
        category_items = list(index[category].keys())
        category_items.sort()
        for program_id in category_items:
            app = index[category][program_id]
            # Check for required variables.
            for variable in ['name', 'img', 'main-package', 'description', 'subcategory', 'open-source', 'url-info', 'arch', 'releases', 'working']:
                try:
                    app[variable]
                except:
                    t.add_row([category, program_id, variable, 'Missing, is required.'])

            # Check data types are consistent.
            for variable in ['name', 'img', 'main-package', 'install-packages', 'remove-packages', 'subcategory', 'arch', 'releases']:
                try:
                    if not type(app[variable]) is str:
                        t.add_row([category, program_id, variable, 'Must be a string.'])
                except:
                    pass

            for variable in ['upgradable', 'boolean']:
                try:
                    if not type(app[variable]) is bool:
                        t.add_row([category, program_id, variable, 'Must be a boolean.'])
                except:
                    pass

            if not category == 'Unlisted':
                for variable in ['description']:
                    try:
                        if not type(app[variable]) is list:
                            t.add_row([category, program_id, variable, 'Must be a list.'])
                    except:
                        pass

            try:
                app['pre-install']
            except:
                t.add_row([category, program_id, variable, 'Missing pre-install configuration.'])

    print('\nIndex Validation Results\n')
    print(t)
    return


def list_broken():
    global index
    t = PrettyTable(["Category", 'Program ID', 'Notes'])
    categories = list(index.keys())
    categories.sort()
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


def list_missing_arch(arch):
    global index
    t = PrettyTable(["Category", 'Program ID', 'Releases'])
    categories = list(index.keys())
    categories.sort()
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
        if arg == '--validate':
            args_ok = True
            validate_apps()
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
    if not args_ok:
        print('Invalid arguments.')
        help()


def help():
    print('Usage:')
    print(' --validate                        Check index for consistent data types and required values.')
    print(' --list-index                      List applications in the index.')
    print(' --list-broken                     List applications that are not working.')
    print(' --list-missing-codename=<RELEASE> List applications not present in a release.')
    print(' --list-missing-arch=<ARCH>        List applications not present for an architecture.')
    print(' --list-special                    List applications that pre-install differently on releases.')
    print(' --list-sources                    List each application\'s source (eg. PPA, Ubuntu Archives)')
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if not sys.argv:
        help()

    load_index()
    process_args()