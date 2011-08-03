#!/bin/bash

# Remove dynamically created files

PWD=`pwd`
#if [ "`basename $PWD`" != "GoGo.activity" ] ; then
if [ ! -f "GoGoActivity.py" ] ; then
    echo "*** ONLY RUN IN ACTIVITY DIRECTORY"
    exit -1
fi

find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyc" -delete
find . -type f -name lextab.py -delete
find . -type f -name parser.out -delete
find . -type f -name parsetab.py -delete

exit 0
