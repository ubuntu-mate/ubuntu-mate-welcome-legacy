#!/bin/bash
#
# This script will regenerate all the POT files for
# Ubuntu MATE Welcome.
#

repo_root=`realpath $(dirname "$0")/../`
cd "$repo_root"

for pot in $(ls data/po/)
do
  rm data/po/$pot/$pot.pot -v
done
rm po/ubuntu-mate-welcome.pot
./welcome-po.py --create-pot
./edgar-allan create-all-pots

