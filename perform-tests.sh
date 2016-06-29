#!/bin/bash
#
# Test ubuntu-mate-welcome locally.
#

repo_root=$(dirname "$0")
success=true

echo -e "\n-------- Start of Testing --------"
cd "$repo_root"

for test in "$repo_root"/tests/*.py
do
    python3 "$test"
    if [ ! "$?" == "0" ]; then
        success=false
    fi
done

echo -e "\n-------- End of Testing  --------\n"

if [ "$success" == true ]; then
    exit 0
else
    exit 1
fi
