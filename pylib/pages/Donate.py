#!/usr/bin/env python3
#
# Ubuntu MATE Welcome is licensed under the GPLv3.
#
# Copyright (C) 2015-2018 Luke Horwell <code@horwell.me>
#               2015-2016 Martin Wimpress <code@flexion.org>
#

"""
Welcome Page: Donate

Provides links on how to donate to support development, as well as
monthly donation reports.
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
    ui = variables["objects"]["ui"]
    run_js = variables["objects"]["run_js"]

    content = ui.print_title(_("Donate Today"))
    content += ui.print_paragraph(_("Ubuntu MATE is funded by our community. Your donations help pay towards:"))
    content += ui.print_list([
                    _("Web hosting and bandwidth costs."),
                    _("Supporting Open Source projects that Ubuntu MATE depends upon."),
                    _("Eventually pay for full time developers of Ubuntu MATE and MATE Desktop.")
                ])

    content += ui.print_paragraph(_("{Patreon} is a unique way to fund an Open Source project. A" \
                  "regular monthly income ensures sustainability for the Ubuntu" \
                  "MATE project. Patrons will be rewarded with exclusive project" \
                  "news, updates and invited to participate in video conferences" \
                  "where you can talk to the developers directly.").format(Patreon='<b>Patreon</b>'))

    content += ui.print_paragraph(_("If you would prefer to use {PayPal} then we have options to" \
                  "donate monthly or make a one off donation. Finally, we also accept" \
                  "donations via {Bitcoin}.").format(Bitcoin='<b>Bitcoin</b>', PayPal='<b>PayPal</b>'))

    content += ui.print_button(_("Become a Patron"), "link?http://www.patreon.com/ubuntu_mate", "usd")
    content += ui.print_button(_("Donate with PayPal"), "link?https://ubuntu-mate.org/donate/", "paypal")
    content += ui.print_button(_("Donate with Bitcoin"), "link?http://www.patreon.com/ubuntu_mate", "bitcoin")

    content += ui.print_paragraph(_("Commercial sponsorship is also available. Click the {Patreon} button above to find out more").format(
                Patreon=ui.print_link(_("Become a Patron"), "link?http://www.patreon.com/ubuntu_mate")))

    content += ui.print_horizontal_line()

    content += ui.print_subtitle(_("Our Supporters"))
    content += ui.print_paragraph(_("Thank you!"))
    content += ui.print_paragraph(_("Every month, we compile a list of our donations and detail how they are spent."))
    content += ui.print_paragraph(_("This information is published monthly to the {Blog} which you can take a look below.").format(
                Blog=ui.print_link(_("Ubuntu MATE Blog"), "link?http://ubuntu-mate.org/blog/")))

    # Initalise donations table
    content += "<table id='donationTable' class='table table-hover'></table>"

    month_short_string_dict = {}
    month_long_string_dict = {}

    month_id = 0
    for month in [_("January"), _("February"), _("March"), _("April"), _("May"), _("June"), _("July"), _("August"), _("September"), _("October"), _("November"), _("December")]:
        month_long_string_dict[month_id] = month
        month_short_string_dict[month_id] = month[:3]
        month_id += 1

    # Populate page contents
    update_page("content", "html", content)
    Common.page_enter_global(variables, _("Donate"))


    run_js("initDonateTable({0}, {1})".format(str(month_short_string_dict), str(month_long_string_dict)))


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
