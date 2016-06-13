#!/usr/bin/env python3
#
#  Pings external repositories (PPAs or source lists)
#  to check they exist.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'Ping External Repositories'

import os
import json
import requests

###############################################
# START OF TEST
###############################################
test.start()

# Dictonary of URLs. Unique to prevent duplicates.
# urls["http://example.com"] = 1
urls = {}

# Load Applications JSON
json_path = os.path.join(test.repo_root, 'data/js/applications.json')
try:
    with open(json_path) as data_file:
        index = json.load(data_file)
except Exception as reason:
    test.error('Cannot open applications.json due to load error.')
    test.end()

# Test each source and PPA
categories = list(index.keys())
categories.sort()
for category in categories:
    category_items = list(index[category].keys())
    category_items.sort()
    for program_id in category_items:
        app = index[category][program_id]
        preinst = list(app['pre-install'].keys())
        for distro in preinst:
            method = app['pre-install'][distro]['method']

            # Generate Launchpad URL if a PPA
            if method == 'ppa':
                ppa = app['pre-install'][distro]['enable-ppa']
                ppa_author = ppa.split('ppa:')[1].split('/')[0]
                ppa_name = ppa.split('ppa:')[1].split('/')[1]
                url = "https://launchpad.net/~{0}/+archive/ubuntu/{1}".format(ppa_author, ppa_name)
                urls[url] = 1

            # Extract the URL if an apt source
            elif method == 'manual':
                apt_source_list = str(app['pre-install'][distro]['apt-sources'])
                apt_source_parts = apt_source_list.split(' ')
                for part in apt_source_parts:
                    if part.startswith('http'):
                        url = part
                        urls[url] = 1
                        break

                if not url.startswith('http'):
                    error('No source URL found for "{0}"!'.format(program_id))


# Compile the list of URLs
checklist = list(urls.keys())
checklist.sort()

# Check for resources that no longer exist.
for url in checklist:
    r = requests.get('http://ubuntu-mate.org/')
    if r.status_code == 404:
        test.error("Repository not found: " + url)

###############################################
# END OF TEST
###############################################
test.end()
