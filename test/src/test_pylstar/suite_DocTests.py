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
import doctest

# +----------------------------------------------------------------------------
# | Local application imports
# +----------------------------------------------------------------------------
from pylstar import LSTAR
from pylstar import ObservationTable
from pylstar import Word
from pylstar import OutputQuery
from pylstar import KnowledgeBase
from pylstar import KnowledgeTree
from pylstar import ActiveKnowledgeBase
from pylstar import FakeActiveKnowledgeBase
from pylstar.automata import Automata
from pylstar import Letter
from pylstar.eqtests import RandomWalkMethod

def getSuite():
    # List of modules to include in the list of tests
    modules = [
        LSTAR,
        ObservationTable,
        Word,
        OutputQuery,
        KnowledgeBase,
        KnowledgeTree,
        ActiveKnowledgeBase,
        FakeActiveKnowledgeBase,
        Automata,
        Letter,
        RandomWalkMethod
    ]

    suite = unittest.TestSuite()
    for mod in modules:
        suite.addTest(doctest.DocTestSuite(mod))
    return suite
