#!/usr/bin/env python3
#
#  Common functions for test scripts.
#
#  (C) Luke Horwell, Revised Jun 2016
#

import os
import sys
import inspect
import signal

repo_root = str(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '../../'))
name = 'Unspecified'
failed = False

# Prevent lock-up on CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

def start():
    global name
    if sys.stdout.isatty():
        print('\033[93m\nTest Started: ' + name + '\033[0m')
    else:
        print('Test Name: ' + name + '\n')

def error(reason):
    global failed
    failed = True
    if sys.stdout.isatty():
        print('\033[91m -- ' + reason + '\033[0m')
    else:
        print('ERROR: ' + reason)
    sys.stdout.flush()

def warning(message):
    if sys.stdout.isatty():
        print('\033[93m -- ' + message + '\033[0m')
    else:
        print('WARNING: ' + message)
    sys.stdout.flush()

def success(message):
    if sys.stdout.isatty():
        print('\033[92m -- ' + message + '\033[0m')
    else:
        print(message)
    sys.stdout.flush()

def end():
    global name
    global failed

    # Did the test succeed?
    if failed == True:
        if sys.stdout.isatty():
            print('\033[91mTEST FAILED: ' + name + '\033[0m')
        else:
            print('\nTest Failed!')
        exit(1)
    else:
        if sys.stdout.isatty():
            print('\033[92mTest Passed: ' + name + '\033[0m')
        else:
            print('\nSuccessfully passed.')
        exit(0)
