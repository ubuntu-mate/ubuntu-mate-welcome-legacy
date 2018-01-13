#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <luke@ubuntu-mate.org>
#               2015-2016 Martin Wimpress <code@flexion.org>
#               2015, Larry Bushey
#

"""
Welcome Page: Features

Informs about what you can do with Ubuntu MATE.
"""

from .. import Common
from time import sleep
import os

_ = Common.setup_translations(__file__, "ubuntu-mate-welcome")


def page_enter(variables):
    """
    Triggered upon opening the page.
    """
    update_page = variables["objects"]["update_page"]
    change_page = variables["objects"]["change_page"]
    ui = variables["objects"]["ui"]

    content = ''
    content += '<div id="content" class="container-fluid entire-page-fade" tabindex="1">' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span12">' \
                '<h2>' + _("Modern and Full-Featured") + '</h2>' \
                '<p>'
    content += _("Ubuntu MATE is a modern computer operating system, with an " \
                    "attractive and easy to understand user interface. Its update " \
                    "manager keeps not only the operating system itself, but all of its " \
                    "installed applications updated to the current release. The " \
                    "operating system is more secure, and better supported than " \
                    "operating systems that come pre-installed on most home computer " \
                    "hardware today.")
    content += '</p>' \
                '</div>' \
                '</div>'

    content += '<h3 class="wow fadeIn">' + _("Pre-Configured Yet Flexible") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/control-centre.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Using Ubuntu MATE provides you with the freedom to run a " \
                    "complete, full-featured operating system, pre-configured with " \
                    "most, if not all, of the applications you will need for your daily " \
                    "computing - or to change anything about the way it looks, the way " \
                    "it works, or the applications it runs to suit your taste.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \

    content += '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Built-In Security") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/system-software-update.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Ubuntu MATE is designed with security in mind. Unlike operating " \
                    "systems that update only once a month, Ubuntu MATE receives " \
                    "updates continuously. The updates include security patches for " \
                    "Ubuntu MATE and all of its components. Security updates for all of " \
                    "its installed applications are also provided on the same schedule. " \
                    "This ensures that you have the latest protection for all of your " \
                    "computer's software -- as soon as it's available!")
    content += '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">'

    content += '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/security.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Ubuntu MATE can get viruses and other infections... but it " \
                    "doesn't. Rapid and timely updates ensure that there are very few, " \
                    "if any threats to Linux systems like Ubuntu MATE that persist in " \
                    "the wild. In reality, there have been very few \"public\" infections " \
                    "in the last 10 years that can affect Ubuntu MATE. They are no " \
                    "longer a threat to anyone installing or using a modern Linux " \
                    "distribution today. Ubuntu MATE is designed to make it difficult " \
                    "for viruses, root kits and other malware to be installed and run " \
                    "without conscious intervention by you, the user. Even if you do " \
                    "accidentally invite in an infection, chances are it's designed to " \
                    "attack Windows and won't do much, if any damage to Ubuntu MATE.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">'

    content += '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/system-config-securitylevel.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content += _("Another significant security feature of Ubuntu MATE is that its " \
                    "users are not administrators by default. Administrators (\"root\" " \
                    "users) on any computer system have permission to do anything they " \
                    "want, including the ability to damage the system.")
    content += '</p>' \
                '<p>'
    content += _("For example, other operating systems look at the name of a file " \
                    "to determine which program should open it, then immediately " \
                    "attempt to open it. That design makes it easy for an intruder to " \
                    "attack a computer. Ubuntu MATE opens a file based on what the file " \
                    "is, not based on its name. So even if a malicious program " \
                    "disguises its identity by using the name \"Last Will and " \
                    "Testament.txt\" Ubuntu MATE will recognize the file as a program. " \
                    "The system provides a warning that the file is not a text file, " \
                    "but that it is a program that will be run if you give it " \
                    "permission to continue. To be extra secure, Ubuntu MATE requires " \
                    "you to provide your administrator password before that permission " \
                    "is granted. Every single time.")
    content += '</p>' \
                '</div>' \
                '</div>'

    content += '<div class="row-fluid wow fadeIn">' \
                '<div class="span12">' \
                '<hr class="soften">' \
                '<h2>' + _("Powerful Applications") + '</h2>' \
                '<p>'
    content +=  _("While MATE Desktop provides the essential user interfaces to " \
                "control and use a computer, Ubuntu MATE adds a collection of " \
                "additional applications to turn your computer into a truly " \
                "powerful workstation.")
    content +=  '</p>' \
                '<h3>' + _("Productivity") + '</h3>' \
                '</div>' \
                '</div>'

    content +=  '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/firefox.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Firefox delivers safe, easy web browsing. A familiar user " \
                "interface, enhanced security features including protection from " \
                "online identity theft, and an integrated search to let you get the most " \
                "out of the web.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/thunderbird.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Thunderbird is a full-featured email, RSS and newsgroup client"
                "that makes emailing safer, faster and easier than ever before. It " \
                "supports different mail accounts (POP, IMAP, Gmail), has a simple " \
                "mail account setup wizard, one-click address book, tabbed " \
                "interface, an integrated learning spam filter, advanced search and " \
                "indexing capabilities, and offers easy organization of mails with " \
                "tagging and virtual folders. It also features unrivalled" \
                "extensibility.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/libreoffice.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("LibreOffice is a full-featured office productivity suite that " \
                "provides a near drop-in replacement for Microsoft(R) Office; its " \
                "clean interface and powerful tools let you unleash your creativity " \
                "and grow your productivity. LibreOffice embeds several " \
                "applications that make it the most powerful Free and Open Source " \
                "Office suite on the market:")
    content +=  '<ul>' \
