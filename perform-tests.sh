#!/bin/bash
#
# Test ubuntu-mate-welcome locally.
#
# These parameters specify the length of the test:
# --quick
# --extended
#

repo_root=$(dirname "$0")
success=true
cd "$repo_root"

# Determine which tests to run
tests=""
if [ "$1" == "--quick" ]; then
    tests="all-json-check.py validate-apps.py image-extensions.py check-trans-code-tags.py check-trans-page-templates.py"

elif [ "$1" == "--extended" ]; then
    for test in "$repo_root"/tests/*.py; do
        tests+=" $(basename $test)"
    done

else
    echo "Please specify one of the following:"
    echo " "
    echo " --quick      Checks for common errors and faults."
    echo " --extended   Deep test, checks remote repositories."
    exit 1
fi

# Perform each test
echo -e "\n-------- Start of Testing --------"
for test in $tests; do
    python3 "$repo_root"/tests/"$test"
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
