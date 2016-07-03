#!/usr/bin/env python3
#
#  Allows test scripts to easily read the software index.
#
#  (C) Luke Horwell, Revised Jul 2016
#

import os
import json
import common.testing as test

# Load Applications JSON
path = os.path.join(test.repo_root, 'data/js/applications.json' )
try:
    with open(path) as f:
        data = json.load(f)

except Exception as reason:
    test.error('Syntax Error in "applications.json": ' + str(reason))
    test.error('Cannot proceed with this test!')
    test.end()

# Variables containing useful data
categories = list(data.keys())

# Function for getting information from the index.
def get(requested_id, attribute):
    ''' Retrieves a specific attribute from a listed application, without specifying its category. '''
    for category in categories:
        category_items = list(data[category].keys())
        for program_id in category_items:
            if program_id == requested_id:
                if not attribute == 'category':
                    return data[category][program_id][attribute]
                else:
                    return category
