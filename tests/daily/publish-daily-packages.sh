#!/bin/bash
####################################################
# This script can only be ran by the owner of
# the Ubuntu MATE Welcome Daily PPA.
####################################################

# Go to repository root.
cd "$(dirname "$0")/../../"
repo_path=$(pwd)
build_path="$(mktemp -d)"
base_package="ubuntu-mate-welcome"

# Create temporary building area
cd $build_path

#####################################
# Functions
#####################################
function notify_local_user() {
    notify-send "$1" "$2" -i ubuntu-mate
}

function replace_this() {
    # $1 = Source
    # $2 = Dest.
    # $3 = File
    FileName="$3"
    FromString="$1"
    ToString="$2"
    #echo "***** Replacing '$FromString' to '$ToString' in '$FileName'." # Debugging
    find "$FileName" -type f -exec sed -i 's/'"$FromString"'/'"$ToString"'/g' {} \;
}

function delete_this {
    # $1 = String
    # $2 = File
    old="$2.old"
    new="$2"
    mv "$new" "$old"
    sed '/'"$1"'/d' "$old" > "$new"
    rm "$old"
}

#####################################
# Function for preparing builds
#####################################
function build_branch() {
    # ---- Parameters ----
    branch="$1"     # Name of Git branch, e.g. "master"
    folder="$2"     # Name of folder
    package="$3"    # Name of package to produce.
    codename="$4"   # Ubuntu version to build against.
    name="$5"       # Brief name to appear in menus.

    # What are we doing?
    echo -e "\n\n\n=============================================="
    echo " Package:    $package"
    echo " Branch:     $branch"
    echo " Codename:   $codename"
    echo " Directory:  $folder"
    echo -e "==============================================\n"

    # Prepare to build a clean copy, using local copy as base.
    cp -r "$repo_path/" "$build_path/$package/"
    cd "$package/"
    git reset --hard
    git clean -f ./
    git checkout $branch
    git pull --rebase upstream $branch

    # Don't bother if there are conflicts.
    if [ ! "$?" == "0" ]; then
        notify_local_user "Merge Failed" "Something went wrong merging upstream!\n Is the internet down? Is there a conflict? \nRefusing to build a package for '$package'."
        cd ..
        rm -rf $package/
        return
    fi

    # Don't bother with package if automatic tests fail.
    bash "$build_path/$package/perform-tests.sh"
    if [ ! "$?" == "0" ]; then
        notify-send "$package Failed" "Automatic tests did not pass." -i error
        return 1
    fi

    # Quickly clean up.
    ./clean.sh &>/dev/null

    # Preparations for packaging.
    hash="$(git rev-parse HEAD | tail -c 8)"
    version="$(date +%Y\.%m\.%d)-$codename-$hash"
    timestamp="$( date +%a,\ %d\ %b\ %Y\ %T\ +0100)"
    signed="Luke Horwell <luke@ubuntu-mate.org>"

    # Write new changelog file
    changelog=$(echo -e "$package ($version) $codename; urgency=low\n\n  * Automatic daily build.\n\n -- $signed  $timestamp")
    rm ./debian/changelog
    echo "$changelog" > ./debian/changelog

    # Update menu entries so user knows it's a development version.
    mv ubuntu-mate-welcome.desktop   ubuntu-mate-welcome.desktop.old
    mv ubuntu-mate-software.desktop  ubuntu-mate-software.desktop.old

    grep -v "Name" ubuntu-mate-welcome.desktop.old > ubuntu-mate-welcome.desktop
    grep -v "Name" ubuntu-mate-software.desktop.old > ubuntu-mate-software.desktop
    rm *.old

    echo "Name=Welcome ($name)" >> ubuntu-mate-welcome.desktop
    echo "Name=Software Boutique ($name)" >> ubuntu-mate-software.desktop

    # Do not allow actual package to be installed.
    echo "Provides: ubuntu-mate-welcome" >> ./debian/control
    echo "Conflicts: ubuntu-mate-welcome" >> ./debian/control
    echo "Replaces: ubuntu-mate-welcome" >> ./debian/control
    replace_this "\['ubuntu-mate-welcome'\]" "\['$package'\]" ./ubuntu-mate-welcome

    # Change name for packaging
    mv ./debian/ubuntu-mate-welcome.install ./debian/$package.install
    replace_this " ubuntu-mate-welcome" "\ $package" ./debian/control

    # Let's build this!
    cd "$build_path/$package/"
    debuild --no-tgz-check -S
    cd "$build_path"
    mv $package $folder

}

#####################################
# Packages to Build
#####################################
build_branch "master" "daily-yakkety" "ubuntu-mate-welcome-dev" "yakkety" "Development Build"
build_branch "xenial-ppa" "daily-xenial" "ubuntu-mate-welcome-dev" "xenial" "Development Build"

#####################################
# Upload to Launchpad
#####################################
cd "$build_path"
dput ppa:lah7/ubuntu-mate-welcome-dev *.changes


#####################################
# Clean up and finish
cd ..
rm -rf "$build_path"
notify_local_user "Daily Packages Built" "New packages will be available for Ubuntu MATE Welcome for testers shortly."
canberra-gtk-play --id="complete"
