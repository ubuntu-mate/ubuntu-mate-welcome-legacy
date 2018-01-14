#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <code@horwell.me>
#               2015-2016 Martin Wimpress <code@flexion.org>
#

"""
Welcome Page: Community

Informs and provides links to the community areas.
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

    update_page("header", "show")
    update_page("footer", "show")
    update_page("main", "show")

    # Forum
    content = ui.print_title(_("Forum"))
    content += ui.print_paragraph(_("To play an active role and help shape the direction of Ubuntu MATE, " \
        "the forum is the best place to go. From here, you can talk with the Ubuntu MATE " \
        "team and other members of our growing community."))
    content += ui.print_button("https://ubuntu-mate.community", "link?https://ubuntu-mate.community", "img/welcome/ubuntu-mate-gray.svg", "green")

    # Social Networks
    content += ui.print_title(_("Social Networks"))
    content += ui.print_paragraph(_("Ubuntu MATE is active on the following social networks."))
    content += ui.print_button("Google+", "link?https://plus.google.com/communities/108331279007926658904", "img/social/google+.svg", "social")
    content += ui.print_button("Facebook", "link?https://www.facebook.com/UbuntuMATEedition/", "img/social/facebook.svg", "social")
    content += ui.print_button("Twitter", "link?https://twitter.com/ubuntu_mate", "img/social/twitter.svg", "social")

    # Chatroom
    content += ui.print_title(_("Chat with fellow users"))
    content += ui.print_paragraph(_("This IRC client is pre-configured so you can jump into our " \
                "#ubuntu-mate channel on {Freenode}.".format(
                    Freenode='<button class="link" onclick="cmd(&quot;https://freenode.net/&quot;)">Freenode</button>'))).replace("#ubuntu-mate", '<code>#ubuntu-mate</code>')
    content += ui.print_paragraph(_("Many members and users of Ubuntu MATE are on here but they have real lives too. " \
                "If you have a question, feel free to ask. However, it may take a while " \
                "for someone to reply. Just be patient and don't disconnect right away."))

    content += ui.print_button(_("Join the IRC on Hexchat"), "chatroom", "img/applications/hexchat.png", "inverse")
    content += ui.print_button(_("Join the IRC at ubuntu-mate.org/IRC"), "chatroom", "img/welcome/ubuntu-mate-gray.svg", "inverse")

    update_page("content", "append", content)
    Common.page_enter_global(variables, _("Community"))


def page_exit(variables):
    """
    Triggered upon closing the page.
    """
    Common.page_exit_global(variables)


def do_command(variables, cmd):
    """
    When a command is triggered from the page.
    Returns True if matches here.
    """
    parameters = cmd.split('?')[1:]
    return False
