# -*- coding: utf-8 -*-

# +---------------------------------------------------------------------------+
# | pylstar : Implementation of the LSTAR Grammatical Inference Algorithm     |
# +---------------------------------------------------------------------------+
# | Copyright (C) 2015 Georges Bossert                                        |
# | This program is free software: you can redistribute it and/or modify      |
# | it under the terms of the GNU General Public License as published by      |
# | the Free Software Foundation, either version 3 of the License, or         |
# | (at your option) any later version.                                       |
# |                                                                           |
# | This program is distributed in the hope that it will be useful,           |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of            |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
# | GNU General Public License for more details.                              |
# |                                                                           |
# | You should have received a copy of the GNU General Public License         |
# | along with this program. If not, see <http://www.gnu.org/licenses/>.      |
# +---------------------------------------------------------------------------+
# | @url      : https://github.com/gbossert/pylstar                           |
# | @contact  : gbossert@miskin.fr                                            |
# +---------------------------------------------------------------------------+

# +----------------------------------------------------------------------------
# | Global Imports
# +----------------------------------------------------------------------------
from distutils.core import Command
import os
import sys
import unittest


class test_command(Command):
    description = "Test PYLSTAR"

    user_options = [('reportfile=', None, 'name of the generated XML report file (not required)') ]

    def initialize_options(self):
        self.reportfile = None
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in test/, and runs them.
        '''
        sys.path.insert(0, 'src/')

        sys.path.insert(0, 'test/src/')

        from common.xmlrunner import XMLTestRunner
        from test_pylstar import suite_global

        # We retrieve the current test suite
        currentTestSuite = suite_global.getSuite()

        if self.reportfile is None or len(self.reportfile) == 0:
            runner = unittest.TextTestRunner()
            runner.run(currentTestSuite)
        else:
            # We execute the test suite
            File = open(self.reportfile, 'w')
            File.write('<?xml version="1.0" encoding="utf-8"?>\n')
            reporter = XMLTestRunner(File)
            reporter.run(currentTestSuite)
            File.close()

            self.cleanFile(self.reportfile)

    def cleanFile(self, filePath):
        """Clean the file to handle non-UTF8 bytes.
        """

        aFile = open(filePath, 'r')
        data = aFile.read()
        aFile.close()

        cleanData = ""
        for c in data:
            if (0x1f < ord(c) < 0x80) or (ord(c) == 0x9) or (ord(c) == 0xa) or (ord(c) == 0xd):
                cleanData += c
            else:
                cleanData += repr(c)

        aFile = open(filePath, 'w')
        aFile.write(cleanData)
        aFile.close()
