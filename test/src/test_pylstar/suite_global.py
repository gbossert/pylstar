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
import unittest
import sys
from common.xmlrunner import XMLTestRunner

# +----------------------------------------------------------------------------
# | Local Application Imports
# +----------------------------------------------------------------------------
from test_pylstar import suite_DocTests


def getSuite():
    globalSuite = unittest.TestSuite()

    modulesOfTests = []
    modulesOfSuites = [
        suite_DocTests,  # tests extracted from docstrings (doctests)
    ]

    # Add individual tests
    for module in modulesOfTests:
        globalSuite.addTests(unittest.TestLoader().loadTestsFromModule(module))

    # Add suites
    for module in modulesOfSuites:
        globalSuite.addTests(module.getSuite())

    return globalSuite

if __name__ == "__main__":
    # Output is given through argument.
    # If no argument: output to stdout
    outputStdout = True

    if (len(sys.argv) == 2):
        outputStdout = False
        reportFile = sys.argv[1]

    # We retrieve the current test suite
    currentTestSuite = getSuite()

    # We execute the test suite
    if outputStdout:
        runner = unittest.TextTestRunner()
        testResult = runner.run(currentTestSuite)
    else:
        File = open(reportFile, "w")
        reporter = XMLTestRunner(File)
        reporter.run(currentTestSuite)
        File.close()
