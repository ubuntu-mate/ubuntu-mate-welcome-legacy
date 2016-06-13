#!/usr/bin/env python3
#
#  Validates the applications saved in the Boutique database.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'Image Extensions'

import os
import glob

###############################################
# START OF TEST
###############################################
test.start()

# Where are they?
app_icons = os.path.join(test.repo_root, 'data/img/applications/')
app_scnsht = os.path.join(test.repo_root, 'data/img/applications/screenshots/')

icon_list   = glob.glob(app_icons + '*.jpg') + glob.glob(app_icons + '*.jpeg')
scnsht_list = glob.glob(app_scnsht + '*.png')

if len(icon_list) > 0:
    for filename in icon_list:
        filename = filename.split('/')[-1]
        test.error("Wrong extension for application icon: " + filename)

if len(scnsht_list) > 0:
    for filename in scnsht_list:
        filename = filename.split('/')[-1]
        test.error("Wrong extension for application screenshot: " + filename)

###############################################
# END OF TEST
###############################################
test.end()
