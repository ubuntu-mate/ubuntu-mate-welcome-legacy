#!/usr/bin/env python3
#
#  Validates the applications saved in the Boutique database.
#
#  Test written by Luke Horwell
#

test = 'Index Validation'

import os
import sys
import signal
import inspect
import json

current_folder = os.path.dirname( os.path.abspath(inspect.getfile(inspect.currentframe())) )
json_path = os.path.join(current_folder, '../data/js/applications.json' )
test_failed = False

# Prevent lock-up on CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# When tests fail.
def failed(reason):
    global test
    global test_failed
    test_failed = True
    print('\033[91m -- ' + reason)

def test_results():
    global test
    global test_failed
    # Did the test succeed?
    if test_failed == True:
        print('\033[91mTEST FAILED: ' + test)
        exit(1)
    else:
        print('\033[92mTest Passed: ' + test)
        exit(0)

# Silence please!
print('\033[93m\nTest Started: ' + test + '\033[0m')


###############################################
# START OF TEST
###############################################

# Load Applications JSON
try:
    with open(json_path) as data_file:
        index = json.load(data_file)
except Exception as reason:
    failed('Syntax Error in "applications.json": ' + str(reason))
    # The test can't continue.
    exit(1)


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
                failed('Missing required data: "' + variable + '" for Program ID "' + program_id + '"')

        # Program IDs should only contain alphumerical characters or numbers or dashes in lowercase.
        for char in program_id:
            if char not in 'qwertyuiopasdfghjklzxcvbnm1234567890-':
                failed('Non-alphumeric lowercase characters (a-z 0-9 -) found for: "' + program_id + '"')

        # Should not start or end with a dash.
        if program_id[:1] == '-':
            failed('ID cannot start with dash: "' + program_id + '"')

        if program_id[-1:] == '-':
            failed('ID cannot end with dash: "' + program_id + '"')

        # Check data types are consistent for strings.
        for variable in ['name', 'img', 'main-package', 'install-packages', 'remove-packages', 'subcategory', 'arch', 'releases']:
            try:
                if not type(app[variable]) is str:
                    failed('Data must be string: "' + variable + '" for Program ID "' + program_id + '"')
            except:
                pass

        # If an upgrade package, is it a boolean?
        for variable in ['upgradable', 'boolean']:
            try:
                if not type(app[variable]) is bool:
                    failed('Data must be boolean: "' + variable + '" for Program ID "' + program_id + '"')
            except:
                pass

        # Any
        if not category == 'Unlisted':
            for variable in ['description']:
                try:
                    if not type(app[variable]) is list:
                        failed('Data must be list: "' + variable + '" for Program ID "' + program_id + '"')
                except:
                    pass

        # Does an icon exist for notifications?
        try:
            img = app['img']
        except:
            img = 'null'

        path = os.path.join(current_folder, '../data/img/applications/', img + '.png' )
        if not os.path.exists(path):
            failed('Missing icon: "' + path + '" for Program ID "' + program_id + '"')

        # Is there pre-install info?
        try:
            app['pre-install']
            try:
                app['pre-install']['all']
            except:
                failed('Missing pre-install data for Program ID "' + program_id + '". "all": { "method": "skip" } must be explicitly stated. ')
        except:
            failed('Missing pre-install information for Program ID "' + program_id + '!"')

        # Check that there is a valid arch specified for applications.
        arch_check = app['arch'].split(',')
        arch_OK = False
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
                failed('Unknown architecture: "' + arch + '" for Program ID "' + program_id + '"')

        # Check for no spaces in package names.
        ## For regular packages
        for list_data in ['main-package', 'install-packages', 'remove-packages', 'upgrade-packages']:
            try:
                packages = app[list_data]
                search = packages.find(' ')
                if search is not -1:
                    failed('Whitespace found: "' + list_data + '" for "' + program_id + '".')
            except:
                # That package list doesn't exist, depends if it's an upgrade package or not.
                pass


###############################################
# END OF TEST
###############################################

test_results()
