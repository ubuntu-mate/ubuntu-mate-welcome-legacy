#!/usr/bin/env python3
#
#  Validates the applications saved in the Boutique database.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'Translation Templates for Code Tags'

import os

###############################################
# START OF TEST
###############################################
test.start()

# Where are they?
template_dir = os.path.join(test.repo_root, 'data/po/')
pages = os.listdir(template_dir)

# Only get the page name, no paths or extensions
html_pages = []
for page in pages:
    page = page.split('/')[-1]
    page = page.split('.html')[0]
    html_pages.append(page)

# Check each page's POT file
for page in html_pages:
    pot_path = os.path.join(template_dir, page, page + '.pot')

    with open(pot_path, 'r') as f:
        pot_data = f.read()

    # Search for code strings
    bad_strings = ['<span', '<b>', '</b>', '</span>', '<a',
                   'height=', 'width=', '<p', 'class=', 'id=']

    for syntax in bad_strings:
        results = pot_data.find(syntax)
        if results != -1:
            test.error('Found bad syntax containing "{0}" in "{1}" at character {2}.'.format(syntax, page, results))


###############################################
# END OF TEST
###############################################
test.end()