'                <li><img src="img/applications/libreoffice/writer.png"/> ' + _("Writer, the word processor.") + '</li>' \
                '<li><img src="img/applications/libreoffice/calc.png"/> ' + _("Calc, the spreadsheet application.") + '</li>' \
'                <li><img src="img/applications/libreoffice/impress.png"/> ' + _("Impress, the presentation engine.") + '</li>' \
                '<li><img src="img/applications/libreoffice/draw.png"/> ' + _("Draw, the drawing and flowcharting application.") + '</li>' \
                '<li><img src="img/applications/libreoffice/base.png"/> ' + _("Base, the database and database frontend.") + '</li>' \
                '<li><img src="img/applications/libreoffice/math.png"/> ' + _("Math, for editing mathematics.") + '</li>' \
                '</ul>' \
                '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Entertainment") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/rhythmbox.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Rhythmbox is a very easy to use music playing and management " \
                "program which supports a wide range of audio formats (including " \
                "mp3 and ogg). Originally inspired by Apple's iTunes, the current " \
                "version also supports Internet Radio, iPod integration and generic " \
                "portable audio player support, Audio CD burning, Audio CD " \
                "playback, music sharing, and Podcasts.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">' \
'                <div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/shotwell.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Shotwell is a digital photo organizer. It allows you to import " \
                "photos from disk or camera, organize them in various ways, view " \
                "them in full-window or fullscreen mode, and export them to share " \
                "with others. It is able to manage a lot of different image " \
                "formats, also including raw CR2 files.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<hr class="soften-light">' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/vlc.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("VLC is the VideoLAN project's media player. It plays MPEG, "
                "MPEG-2, MPEG-4, DivX, MOV, WMV, QuickTime, WebM, FLAC, MP3, " \
                "Ogg/Vorbis files, DVDs, VCDs, podcasts, and multimedia streams " \
                "from various network sources.")
    content +=  '</p>' \
                '<p>'
    content +=  _("VLC can also be used as a streaming server that duplicates the " \
                "stream it reads and multicasts them through the network to other " \
                "clients, or serves them through HTTP.")
    content +=  '</p>' \
                '<p>'
    content +=  _("VLC has support for on-the-fly transcoding of audio and video " \
                "formats, either for broadcasting purposes or for movie format transformations.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span12">' \
                '<hr class="soften-light">' \
                '<h4 class="wow pulse center">... ' + _("And a whole lot more!") + '</h4>' \
                '<p>'
    content +=  _("Naturally you'll also find a firewall, backup " \
                "application, document/photo scanner and printer management " \
                "all included in Ubuntu MATE. And this is just the start. " \
                "The Software sections includes " \
                "best-in-class applications for most tasks and a one-click " \
                "installer for an \"App Store\" that will give you " \
                "access to thousands of applications suitable for just about " \
                "any professional or recreational pursuit.")
    content +=  '</p>' \
                '</div>' \
                '</div>'

    content +=  '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Games") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/applications/steam.png"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("In the last couple of years Linux has become a first " \
                "class gaming platform thanks to {Valve} and {Steam} bringing the " \
                "Steam platform to Linux. At the time of writing Steam has more " \
                "than 1000 high quality indie and AAA titles " \
                "available for Linux. Ubuntu MATE is fully compatible with Steam for Linux.").format(
                    Valve='<button onclick="cmd(&quot;link?http://www.valvesoftware.com&quot;)">Valve</button>',
                    Steam='<button onclick="cmd(&quot;link?http://store.steampowered.com&quot;)">Steam</button>')
    content +=  '</p>' \
                '<p>'
    content +=  _("While Steam is a major step forward for gaming on Linux, " \
                "there are also many high quality and enjoyable Open Source " \
                "games titles available for Ubuntu MATE. It doesn't matter " \
                "if you like flight simulators, motor racing, first person " \
                "shooters, jump and run or card games, you'll find something " \
                "to keep you entertained.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \

    content +=  '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Accessibility") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="img/logos/a11y.png" height="64px" width="64px"></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Making an accessible operating system was a key priority " \
                "when the Ubuntu MATE founders initially set out the goals " \
                "of the project.")
    content +=  '</p>' \
                '<p>'
    content +=  _("Ubuntu MATE is never going to be able to offer the " \
                "comprehensive integration of assistive technologies that {Sonar} " \
                "GNU/Linux provides. But Ubuntu MATE will continue to " \
                "follow their lead so that Ubuntu MATE is a viable desktop " \
                "solution where computer access is shared within a household " \
                "or business where individual needs differ.").format(
                    Sonar='<button onclick="cmd(&quot;link?http://sonargnulinux.com/&quot;">Sonar</button>')
    content +=  '</p>' \
                '</div>' \
                '</div>'

    content +=  '<hr class="soften">' \
                '<h3 class="wow fadeIn">' + _("Mobile Integration") + '</h3>' \
                '<div class="row-fluid wow fadeIn">' \
                '<div class="span2 center-inside"><img src="/usr/share/icons/Humanity/devices/48/phone.svg" width="64px" height="64px"/></div>' \
                '<div class="span10">' \
                '<p>'
    content +=  _("Currently Ubuntu MATE has the essential mobile device " \
                "support you'd expect. You can plug in a phone, media player " \
                "or digital camera and the device is automatically detected " \
                "and mounted. You can then access the files on it or sync its contents.")
    content +=  '</p>' \
                '</div>' \
                '</div>' \
                '<br><br>' \
                '</div>'

    update_page("content", "html", content)

def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    update_page = variables["objects"]["update_page"]
    pass


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]
    return False
