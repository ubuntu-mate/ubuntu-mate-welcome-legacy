#!/usr/bin/python3

import gi
import json
import os
import sys
import subprocess
from shutil import which
try:
    gi.require_version ('Snapd', '1')
    from gi.repository import Snapd
except:
    pass

# Connects on-demand
client = None
ui_callback = None

# Check we have Zenity installed.
zenity_present = which("zenity")
if not zenity_present:
    print("Zenity is not installed.")
    exit(1)


def progress_snap_cb (client, change, _, user_data):
    # Interate over tasks to determine the aggregate tasks for completion.
    total = 0
    done = 0
    for task in change.get_tasks():
        total += task.get_progress_total()
        done += task.get_progress_done()
    percent = round((done/total)*100)
    ui_callback.update_current_progress("In Progress", percent)

# FIXME: Credentials stored on disk in plain text!
def load_auth_data():
    if os.path.exists(os.path.join(os.path.expanduser('~'),'.deleteme')):
        with open(os.path.join(os.path.expanduser('~'),'.deleteme')) as stream:
            auth_data = json.load(stream)
        macaroon = auth_data['macaroon']
        discharges = auth_data['discharges']
        auth_data = Snapd.AuthData.new(macaroon, discharges)
    else:
        auth_data = None

    return auth_data

def save_auth_data(auth_data):
    macaroon = Snapd.AuthData.get_macaroon(auth_data)
    discharges = Snapd.AuthData.get_discharges(auth_data)
    data = {'macaroon': macaroon,
            'discharges': discharges}
    f = open(os.path.join(os.path.expanduser('~'),'.deleteme'), "w+")
    f.write(json.dumps(data))
    f.close()


def snap_login():
    def _ask_for_username():
        # Invite user to sign up for account.
        try:
            question = subprocess.check_output(["zenity", "--question", \
            "--title", "Authentication for Snappy", \
            "--text", "To install snaps from the Ubuntu Store (without being root), you need an Ubuntu One account.\n\nDo you have an Ubuntu One account?", \
            "--ok-label", "Continue", \
            "--cancel-label", "Sign up"]).decode("ascii")
        except subprocess.CalledProcessError:
            # Zenity produces exit code 1 on cancel.
            # Presume cancelled
            subprocess.Popen(["xdg-open", "https://login.ubuntu.com/"])

        # Prompt for username
        try:
            username = subprocess.check_output(["zenity", "--entry", \
                "--title", "Authentication for Snappy", \
                "--text", "Please enter your e-mail address for your Ubuntu One account."]).decode('ascii').replace('\n', '')
            return username
        except subprocess.CalledProcessError:
            subprocess.call(["zenity", "--error", \
            "--title", "Authentication for Snappy", \
            "--text", "No credentials were supplied. This snap cannot be installed."])
            return None

    def _ask_for_password():
        # Prompt for password
        try:
            password = subprocess.check_output(["zenity", "--password", \
            "--title", "Authentication for Snappy", \
            "--text", "Please enter your Ubuntu One password."]).decode('ascii').replace('\n', '')
            return password
        except subprocess.CalledProcessError:
            subprocess.call(["zenity", "--error", \
            "--title", "Authentication for Snappy", \
            "--text", "No credentials were supplied. This snap cannot be installed."])
            return None

    def _ask_for_2FA():
        # Get 2FA
        try:
            twofactorauth = subprocess.check_output(["zenity", "--entry", \
            "--title", "Authentication for Snappy", \
            "--text", "Please enter your 2 factor authentication code."]).decode('ascii').replace('\n', '')
            return twofactorauth
        except subprocess.CalledProcessError:
            subprocess.call(["zenity", "--error", \
            "--title", "Authentication for Snappy", \
            "--text", "No credentials were supplied. This snap cannot be installed."])
            return None

    username = _ask_for_username()
    password = _ask_for_password()

    try:
        auth_data = Snapd.login_sync(username, password, None)
    except Exception as e:
        if e.domain == 'snapd-error-quark' and e.code == Snapd.Error.TWO_FACTOR_REQUIRED:
            otp = _ask_for_2FA()
            try:
                auth_data = Snapd.login_sync(username, password, otp)
            except:
                return None
        else:
            return None

    client.set_auth_data(auth_data)
    save_auth_data(auth_data)
    return True

def is_installed(snapname):
    connect()
    try:
        client.list_one_sync(snapname)
    except Exception as e:
        return False
    else:
        return True

def snap_install(snapname):
    print("Installing")
    connect()
    client.install_sync(snapname,
                        None, # channel
                        progress_snap_cb, (None,),
                        None) # cancellable


def snap_remove(snapname):
    print("Removing")
    connect()
    client.remove_sync(snapname,
                       progress_snap_cb, (None,),
                       None) # cancellable

def connect():
    global client
    if client == None:
        client = Snapd.Client()
        client.connect_sync()

        auth_data = load_auth_data()
        if auth_data:
            client.set_auth_data(auth_data)
        else:
            snap_login()
