#!/bin/bash
#
# This script will regenerate the translations
# for Ubuntu MATE Welcome. Intended for debugging.
#

repo_root=`realpath $(dirname "$0")/../`
cd "$repo_root"

rm -rf ./locale/
rm -rf ./data/i18n/
mkdir ./locale/
mkdir ./data/i18n/
./welcome-po.py --update-pos
./welcome-po.py --install
./edgar-allan translate-all
