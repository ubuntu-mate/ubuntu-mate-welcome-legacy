#! /usr/bin/python3
# -*- coding:utf-8 -*-

""" .pot file generator for Ubuntu Mate Welcome slides

Create the file structure and inital files required for translating
Ubuntu Mate Welcome slide


Create a 'po' directory in ./data if one is not already there and
under this create a directory for each of the Welcome slides, named 
appropriately, e.g. the directory for the Community slide will be named 'community'

For each slide generate a .pot file by calling html2po and 
place this file (e.g. community.pot) placed in the relevant directory 
If the file already exists, rename the existing file (e.g. to community.po.old)
so that it can be used for validating and correcting the new version

When all files are done, print a message reminding the user to
to manually check the new .pots

"""


import os,sys,glob,shutil, subprocess


if not subprocess.call(["which", "html2po"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
	print("Error: html2po is not available.")
	sys.exit(1)

source_dir = '.'
build_slides = os.path.join(source_dir, 'data')
po_dir = os.path.join(build_slides, 'po')

# if there isnt already a 'po' directory in ./data, create one
if not os.path.exists(po_dir):
    os.mkdir(po_dir)

template_slides = glob.glob(os.path.join(build_slides, '*.html'))

# create a list of tuples containing the full slide path and filename, and the slide 
# names minus the .html extension
slide_info=[]
for slide in template_slides:
    slide_filename = slide
    slide_name =(os.path.splitext(os.path.split(slide)[1])[0])
    slide_info.append([slide_filename, slide_name])

# if necessary create directories under po_dir for the slides
for slide in slide_info:
    print("%s %s" %(slide[0], slide[1]))
    if not os.path.exists(os.path.join(po_dir, slide[1])):
        os.mkdir(os.path.join(po_dir, slide[1]))

# now create the .pot files
for slide in slide_info:
    pot_file = os.path.join(po_dir, slide[1])
    pot_file = os.path.join(pot_file, slide[1] + ".pot")
    if os.path.exists(pot_file):
        # move the existing file out of the way
        shutil.copyfile (pot_file, pot_file + ".old")

    # now run html2po
    subprocess.call(['html2po',
	             '-P',                 # produce .pot file
	             '-i', slide[0],       # input file
	             '-o', pot_file])      # output file

    print ("%s created." %pot_file)

print ("\nReminder: don't forget check the .pot files in a text editor to ensure that all entries")
print ("are correct, and any new text in the html has been included.")

