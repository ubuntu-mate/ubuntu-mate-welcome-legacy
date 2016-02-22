#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""  i18n helper for Ubuntu Mate Welcome

Perform one of the following functions depending on the command line args

    create a .pot file for the Welcome program and put it in the ./po directory
    (create this if necessary). To be used when initially creating the .pot file
    and also when new strings to translate are included in the Welcome program

    create a .po file either for a specified locale or for all locales supported
    by the system. If a .po file already exists, it will not be overwritten since
    it may contain translations

    update all .po files with new translatable strings from the .pot file

    compile and install the translations in all available .po file to
    usr/share/locale

"""

import os,sys,subprocess,shutil,glob

###########################################################
def show_usage():
    """ Display the command line options """

    print("\nwelcome-po usage")
    print("\nUsage: welcome-po [arguments]")
    print("  --create-pot                Create a ubuntu-mate-welcome.pot in the po directory")
    print("                              (can also be used when whenever new translatable strings")
    print("                               are added to ubuntu-mate-welcome.\n")
    print("  --create-po=<locale>        Create a .po file using the specfied locale and")
    print("                              place it in the po directory. If the .po file")
    print("                              already exists, it will not be overwritten as it")
    print("                              may already contain translations.")
    print("                              if ALL is specified for the locale, .po files for all")
    print("                              locales supported by the system will be produced.\n")
    print("  --update-pos                Update all .po files in the .po directory with new")
    print("                              translateable strings from the .pot file\n")
    print("  --install                   Compile all of the .po files in the po directory")        
    print("                              and install them under ./locale/\n")
    print("  --help                      Show this message\n")
    print(" Requirements:                Must be run in the same directory as ubuntu-mate-welcome")
    print("                              Requires xgettext, pot2po, msgmerge, msgfmt \n")



###########################################################
def create_pot(po_dir):
    """ Create .pot file for Ubuntu Mate Welcome
   
    Expect to find Welcome in the current directory...
    Create a po directory if one doesn't exist 

    Args: 
        po_dir - the location of the po directory

    """

    if not subprocess.call(["which", "pygettext"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
        print("Error: pygettext is not available.")
        sys.exit(1)

    if not (os.path.exists(po_dir)):
        os.mkdir(po_dir)

    pot_file = os.path.join(po_dir,"ubuntu-mate-welcome.pot")

    subprocess.call(["xgettext",
	             "-d", "ubuntu-mate-welcome",    # domain name
	             "-o", pot_file,                 # output file
                     "ubuntu-mate-welcome",          # input file
                     "-L", "Python"])                # Language

    print ("%s created.\n" %pot_file)


###########################################################
def get_country_codes():

    """ Read country codes /usr/share/i18n/SUPPORTED

    Returns:
        a list containing the country codes, or None if an error occured reading the codes
    """

    codes = []
    codefile = open("/usr/share/i18n/SUPPORTED")
    for code in codefile:

        thiscode = None

        iscomment = code.startswith('#')
        if not iscomment:

            # check for a two character country code
            if (code[2] == " ") or (code[2] == "."):
                thiscode = code[0:]
            elif code[2] == "_":
                thiscode = code[0:5]
            elif code[3] == "_":
                thiscode = code[0:6]

            if thiscode is not None:
                thiscode = thiscode.split()[0]
                thiscode = thiscode.split(".")[0]

            if not thiscode in codes:
                codes.append(thiscode)

    return codes

###########################################################
def create_po (po_dir, locale):
    """ Create a .po file for the specified locale

    Display an error if locale is not valid
    If locale is 'ALL' create .po files for all supported locales
    Do not overwrite any existing .po files
    """

    def pot_2_po (pot_file, po_file):
        """ Copy a pot file to a po file
        
        Use the pot2po command to ensure correct character encoding
        """

        if os.path.exists(po_file):
            print("%s already exists. Not overwriting..." %po_file)
        else:
            subprocess.call(["pot2po",
	                     pot_file, po_file])        
            print("%s created" %locale_file)


    pot_file = os.path.join(po_dir,"ubuntu-mate-welcome.pot")
    if not os.path.exists(pot_file):
        print("Error: ubuntu-mate-welcome.pot does not exist")

    codes = get_country_codes()
    if codes is None:
        print("Error: could not read country codes")
        exit()

    if locale != "ALL":
        if not locale in codes:
            print("Error: %s is not a valid locale" %locale)
            exit()

        locale_file = os.path.join(po_dir, locale + ".po")
        pot_2_po(pot_file, locale_file)
    else:
        for code in codes:
            locale_file = os.path.join(po_dir, code + ".po")
            pot_2_po(pot_file, locale_file)

        print ("All files created.....")

    exit()

###########################################################
def update_pos(po_dir):
    """ Update all .po files with any new translatable strings from the .pot
        file

    Use msgmerge in order to preserve any existing translations in the .po
    files

    Args: po_dir - the directory containing the .po files
    """

    pot_file = os.path.join(po_dir,"ubuntu-mate-welcome.pot")
    if not os.path.exists(pot_file):
        print("Error: ubuntu-mate-welcome.pot does not exist")
        exit()

    po_files = glob.glob(os.path.join(po_dir, '*.po'))

    for po_file in po_files:
        subprocess.call(["msgmerge",
                        po_file, pot_file,
                        "-U",                # Update po file
                        "-q"])               # Quiet mode
        print("%s updated " %po_file)

    print ("Update completed......")


###########################################################
def compile_and_install(po_dir, locale_dir):
    """ Compile all of the po files in the po directory into the
        locale directory, ready for use by the Welcome
        program
    
    Create the locale directory and any required subdirectories 
    if they don't already exist
    """

    if not (os.path.exists(locale_dir)):
        os.mkdir(locale_dir)

    po_files = glob.glob(os.path.join(po_dir, '*.po'))
    for po_file in po_files:
        locale_name =(os.path.splitext(os.path.split(po_file)[1])[0])
        
        #create a directory for the locale if we don't already have one
        this_locale = os.path.join(locale_dir, locale_name)
        lcm_dir = os.path.join(this_locale, "LC_MESSAGES")

        if not os.path.exists(this_locale):
            os.mkdir(this_locale)
            # also make the LC_MESSAGES directory
            os.mkdir(lcm_dir)
        
        #now compile and install the .po
        print ("processing %s" %po_file)
        output_file = os.path.join(lcm_dir, "ubuntu-mate-welcome.mo")

        subprocess.call(["msgfmt", po_file,
	             "--output-file", output_file])


    print ("All languages compiled.")


if (len(sys.argv)==1) or (sys.argv[1]=="--help"):
    show_usage()
    exit()

if not os.path.exists("./ubuntu-mate-welcome"):
    print("Error: Need to be in the same directory as ubuntu-mate-welcome...")
    exit()

source_dir = '.'
po_dir = os.path.join(source_dir, "po")
locale_dir = os.path.join(source_dir, "locale")

arg = sys.argv[1]
if (arg == "--create-pot") or (len(sys.argv)==1):
    create_pot(po_dir)
    exit()

if arg.startswith('--create-po='):
    locale = arg.split('--create-po=')[1]
    create_po(po_dir, locale)
    exit()

if arg=="--update-pos":
    update_pos(po_dir)
    exit()

if arg=="--install":
    compile_and_install(po_dir, locale_dir)
    exit()
