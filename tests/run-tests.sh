#!/bin/bash
#
# Test ubuntu-mate-welcome locally.
#
# These parameters specify the length of the test:
# --quick
# --extended
#

repo_root=`realpath $(dirname "$0")/../`
cd "$repo_root"
success=true

echo -e "\n-------- Start of Tests --------"
for test in ./tests/*.py; do
    python3 "$test"
    if [ ! "$?" == "0" ]; then
        success=false
    fi
done
echo -e "\n-------- End of Tests --------\n"

if [ "$success" == true ]; then
    exit 0
else
    exit 1
fi
