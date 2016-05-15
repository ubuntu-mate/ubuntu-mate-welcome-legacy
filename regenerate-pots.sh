#!/bin/bash
#
# This script will regenerate all the POT files for
# Ubuntu MATE Welcome.
#

workingdir=$(pwd)
for pot in $(ls $workingdir/data/po/)
do
  rm $workingdir/data/po/$pot/$pot.pot -v
done
rm po/ubuntu-mate-welcome.pot
./welcome-po.py --create-pot
./edgar-allan create-all-pots

