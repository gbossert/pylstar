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


# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger


@PylstarLogger
class Letter(object):

    def __init__(self, symbol = None):
        self.symbol = symbol

    def __eq__(self, other):
        if not isinstance(other, Letter):
            return False
        return self.symbol == other.symbol

    def __ne__(self, other):
        return self.symbol != other.symbol
    
    def __str__(self):
        return "Letter({})".format(self.symbol)

    def __repr__(self):
        return self.__str__()

    @property
    def symbol(self):
        """Symbol that is represented by the letter"""
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol):    
        self.__symbol = symbol

        
@PylstarLogger
class EmptyLetter(Letter):

    def __init__(self):
        super(EmptyLetter, self).__init__()

    def __str__(self):
        return "EmptyLetter"
