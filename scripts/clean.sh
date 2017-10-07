#!/usr/bin/env bash

repo_root=`realpath $(dirname "$0")/../`
cd "$repo_root"

rm -rfv __pycache__
rm -rfv data/i18n
rm -rfv locale
rm -v data/po/*/*.old
