#!/bin/bash
#
# This script needs to be run after all .pots have been created
# and it requires pot2po
# For every slide two .po files - 
# en_GB.po (without translations) and fr_FR.po (in which all
# translations are set to be the original text reversed. 
#
# a full set of the translated html slides can then be generated
# from these and used for testing purposes

pot2po data/po/chatroom/chatroom.pot data/po/chatroom/en_GB.po 
pot2po data/po/community/community.pot data/po/community/en_GB.po 
pot2po data/po/donate/donate.pot data/po/donate/en_GB.po 
pot2po data/po/features/features.pot data/po/features/en_GB.po 
pot2po data/po/gettingstarted/gettingstarted.pot data/po/gettingstarted/en_GB.po 
pot2po data/po/getinvolved/getinvolved.pot data/po/getinvolved/en_GB.po 
pot2po data/po/helloguest/helloguest.pot data/po/helloguest/en_GB.po 
pot2po data/po/hellolive/hellolive.pot data/po/hellolive/en_GB.po 
pot2po data/po/index/index.pot data/po/index/en_GB.po 
pot2po data/po/introduction/introduction.pot data/po/introduction/en_GB.po 
pot2po data/po/rpi/rpi.pot data/po/rpi/en_GB.po 
pot2po data/po/shop/shop.pot data/po/shop/en_GB.po 
pot2po data/po/software/software.pot data/po/software/en_GB.po 
pot2po data/po/splash/splash.pot data/po/splash/en_GB.po
echo "Creating fr_FR.po files for each slide"
./edgar-allan po --input=data/po/chatroom/en_GB.po --output=data/po/chatroom/fr_FR.po
./edgar-allan po --input=data/po/community/en_GB.po --output=data/po/community/fr_FR.po 
./edgar-allan po --input=data/po/donate/en_GB.po --output=data/po/donate/fr_FR.po
./edgar-allan po --input=data/po/features/en_GB.po --output=data/po/features/fr_FR.po
./edgar-allan po --input=data/po/gettingstarted/en_GB.po --output=data/po/gettingstarted/fr_FR.po
./edgar-allan po --input=data/po/getinvolved/en_GB.po --output=data/po/getinvolved/fr_FR.po
./edgar-allan po --input=data/po/gettingstarted/en_GB.po --output=data/po/gettingstarted/fr_FR.po
./edgar-allan po --input=data/po/helloguest/en_GB.po --output=data/po/helloguest/fr_FR.po
./edgar-allan po --input=data/po/hellolive/en_GB.po --output=data/po/hellolive/fr_FR.po
./edgar-allan po --input=data/po/index/en_GB.po --output=data/po/index/fr_FR.po
./edgar-allan po --input=data/po/introduction/en_GB.po --output=data/po/introduction/fr_FR.po
./edgar-allan po --input=data/po/rpi/en_GB.po --output=data/po/rpi/fr_FR.po
./edgar-allan po --input=data/po/shop/en_GB.po --output=data/po/shop/fr_FR.po
./edgar-allan po --input=data/po/software/en_GB.po --output=data/po/software/fr_FR.po
./edgar-allan po --input=data/po/splash/en_GB.po --output=data/po/splash/fr_FR.po
echo
echo "Done."
