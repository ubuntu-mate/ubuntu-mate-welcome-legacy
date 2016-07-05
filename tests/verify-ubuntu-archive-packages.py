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
import sys
import json
import subprocess
import time
from threading import Thread

###############################################
# START OF TEST
###############################################
test.start()

# This test could take a while due to 'rmadison'.
# ... A hint of Yorkshire dialect ;)
test.warning("Ar' Madison takes 'er time. This test may take a few minutes to complete.")

# Miss Madison, look this up please!
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

# Function to output current progress
current = 0
total = 0
def progress():
    global current, total
    current = current + 1
    percent = int((current / total) * 100)
    return "[{0}%] - {1} / {2} - ".format(percent, current, total)

###############################################

# Prepare the index
import common.index as index

# Counts up all the packages for tracking progress.
counter = 0
names = []
for category in index.categories:
    category_items = list(index.data[category].keys())
    for program_id in category_items:
        try:
            for this in index.data[category][program_id]['install-packages'].split(','):
                if this != '':
                    names.append(this)
            for this in index.data[category][program_id]['remove-packages'].split(','):
                if this != '':
                    names.append(this)
        except:
            continue

    unique_names = list(set(names))
    counter =+ len(unique_names)
    total =+ counter

# Procedure for validating an application.
def check_category(category):
    global current
    category_items = list(index.data[category].keys())
    category_items.sort()
    for program_id in category_items:
        packages = []

        # rmadison can only check things in the official archive.
        try:
            if not index.data[category][program_id]['pre-install']['all']['method'] == 'skip':
                test.warning(progress() + "Skipped ID: " + program_id)
                continue
        except:
            # Cannot be checked, next!
            test.warning(progress() + "Skipped ID: " + program_id)
            continue

        # Skip if we mark it as broken.
        try:
            if index.data[category][program_id]['working'] == False:
                test.warning(progress() + "Skipped ID: " + program_id + " (marked as not working)")
                continue
        except:
            # Known Repos and Unlisted entries may not have this.
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
            test.warning(progress() + "Skipped ID: " + program_id)
            continue

        # Merge package lists together.
        checklist = list(set(packages))

        # For each package this app uses...
        for package in checklist:
            output = run_this_madison(package)
            failed = False

            # Give up if no data was received.
            if output.strip() == '':
                test.error(progress() + "FAILED: {0} = No data received!'")
                continue

            # Check each code name specified is available for our distribution.
            for codename in packaged_releases:
                pkg_info = grep(output, codename)

                # If that's empty, then it doesn't exist.
                if pkg_info == None:
                    test.error(progress() + "FAILED: {0} = No package for '{1}'.".format(package, codename))
                    failed = True
                    continue

                # Check each architecture has a package for that release.
                pkg_arch = pkg_info.split('|')[3]

                # Ignore source only lines.
                if pkg_arch.strip() == 'source':
                    break


                for arch in packaged_arches:
                    if pkg_arch.find('all') != -1:
                        # Packages that are not dependent on architecture.
                        break

                    if pkg_arch.find(arch) == -1:
                        # This package doesn't have a package for that arch!
                        test.error(progress() + "FAILED: {0} = No package found for '{1}' (on '{2}')".format(package, arch, codename))
                        failed = True
                        continue

            if not failed:
                test.success(progress() + "Passed: " + package)

# To speed things up, check each category in its own thread.
def check_thread(category):
    thread = Thread(target=check_category, args=[category])
    thread.start()
    threads.append(thread)

# Check each application in the Ubuntu archive.
threads = []
for category in index.categories:
    check_thread(category)
    # Wait a bit between each request.
    time.sleep(1.5)

# Wait for each thread to finish.
for thread in threads:
    thread.join()

###############################################
# END OF TEST
###############################################
test.end()
