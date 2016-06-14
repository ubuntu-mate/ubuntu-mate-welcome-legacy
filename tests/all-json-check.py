#!/usr/bin/env python3
#
#  Checks all JSON databases can be processed.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import common.testing as test
test.name = 'JSON Syntax Check'

import os
import json

###############################################
# START OF TEST
###############################################
test.start()

json_files = [
                'data/js/applications.json',
                'data/js/news.json'
             ]

# Check each JSON file is free from syntax errors.
for json_path in json_files:
    try:
        path = os.path.join(test.repo_root, json_path)
        with open(json_path) as data_file:
            index = json.load(data_file)
    except Exception as reason:
        test.error('Syntax Error in "' + json_path + '". ')
        test.error('-- ' + str(reason))

###############################################
# END OF TEST
###############################################
test.end()
