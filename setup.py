#!/usr/bin/env python

# Copyright (C) 2006, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from sugar.activity import bundlebuilder

# ignored directories
bundlebuilder.IGNORE_DIRS.append(".eric4project")
bundlebuilder.IGNORE_DIRS.append(".settings")
bundlebuilder.IGNORE_DIRS.append("power")
bundlebuilder.IGNORE_DIRS.append("t")
#bundlebuilder.IGNORE_DIRS.append("pyLogoCompiler/pre-bundle-ops")

# ignored files
bundlebuilder.IGNORE_FILES.append("*.e4p")
#bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/*.sh")
bundlebuilder.IGNORE_FILES.append(".project")
bundlebuilder.IGNORE_FILES.append(".pydevproject")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/py-docstring-test.sh")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/rebuild-debug.sh")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/compiler-test.sh")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/files1.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/test-output-expected.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/files3.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/test-output-2.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/test-output-1.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/results/files2.txt")
bundlebuilder.IGNORE_FILES.append("pyLogoCompiler/pre-bundle-ops/t/cmp-test.sh")

bundlebuilder.start()
