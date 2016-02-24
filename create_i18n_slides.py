#!/usr/bin/python

""" Create a full set of translated slides for the Ubuntu Mate Welcome program

For every slide, run po2html for everyget a list of the po files available for
it and po2html for each. Place the output files in ./local/<locale>/<slidename>.html

Adapted from generate-local-slides.py from:
https://github.com/linuxmint/ubiquity-slideshow-mint

"""
import os, sys, glob, subprocess
import json

if not subprocess.call(["which", "po2html"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
	print("Error: po2html is not available.")
	sys.exit(1)

source_dir = '.'
build_slides = os.path.join(source_dir, 'data')
template_slides = glob.glob(os.path.join(build_slides, '*.html'))

i18n_dir = os.path.join(source_dir, "i18n")

# make the 'i18n' directory if not already present
if not os.path.exists(i18n_dir):
    os.mkdir(i18n_dir)

for slide in template_slides:
    slide_name = (os.path.splitext(os.path.split(slide)[1])[0])
    print("Working on slide: %s...." %slide_name)

    po_dir = os.path.join(os.path.join(os.path.join(source_dir, "data"), "po"), slide_name)
    locales = glob.glob(os.path.join(po_dir, '*.po'))
    for locale_file in sorted(locales):
	locale_name = os.path.basename(locale_file).replace(".po", "")

	locale_slides = os.path.join(i18n_dir, locale_name)
        #make the locale directory if it doesn't already exists
        if not os.path.exists(locale_slides):
            os.mkdir(locale_slides)
        
	output_slide = os.path.join(locale_slides, slide_name + ".html")
	
	if os.path.exists(output_slide):
		os.remove(output_slide)

	subprocess.call(['po2html',
		             '-i', locale_file,
		             '-t', slide,
                             '--progress', 'none',
                             '-o', output_slide])

