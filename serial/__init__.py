#! /usr/bin/python 
#portable serial port access with python
#this is a wrapper module for different platform implementations
#
# (C)2001-2002 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

import sys, os, string
VERSION = '2.3'

#chose an implementation, depending on os
if os.name == 'posix':
    from serialposix import *
else:
    raise Exception(_("Sorry: no implementation for your platform ('%s') available") % os.name)
