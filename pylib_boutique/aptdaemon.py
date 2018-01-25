#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2015-2016 Martin Wimpress <code@flexion.org>
#           2016-2018 Luke Horwell <code@horwell.me>
#
# Software Boutique is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Software Boutique is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Software Boutique. If not, see <http://www.gnu.org/licenses/>.
#

from aptdaemon.client import AptClient
from aptdaemon.gtk3widgets import AptErrorDialog, AptConfirmDialog, AptProgressDialog
import aptdaemon.errors
from aptdaemon.enums import *

class SimpleApt(object):
    def __init__(self, packages, action, appdata=None):
        self._timeout = 100
        self.packages = packages
        self.action = action
        self.source_to_update = None
        self.update_cache = False
        self.loop = GLib.MainLoop()
        self.client = AptClient()
        self.appdata = appdata

    def on_error(self, error):
        if isinstance(error, aptdaemon.errors.NotAuthorizedError):
            # Silently ignore auth failures
            return
        elif not isinstance(error, aptdaemon.errors.TransactionFailed):
            # Catch internal errors of the client
            error = aptdaemon.errors.TransactionFailed(ERROR_UNKNOWN, str(error))
        error_dialog = AptErrorDialog(error)
        error_dialog.run()
        error_dialog.hide()

    def on_finished_fix_incomplete_install(self, transaction, status):
        self.loop.quit()
        if status == 'exit-success':
            notify_send( _("Successfully performed fix."), _("Any previously incomplete installations have been finished."), data_path + 'img/notify/fix-success.svg' )
            return True
        else:
            notify_send( _("Failed to perform fix."), _("Errors occurred while finishing an incomplete installation."), data_path + 'img/notify/fix-error.svg' )
            return False

    def on_finished_fix_broken_depends(self, transaction, status):
        self.loop.quit()
        if status == 'exit-success':
            notify_send( _("Successfully performed fix."), _("Packages with broken dependencies have been resolved."), data_path + 'img/notify/fix-success.svg')
            return True
        else:
            notify_send( _("Failed to perform fix."), _("Packages may still have broken dependencies."), data_path + 'img/notify/fix-error.svg')
            return False

    def on_finished_update(self, transaction, status):
        # Show notification if user forces cache update.
        if self.action == 'update':
            self.loop.quit()
            if status == 'exit-success':
                notify_send(_("Successfully updated cache."), _("Software is now ready to install."), data_path + 'img/notify/fix-success.svg')
                return True
            else:
                notify_send( _("Failed to update cache."), _("There may be a problem with your repository configuration."), data_path + 'img/notify/fix-error.svg')
                return False
        elif self.action == 'install':
            if status != 'exit-success':
                self.do_notify(status)
                self.loop.quit()
                return False

            GLib.timeout_add(self._timeout,self.do_install)
            return True
        elif self.action == 'upgrade':
            if status != 'exit-success':
                self.do_notify(status)
                self.loop.quit()
                return False

            GLib.timeout_add(self._timeout,self.do_upgrade)
            return True

    def on_finished_install(self, transaction, status):
        self.loop.quit()
        if status != 'exit-success':
            return False
        else:
            self.do_notify(status)

    def on_finished_remove(self, transaction, status):
        self.loop.quit()
        if status != 'exit-success':
            return False
        else:
            self.do_notify(status)

    def on_finished_upgrade(self, transaction, status):
        self.loop.quit()
        if status != 'exit-success':
            return False
        else:
            self.do_notify(status)

    def do_notify(self, status):
        # Notifications for individual applications.
        if self.program_id:
            name = program_id.name
            img = program_id.icon_path
            if not os.path.exists(img_path):
                img_path = 'package'

            dbg.stdout('Apps', 'Changed status for "' + program_id.appid + '": ' + status, 0, 3)

            # Show a different notification for Welcome Updates
            if program_id == 'ubuntu-mate-welcome' and status == 'exit-success':
                notify_send( _("Welcome will stay up-to-date."), \
                             _("Welcome and the Software Boutique are set to receive the latest updates."), \
                             os.path.join(data_path, 'img', 'welcome', 'ubuntu-mate-icon.svg'))
                return

            # Show a different notification for "Upgrade Installed Packages" fix
            if self.program_id == 'ubuntu-standard' and status == 'exit-success':
                notify_send( _("Everything is up-to-date"), \
                             _("All packages have been upgraded to the latest versions."), \
                             os.path.join(data_path, 'img', 'welcome', 'ubuntu-mate-icon.svg'))
                return

            if self.action == 'install':
                title_success   = name + ' ' + _('Installed')
                descr_success   = _("The application is now ready to use.")

                title_cancel    = name + ' ' + _("was not installed.")
                descr_cancel    = _("The operation was cancelled.")

                title_error     = name + ' ' + _("failed to install")
                descr_error     = _("There was a problem installing this application.")

            elif self.action == 'remove':
                title_success   = name + ' ' + _('Removed')
                descr_success   = _("The application has been uninstalled.")

                title_cancel    = name + ' ' + _("was not removed.")
                descr_cancel    = _("The operation was cancelled.")

                title_error     = name + ' ' + _("failed to remove")
                descr_error     = _("A problem is preventing this application from being removed.")

            elif self.action == 'upgrade':
                title_success   = name + ' ' + _('Upgraded')
                descr_success   = _("This application is set to use the latest version.")

                title_cancel    = name + ' ' + _("was not upgraded.")
                descr_cancel    = _("The application will continue to use the stable version.")

                title_error     = name + ' ' + _("failed to upgrade")
                descr_error     = _("A problem is preventing this application from being upgraded.")

            # Do not show notifications when updating the cache
            if self.action != 'update':
                if status == 'exit-success':
                    notify_send(title_success, descr_success, img_path)
                elif status == 'exit-cancelled':
                    notify_send(title_cancel, descr_cancel, img_path)
                else:
                    notify_send(title_error, descr_error, img_path)

    def do_fix_incomplete_install(self):
        dynamicapps.operations_busy = True
        # Corresponds to: dpkg --configure -a
        apt_fix_incomplete = self.client.fix_incomplete_install()
        apt_fix_incomplete.connect("finished",self.on_finished_fix_incomplete_install)

        fix_incomplete_dialog = AptProgressDialog(apt_fix_incomplete)
        fix_incomplete_dialog.run(close_on_finished=True, show_error=True,
                reply_handler=lambda: True,
                error_handler=self.on_error,
                )
        return False
        dynamicapps.operations_busy = False

    def do_fix_broken_depends(self):
        dynamicapps.operations_busy = True
        # Corresponds to: apt-get --fix-broken install
        apt_fix_broken = self.client.fix_broken_depends()
        apt_fix_broken.connect("finished",self.on_finished_fix_broken_depends)

        fix_broken_dialog = AptProgressDialog(apt_fix_broken)
        fix_broken_dialog.run(close_on_finished=True, show_error=True,
                reply_handler=lambda: True,
                error_handler=self.on_error,
                )
        return False
        dynamicapps.operations_busy = False

    def do_update(self):
        if self.source_to_update:
            apt_update = self.client.update_cache(self.source_to_update)
        else:
            apt_update = self.client.update_cache()
        apt_update.connect("finished",self.on_finished_update)
        try:
            apt_update.connect("finished",self.on_finished_update)
        except AttributeError:
            return

        if pref.get('hide-apt-progress', False):
            apt_update.run()
        else:
            update_dialog = AptProgressDialog(apt_update)
            update_dialog.run(close_on_finished=True, show_error=True,
                    reply_handler=lambda: True,
                    error_handler=self.on_error,
                    )
        return False

    def do_install(self):
        apt_install = self.client.install_packages(self.packages)
        apt_install.connect("finished", self.on_finished_install)

        if pref.get('hide-apt-progress', False):
            apt_install.run()
        else:
            install_dialog = AptProgressDialog(apt_install)
            install_dialog.run(close_on_finished=True, show_error=True,
                            reply_handler=lambda: True,
                            error_handler=self.on_error,
                            )
        return False

    def do_remove(self):
        apt_remove = self.client.remove_packages(self.packages)
        apt_remove.connect("finished", self.on_finished_remove)

        if pref.get('hide-apt-progress', False):
            apt_remove.run()
        else:
            remove_dialog = AptProgressDialog(apt_remove)
            remove_dialog.run(close_on_finished=True, show_error=True,
                            reply_handler=lambda: True,
                            error_handler=self.on_error,
                            )
        return False

    def do_upgrade(self):
        apt_upgrade = self.client.upgrade_system(True)
        apt_upgrade.connect("finished", self.on_finished_upgrade)

        upgrade_dialog = AptProgressDialog(apt_upgrade)
        upgrade_dialog.run(close_on_finished=True, show_error=True,
                        reply_handler=lambda: True,
                        error_handler=self.on_error,
                        )
        return False

    def install_packages(self):
        dynamicapps.operations_busy = True
        if self.update_cache:
            GLib.timeout_add(self._timeout,self.do_update)
        else:
            GLib.timeout_add(self._timeout,self.do_install)
        self.loop.run()
        dynamicapps.operations_busy = False

    def remove_packages(self):
        dynamicapps.operations_busy = True
        GLib.timeout_add(self._timeout,self.do_remove)
        self.loop.run()
        dynamicapps.operations_busy = False

    def upgrade_packages(self):
        dynamicapps.operations_busy = True
        if self.update_cache:
            GLib.timeout_add(self._timeout,self.do_update)
        else:
            GLib.timeout_add(self._timeout,self.do_upgrade)
        self.loop.run()
        dynamicapps.operations_busy = False

    def fix_incomplete_install(self):
        dynamicapps.operations_busy = True
        GLib.timeout_add(self._timeout,self.do_fix_incomplete_install)
        self.loop.run()
        dynamicapps.operations_busy = False

    def fix_broken_depends(self):
        dynamicapps.operations_busy = True
        GLib.timeout_add(self._timeout,self.do_fix_broken_depends)
        self.loop.run()
        dynamicapps.operations_busy = False

def update_repos():
    transaction = SimpleApt('', 'update')
    transaction.update_cache = True
    transaction.do_update()

def fix_incomplete_install():
    transaction = SimpleApt('', 'fix-incomplete-install')
    transaction.fix_incomplete_install()

def fix_broken_depends():
    transaction = SimpleApt('', 'fix-broken-depends')
    transaction.fix_broken_depends()
