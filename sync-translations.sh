#!/bin/bash -xe
#
# Can only be run by the Ubuntu MATE team with access to Transifex.
#
tx pull -a --minimum-perc=5
./welcome-po.py --update-pos
./edgar-allan create-all-pots
./edgar-allan translate-all
./welcome-po.py --update-launchers
tx push -s
