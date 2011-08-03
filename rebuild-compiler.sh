#!/bin/bash

# This script is preparation for creating an OLPC Sugar activity
# bundle. It ensures all dynamically created files are pre-created.
# See READ-ME-OR-WEEP.txt for more info. 

# First check Python is not removing DOC-STRINGS (required by PLY)
if [ "`python py-docstring-test.py`" == "There are no doc-strings! :-(" ] ; then
    echo "Python is removing DOC-STRINGS required by PLY!"
    exit -1
fi

# Clean out dynamically created files. Run test twice to regenerate.
./clean.sh
python compiler-test.py
python compiler-test.py

exit 0
