#! /usr/bin/python3
# -*- coding:utf-8 -*-

""" .po file generator for Ubuntu Mate Welcome slides

From /usr/share/i18n/SUPPORTED get a list of each unique country code e.g. en_GB,
fr_CA etc.

For each Welcome slide in data/ that has a corresponding .pot file in data/po/<slide_name>
e.g. data/chatroom.html and data/po/chatroom/chatroom.pot, create an empty .po file for each
country code by copying the .pot file to <country_code>.po. If <country-code>.po already exists
don't do anything as it might contain translations

Requirements before running:
    a po directory in data/ that contains a .pot file for each slide
"""

import os,sys,glob,shutil,subprocess
import country_codes

def create_slide_pos(po_dir, slide_name, country_codes):
    """ Create a set of .po files for a specfied using a specified 
        .pot file as a template
        
    Create a .po file for each country code named <code>.po
    by copying the .pot file. If the .po file already exists
    nothing is done
    
    Args:
        po_dir : the location of the po directory directory where the files are to be placed 
                 (i.e. data/po)
        slide_name : the name of the slide e.g. commuinity
        country_codes : a list of all the country codes supported on 
                            the system
    """


    dest_dir = os.path.join(po_dir, slide_name)
    pot_file = os.path.join(dest_dir, slide_name + ".pot")
    for code in country_codes:
        dest_po = os.path.join (dest_dir, code + ".po")
        if not os.path.isfile(dest_po):
            subprocess.call(["pot2po",
	                     pot_file, dest_po,
                             "--progress", "none"
                             ])


def check_slide_dirs(po_dir, slide_names):
    """ Check that each slide has a directory under the "po" directory

    Args: 
        po_dir : the location of the po directory
        slide_names : a list of the slide names

    Returns:
        a list which contains the names of any missing directories
    """
    
    missing_dirs = []
    for slide in slide_names:
        if not os.path.isdir (os.path.join(po_dir, slide)):
            missing_dirs.append(os.path.join(po_dir, slide))

    return missing_dirs


def check_for_missing_pots(po_dir, slide_names):
    """ check that each slide has a .pot file in its directory, named
        <slide name>.pot

    Args: po_dir : the location of the po directory
    slide_names :  a list of the slide names

    Returns:
        a list containing the names of any missing .pot files
    """

    missing_pots = []
    for slide in slide_names:
        pot_name = os.path.join(po_dir, slide)
        pot_name = os.path.join(pot_name, slide + ".pot")
        if not os.path.exists(pot_name):
            missing_pots.append (pot_name)

    return missing_pots

#####################################################################################


if not subprocess.call(["which", "pot2po"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
    print("Error: pot2po is not available.")
    sys.exit(1)

source_dir = '.'
build_slides = os.path.join(source_dir, 'data')
po_dir = os.path.join(build_slides, 'po')

if not os.path.exists(po_dir):
    print ("Error: There is no 'po' directory in data/")
    sys.exit(1)

template_slides = glob.glob(os.path.join(build_slides, '*.html'))

#get a list of the slide names, minus the .html extension
slide_names = []
for slide in template_slides:
    slide_names.append (os.path.splitext(os.path.split(slide)[1])[0])

#now check that there is a directory under data/po for each slide and that it contains a .pot
#file
missing_dirs = check_slide_dirs(po_dir, slide_names)
if len(missing_dirs)>0:
    for missing in missing_dirs:
        print ("Error: missing directory %s" %missing)

    sys.exit(1)

# now check that each slide has a .pot file
missing_pots = check_for_missing_pots(po_dir, slide_names)
if len(missing_pots)>0:
    for missing in missing_pots:
        print ("Error: missing pot file: %s" %missing)

    sys.exit(1)


#get the country codes
codes =country_codes.get_country_codes()
if codes is None:
    print("Error: couldn't get country codes")
    sys.exit(1)

# now create the .po files for each slide
for slide in slide_names:
    print ("creating .po files for %s slide" %slide)
    create_slide_pos (po_dir, slide, codes)

print ("Done...")





