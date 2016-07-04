#!/usr/bin/env python3
#
#  Verifies applications are present in the official archive
#  according to the listed architectures and distro codenames.
#
#   Requires 'rmadison' to be installed.
#   'rmadison' requires an internet connection.
#
#  (C) Luke Horwell, Revised Jul 2016
#

import common.testing as test
test.name = 'Verify Packages in Official Ubuntu Archive'

import os
import json
import subprocess

###############################################
# START OF TEST
###############################################
test.start()

# This test could take a while due to 'rmadison'.
# ... A hint of Yorkshire dialect ;)
test.warning("Ar' Madison takes 'er time. This test may take a few minutes to complete.")

# For 'wen we need to call ar Madison (rmadison)
def run_this_madison(package):
    cmd = 'rmadison ' + package

    raw = str(subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0])
    output = raw.replace("b'","").replace('b"',"").replace("\\n'","").replace("\\n","\n")

    return output

# Simple way to filter lists
def grep(data_list, grep):
    for line in data_list.split('\n'):
        if grep in line:
            return str(line)
    return None

###############################################

# Prepare the index
import common.index as index

# Check each application in the Ubuntu archive.
for category in index.categories:
    for program_id in list(index.data[category].keys()):
        packages = []

        # rmadison can only check things in the official archive.
        try:
            if not index.data[category][program_id]['pre-install']['all']['method'] == 'skip':
                continue
        except:
            # Cannot be checked, next!
            continue

        # Get packages from that listing.
        try:
            for this in index.data[category][program_id]['install-packages'].split(','):
                if this != '':
                    packages.append(this)
            for this in index.data[category][program_id]['remove-packages'].split(','):
                if this != '':
                    packages.append(this)
            packaged_arches = index.data[category][program_id]['arch'].split(',')
            packaged_releases = index.data[category][program_id]['releases'].split(',')
        except:
            # Not all listings have packages listed.
            continue

        # Merge package lists together.
        checklist = list(set(packages))

        # For each package this app uses...
        for package in checklist:
            output = run_this_madison(package)
            failed = False

            # Give up if no data was received.
            if output.strip() == '':
                test.warning(package + " = No data received. Could be a network error or no longer exists.")
                continue

            # Check each code name specified is available for our distribution.
            for codename in packaged_releases:
                pkg_info = grep(output, codename)

                # If that's empty, then it doesn't exist.
                if pkg_info == None:
                    test.error("FAILED: {0} = No package for '{1}'.".format(package, codename))
                    failed = True
                    continue

                # Check each architecture has a package for that release.
                pkg_arch = pkg_info.split('|')[3]
                for arch in packaged_arches:
                    if pkg_arch.find('all'):
                        # Packages that are not dependent on architecture.
                        break

                    if pkg_arch.find(arch) == -1:
                        # This package doesn't have a package for that arch!
                        test.error("FAILED: {0} = No package found for '{1}' (built for '{2}')".format(package, arch, codename))
                        failed = True
                        continue

            if not failed:
                test.success("Passed: " + package)

###############################################
# END OF TEST
###############################################
test.end()
