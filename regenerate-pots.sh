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
./welcome-po.py --update-pos
./edgar-allan create-all-pots

