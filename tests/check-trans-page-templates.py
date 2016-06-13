#!/usr/bin/env python3
#
#  Validates the applications saved in the Boutique database.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'Translation Templates for Pages'

import os
import glob

###############################################
# START OF TEST
###############################################
test.start()

# Where are they?
page_dir = os.path.join(test.repo_root, 'data/')
template_dir = os.path.join(test.repo_root, 'data/po/')

templates = os.listdir(template_dir)
pages = glob.glob(page_dir + '*.html')

# Only get the page name, no paths or extensions
html_pages = []
for page in pages:
    page = page.split('/')[-1]
    page = page.split('.html')[0]
    html_pages.append(page)

# Check each page has a template
for page in html_pages:
    if not os.path.exists(os.path.join(template_dir, page, page + '.pot')):
        test.error("No POT for page: " + page)

# Check pages are being translated on Transifex

tx_path = os.path.join(test.repo_root, '.tx/config')
with open(tx_path, 'r') as f:
    tx_file = f.read()

for page in html_pages:
    if tx_file.find('[ubuntu-mate-welcome.' + page + ']') == -1:
        test.warning("Template not on Transifex: " + page)

###############################################
# END OF TEST
###############################################
test.end()
