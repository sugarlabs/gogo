#!/bin/bash

# Remove dynamically created files

PWD=`pwd`
if [ "`basename $PWD`" != "GoGo.activity" ] ; then
    echo "*** ONLY RUN IN DIRECTORY: GoGo.activity"
    exit -1
fi

find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyc" -delete
find . -type f -name lextab.py -delete
find . -type f -name parser.out -delete
find . -type f -name parsetab.py -delete

exit 0
