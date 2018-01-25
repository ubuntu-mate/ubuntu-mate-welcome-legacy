#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2015-2018 Luke Horwell <code@horwell.me>
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

import os
import json

class Preferences(object):
    def __init__(self, dbg_obj, config_name, project_name):
        """
        Prepares an object for the application to save/load persistance data.

        self.dbg_obj = Debug() object from main application.
        """
        self.dbg = dbg_obj
        self.folder_config = os.path.join(os.path.expanduser('~'), ".config", project_name)
        self.folder_cache = os.path.join(os.path.expanduser('~'), ".cache", project_name)
        self.file_path = os.path.join(self.folder_config, config_name + ".json")
        self.data = {}
        self.load_from_disk()

        if project_name == "software-boutique":
            self.revision_file = os.path.join(self.folder_cache, "revision")

    def load_from_disk(self):
        """
        Loads configuration from disk.
        Initialises the folder structure and file if necessary.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as stream:
                    self.data = json.load(stream)
            except Exception as e:
                self.dbg.stdout("Read preferences failed! File will be re-created.", self.dbg.error, 1)
                self.init_config()
        else:
            self.init_config()

    def save_to_disk(self):
        """
        Commit the data from memory to disk.
        Returns True or False depending on success/failure.
        """
        # Create file if it doesn't exist.
        if not os.path.exists(self.file_path):
            open(self.file_path, "w").close()

        # Write new data to specified file.
        if os.access(self.file_path, os.W_OK):
            f = open(self.file_path, "w+")
            f.write(json.dumps(self.data, sort_keys=True, indent=4))
            f.close()
            return True
        else:
            return False

    def write(self, key, value):
        """
        Write new data to memory.
        """
        try:
            self.data[key] = value
            self.save_to_disk()
        except:
            self.dbg.stdout("Preferences write failed: '{0}' => '{1}'".format(key, value), self.dbg.error, 1)

    def read(self, key, default_value=None):
        """
        Read data from memory.
        """
        try:
            value = self.data[key]
            return value
        except:
            # Should it be non-existent, use the default value instead.
            self.dbg.stdout("No preference found for '{0}', so writing '{1}' as default.".format(key, default_value), self.dbg.action, 2)
            self.write(key, default_value)
            return default_value

    def toggle(self, key):
        """
        Toggles a boolean stored key.
        """
        state = self.read(key, False)
        state = not state
        self.write(key, state)

    def init_config(self):
        try:
            os.makedirs(self.folder_config)
        except FileExistsError:
            pass
        self.data = {}
        if self.save_to_disk():
            self.dbg.stdout("Preferences file ready: " + self.file_path, self.dbg.success, 3)
            return True
        else:
            self.dbg.stdout("Failed to create preferences file:" + self.file_path, self.dbg.error, 1)
            return False

    # Used by Boutique only
    def init_cache(self):
        if not os.path.exists(self.folder_cache):
            os.makedirs(self.folder_cache)
            os.makedirs(self.folder_cache + "metadata")

    def get_index_revision(self):
        if not os.path.exists(self.revision_file):
            return 0
        else:
            with open(self.revision_file, "r") as f:
                return int(f.readline())

    def set_index_revision(self, new_rev):
        f = open(self.revision_file, "w")
        f.write(str(new_rev))
        f.close()
