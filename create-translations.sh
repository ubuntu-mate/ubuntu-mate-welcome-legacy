#!/bin/bash
#
# This script will regenerate the translations
# for Ubuntu MATE Welcome. Intended for debugging.
#
rm -rf ./locale/
rm -rf ./data/i18n/
mkdir ./locale/
mkdir ./data/i18n/
./welcome-po.py --install
./edgar-allan translate-all
