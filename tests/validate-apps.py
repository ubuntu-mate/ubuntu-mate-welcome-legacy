#!/usr/bin/env python3
#
#  Validates the applications saved in the Boutique database.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'Index Validation'

import os
import json

###############################################
# START OF TEST
###############################################
test.start()

valid_distro_codenames = [
                          'precise', 'trusty', 'utopic', 'vivid',
                          'wily', 'xenial', 'yakkety'
                         ]

# Load Applications JSON
json_path = os.path.join(test.repo_root, 'data/js/applications.json' )
try:
    with open(json_path) as data_file:
        index = json.load(data_file)
except Exception as reason:
    test.error('Syntax Error in "applications.json": ' + str(reason))
    # The test can't continue.
    test.error('Cannot open applications.json due to load error!')
    test.end()

# Check each application in index for correct data structure
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
                test.error('Missing required data: "' + variable + '" for Program ID "' + program_id + '"')

        # Program IDs should only contain alphumerical characters or numbers or dashes in lowercase.
        for char in program_id:
            if char not in 'qwertyuiopasdfghjklzxcvbnm1234567890-':
                test.error('Non-alphumeric lowercase characters (a-z 0-9 -) found for: "' + program_id + '"')

        # Should not start or end with a dash.
        if program_id[:1] == '-':
            test.error('ID cannot start with dash: "' + program_id + '"')

        if program_id[-1:] == '-':
            test.error('ID cannot end with dash: "' + program_id + '"')

        # Check data types are consistent for strings.
        for variable in ['name', 'img', 'main-package', 'install-packages', 'remove-packages', 'subcategory', 'arch', 'releases']:
            try:
                if not type(app[variable]) is str:
                    test.error('Data must be string: "' + variable + '" for Program ID "' + program_id + '"')
            except:
                pass

        # If an upgrade package, is it a boolean?
        for variable in ['upgradable', 'boolean']:
            try:
                if not type(app[variable]) is bool:
                    test.error('Data must be boolean: "' + variable + '" for Program ID "' + program_id + '"')
            except:
                pass

        # Any
        if not category == 'Unlisted':
            for variable in ['description']:
                try:
                    if not type(app[variable]) is list:
                        test.error('Data must be list: "' + variable + '" for Program ID "' + program_id + '"')
                except:
                    pass

        # Does an icon exist for notifications?
        try:
            img = app['img']
        except:
            img = 'null'

        path = os.path.join(test.repo_root, 'data/img/applications/', img + '.png' )
        if not os.path.exists(path):
            test.error('Missing icon: "' + path + '" for Program ID "' + program_id + '"')

        # Is there pre-install info?
        try:
            app['pre-install']
            try:
                app['pre-install']['all']
            except:
                test.error('Missing pre-install data for Program ID "' + program_id + '". "all": { "method": "skip" } must be explicitly stated. ')
        except:
            test.error('Missing pre-install information for Program ID "' + program_id + '!"')

        # Check that there is a valid arch specified for applications.
        arch_check = app['arch'].split(',')
        for arch in arch_check:
            if arch == 'i386':
                pass
            elif arch == 'amd64':
                pass
            elif arch == 'armhf':
                pass
            elif arch == 'powerpc':
                pass
            else:
                test.error('Unknown architecture: "{0}" for Program ID "{1}"'.format(arch, program_id))

        # Check for valid distribution releases.
        distro_check = app['releases'].split(',')
        for release in distro_check:
            matched = False
            for codename in valid_distro_codenames:
                if codename == release:
                    matched = True
                    break
                else:
                    bad_name = release
            if not matched:
                test.error('Unknown release: "{0}" for Program ID "{1}"'.format(bad_name, program_id))

        # Check for no spaces in package names.
        ## For regular packages
        for list_data in ['main-package', 'install-packages', 'remove-packages', 'upgrade-packages']:
            try:
                packages = app[list_data]
                search = packages.find(' ')
                if search is not -1:
                    test.error('Whitespace found: "' + list_data + '" for "' + program_id + '".')
            except:
                # That package list doesn't exist, depends if it's an upgrade package or not.
                pass


###############################################
# END OF TEST
###############################################
test.end()
