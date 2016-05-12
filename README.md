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

## Testing Arguments

Welcome does not require arguments for general usage, but for debugging
and testing purposes, the following can be specified:

#### ubuntu-mate-welcome

  * `-v` `--verbose` = Show more details to stdout.
  * `--force-arch=<ARCH>` = Simulate an architecture.
    * `i386` or `amd64` or `armvf` or `powerpc`
  * `--force-session=<TYPE>` = Simulate a specific type of session where Welcome is accessed.
    * `live` (Live Session) or `guest` (Guest User) or `pi` (Raspberry Pi 2) or `vbox` (VirtualBox)
  * `--force-codename=<NAME>` = Simulate a specific Ubuntu release. For testing Software Boutique.
    * Eg. `trusty` or `wily` or `xenial`.
  * `--force-no-net` = Simulate no internet connection.
  * `--force-net` = Simulate an internet connection.
  * `--locale` = specify a locale to use, otherwise the default locale will be used.
    * If testing translations, run `./edgar-allan translate-all` first.
  * `--software-only` = Software Boutique mode. (Hides social links, uses a larger window)
  * `--simulate-changes` = Simulate changes made to packages without modifying the system.
  * `--jump-to=<PAGE>` = Jump to a specific page, excluding the `.html` extension.
  * `--font-dpi=<NUMBER>` = Override the font size by specifying a font DPI.


#### tools/app-index-debugger.py

  * `--validate`  =  Check index for consistent data types and required values.
  * `--list-index`  =  List applications in the index.
  * `--list-broken`  =  List applications that are not working.
  * `--list-missing-codename=<RELEASE>`  =  List applications not present in a release.
  * `--list-missing-arch=<ARCH>`  =  List applications not present for an architecture.
  * `--list-special`  =  List applications that pre-install differently on releases.
  * `--list-sources`  =  List each application\'s source (eg. PPA, Ubuntu Archives)


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

## Developers

When you need to update translations do the following.

  tx pull -a
  ./welcome-po.py --update-pos
  ./edgar-allan create-all-pots
  ./edgar-allan translate-all

## Translators

If you are looking to translate the software, look in
the folders `po/` and `data/po` for PO and POT files.

 1. Fork the repository.
 2. Find an existing `.po` file to edit that language's translation
 or a `.pot` file to create a new one.
 3. Translate the strings. `poedit` is recommended.
 4. Push your changes and initiate a pull request here.

A complete guide has been written at the Ubuntu MATE Community:

 * https://ubuntu-mate.community/t/guide-how-to-translate-ubuntu-mate-welcome/4234

## Preview in another locale.

Navigate to your repository folder.

    ./edgar-allan translate-all
    ./ubuntu-mate-welcome --locale=<CODE>

Use the verbose flag (`-v`) for more detailed output on which
pages will use the translated version.

Currently, Welcome still uses English for:

  * Software Boutique - Names and descriptions for applications.
  * Terminal debug output.
  * Screenshots.

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

# Building a local package

If you want to build a local package for testing then do the following:

    sudo apt-get install python3-polib
    ./welcome-po.py --update-pos
    ./welcome-po.py --install
    ./edgar-allan translate-all
    debuild -b

The resulting `.deb` can be installed with
`sudo apt-get install ./ubuntu-mate-welcome.deb`.