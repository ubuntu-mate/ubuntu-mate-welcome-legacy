# ubuntu-mate-welcome

The Ubuntu MATE Welcome application to greet both new and returning users on their first login.

## Builds

[![Build Status](https://semaphoreci.com/api/v1/lah7/ubuntu-mate-welcome/branches/master/shields_badge.svg)](https://semaphoreci.com/lah7/ubuntu-mate-welcome) for **Yakkety**

[![Build Status](https://semaphoreci.com/api/v1/lah7/ubuntu-mate-welcome/branches/xenial-ppa/shields_badge.svg)](https://semaphoreci.com/lah7/ubuntu-mate-welcome) for **Xenial**


## Features

  * **Introduce new users to the operating system.**
    * Highlight key features of Ubuntu MATE and GNU/Linux.
    * Provide quick guidelines on getting started.
    * Provide quick installation guidance.
    * Inform users of their system's specifications.
  * **Grow the Ubuntu MATE Community**
    * Links to the community forums and social networks.
    * Inform of Ubuntu MATE branded products for sale.
    * Provide details on donating to the project.
  * **Software Boutique**
    * From a pick of Ubuntu MATE's recommended software tested for the distribution.
    * Simple tools to manage packages on the system.
    * Install a package manager, such as *Ubuntu Software Center*.

Originally based on:

  * https://github.com/Antergos/antergos-welcome
  * http://blog.schlomo.schapiro.org/2014/01/apt-install.html

## Parameters

Welcome does not require parameters for general usage, but for debugging
and testing purposes, the following can be specified:

#### ubuntu-mate-welcome

```
Usage: ubuntu-mate-welcome [arguments]
  -d, --dev, --debug           Alias for --verbose and no locale.
  --font-dpi=NUMBER            Adapt zoom setting based on DPI. Default 96.
  -h, --help                   Show this help text.
  --force-arch=ARCH            Simulate a specific architecture.
                                -- Options: i386, amd64, armhf, powerpc
  --force-codename=CODENAME    Simulate a specific release.
                                -- Examples: trusty, wily, xenial
  --force-net                  Simulate a working internet connection.
  --force-no-net               Simulate no internet connection.
  --force-session=TYPE         Simulate a specific architecture.
                                -- Options: guest, live, pi, vbox
  --jump-to=PAGE               Open a specific page, excluding *.html
  --locale=CODE                Locale to use. e.g. fr_FR.
  --simulate-changes           Simulate software package changes without
                               modifying the system.
  -b, -boutique,               Open Welcome only for the software selections.
  --software-only
  -v, --verbose                Show more details to stdout (for debugging).

```


#### tools/app-index-debugger.py

This tool is for making queries on the Software Boutique's JSON database.

  * `--list-index`  =  List applications in the index.
  * `--list-broken`  =  List applications that are not working.
  * `--list-missing-codename=<RELEASE>`  =  List applications not present in a release.
  * `--list-missing-arch=<ARCH>`  =  List applications not present for an architecture.
  * `--list-special`  =  List applications that pre-install differently on releases.
  * `--list-sources`  =  List each application\'s source (eg. PPA, Ubuntu Archives)

## Tests

To perform tests against the application, see the `tests/` folder. These scripts
check the application for consistency and may even catch bugs early.

## Dependencies

  * gir1.2-gtk-3.0
  * gir1.2-notify-0.7
  * gir1.2-webkit2-4.0
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

## Translators

We are on Transifex!

* https://www.transifex.com/ubuntu-mate/ubuntu-mate-welcome/

## Testing Translations

1. Navigate to the repository folder.
2. Run `./create-translations.sh`
3. Run `./ubuntu-mate-welcome --locale=<CODE>` (e.g. `fr_FR`, `es_ES`)

## Syncing Translations

    tx pull -a
    ./welcome-po.py --update-pos
    ./edgar-allan create-all-pots
    ./edgar-allan translate-all
    tx push -s
    ./clean.sh

## Non-Translatable

The following cannot be translated:

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
  `data/i18n/<locale>/` directory as `slide_name.html`
  * `create-pot` - create a single `.pot` file (mainly for testing purposes)
  * `translate` - translate a single slide (mainly for testing purposes)
  * `po` - for each translatable string in a po file, set the
  translation to be the original string reversed (only for use when
  testing...)

Additional arguments:

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

# Building a local package

If you want to build a local package for testing then do the following:

    sudo apt-get install python3-polib
    ./welcome-po.py --update-pos
    ./welcome-po.py --install
    ./edgar-allan translate-all
    debuild -b

The resulting `.deb` can be installed with `sudo dpkg -i` or `gdebi`.
