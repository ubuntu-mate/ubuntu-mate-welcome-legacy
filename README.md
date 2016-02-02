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
  * `--simulate-arch=<ARCH>` = Simulate an architecture.
    * `i386`
    * `amd64`
    * `armvf`
    * Does not affect System Specifications page.
  * `--simulate-session=<TYPE>` = Simulate a specific type of session.
    * `live` = Accessed from a live session.
    * `guest` = Accessed from a guest session.
    * `pi` = Accessed from a Raspberry Pi.


## Requirements

  * gir1.2-gtk-3.0
  * gir1.2-notify-0.7
  * gir1.2-webkit-3.0
  * libgtk2-perl
  * policykit-1
  * python3
  * python3-apt
  * python3-aptdaemon
  * python3-aptdaemon.gtk3widgets
  * python3-gi
  * software-properties-common
