# ubuntu-mate-welcome

The Ubuntu MATE Welcome application to greet both new and returning users on their first login.

## Features

  * **Introduce new users to the operating system.**
    * Highlight key features of Ubuntu MATE.
    * Provide quick guidelines on getting started.
    * Provide quick installation guidance.
    * Inform users of their own system specifications.
  * **Grow the Ubuntu MATE Community**
    * Accessible links to the community forums and social networks.
    * Inform of Ubuntu MATE branded products for sale.
    * Provide details on donating to the project.
  * **Install Software**
    * From a pick of Ubuntu MATE's recommended software tested for the distribution.
    * Install a package manager, such as *Ubuntu Software Center*.

Originally based on:

  * https://github.com/Antergos/antergos-welcome
  * http://blog.schlomo.schapiro.org/2014/01/apt-install.html

## Optional Arguments

Welcome does not require arguments for general usage, but for debugging
and testing purposes, the following can be specified:

  * `--verbose` = Show more details to stdout.
  * `--force-arch=<ARCH>` = Simulate an architecture.
    * `i386` or `amd64` or `armvf` or `powerpc`
  * `--force-session=<TYPE>` = Simulate a specific type of session where Welcome is accessed.
    * `live` (Live Session) or `guest` (Guest User) or `pi` (Raspberry Pi 2)
  * `--force-codename=<NAME>` = Simulate a specific Ubuntu release.
    * Eg. `trusty` or `wily` or `xenial`.
  * `--force-no-net` = Simulate no internet connection.
  * `--force-net` = Simulate an internet connection.
  * `--locale` = specify a locale to use, otherwise the default locale will be used.  
  * `--software-only` = Only show the Software page. (Hides social links, uses a larger window)
  * `--simulate-changes` = Simulate changes made to packages without modifying the system.
  

## Requirements

  * gir1.2-gtk-3.0
  * gir1.2-notify-0.7
  * gir1.2-webkit-3.0
  * libgtk2-perl
  * libnotify-bin
  * parted
  * pciutils
  * policykit-1
  * python3
  * python3-apt
  * python3-aptdaemon
  * python3-aptdaemon.gtk3widgets
  * python3-gi
  * software-properties-common
  * inxi
  * humanity-icon-theme

# Translations

## edgar-allan

Stupid name, but we like it, which supports the following arguments:

  * `create-all-pots` - will create a `.pot` file for every slide (using
  `@zwnj;` chars to denote translatable string) and place it in `data/po/<slide name>`
  * `translate-all` - for each slide, will produce translated html for
  each `.po` found in `data/po/slidename`. The `.po` should according to
  locale e.g. `en_GB.po`. The output will be written to the
  `i18n/<locale>/` directory as `slide_name.html`
  * `create-pot` - create a single `.pot` file (mainly for testing purposes)
  * `translate` - translate a single slide (mainly for testing purposes)
  * `po` - for each translatable string in a po file, set the
  translation to be the original string reversed (only for use when
  testing...)

Addtional arguments:

  * `--input=<filename>` used with `create-pot` and translate and
  specifies the source html. Also used with `po` to specified `.po` file
  containing strings to be reversed `--po-file=<filename>` used with
  `translate` and specified `.po` file to use
  * `--output=<filename>` used with `create-pot`, `translate` and `po`
  and specifies the output file

Normal usage would be to:

  * run `create-pot` to create an initial set of `.pot` files or to
  update them when new strings are added to slides.
  * check the .pots in `poedit` or a text editor in case missing or
  misaligned `&zwnj;`'s in the html
  * copy `.po` files translations from Transiflex into the
  `data/po/<slide_name>/` directories
  * run `translate-all` to build a set of translated slides

## create-test-pos.sh

For testing purposes only. After `edgar-allan create-all-pots` has been
run, this can be used to generate test `en_GB` and `fr_FR` .po files for
each slide. The `en_GB` version contains no translations whilst the
French version has every translation set as the reverse of the original
string. Translated html can be produced from these .po files by running
`edgar-allan translate-all`, and viewed in the `i18n/en_GB` and `fr_FR`
directories.


# Old translation documentation

**THESE ARE OBSOLETE AND WILL BE REMOVED SOON.**

Ubuntu MATE Welcome now supports translated html. To serve up html, the
translated files are copied out of i18n directory into another
directory which has symlinks to the css, js etc. directories, and
displayed from there.

You'll need the `translate-toolkit` package in addition to the
utilities provided by Ubuntu MATE Welcome.

    sudo apt-get install translate-toolkit

  * `create_pots.py` - create .pot files for the slides and puts them in a `po/<slide name>` directory under `data/`
  * `create_pos.py` - for each slide, create a `.po` files for translators for every supported locale on the system. These also go in `data/po/<slide name>/`
  * `create_i18n_slides.py` - produces translated slides for everything. These end up in the `./i18n` directory
  * `country_codes.py` - contains a single function which returns a list of supported locales. Used by both `create_pos.py` and `ubuntu-mate-welcome`

To create the translated slides from scratch run `create_pots`,
followed by `create_pos`, followed by `create_i18n_slides`. If you want
to check whether the files from the correct locale are being shown by
`ubuntu-mate-welcome`, just edit the html in the `i18n/<locale of your
choice>/` directory and run `ubuntu-mate-welcome --locale=<locale of
your choice>`.