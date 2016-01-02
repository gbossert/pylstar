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
    """
    A letter is a wrapper for a set of symbols. A word is made of letters.
    A symbol can be of any type (e.g. str, int, Custom class)

    >>> from pylstar.Letter import Letter
    >>> l1 = Letter("l1")
    >>> print l1
    Letter('l1')
    
    """

    def __init__(self, symbol = None, symbols = None):
        self.symbols = set()
        
        if symbol is not None:
            self.symbols.add(symbol)
        if symbols is not None:
            self.symbols.update(symbols)
            

    def __eq__(self, other):
        """Two letters are equal iif their symbols are equals

        >>> from pylstar.Letter import Letter
        >>> la = Letter("a")
        >>> lb = Letter("b")
        >>> la == lb
        False
        >>> la == "a"
        False
        >>> la == Letter("a")
        True
        """
        if not isinstance(other, Letter):
            return False
        return self.symbols == other.symbols

    def __ne__(self, other):
        """Two letters are not equal if their symbols are not equals

        >>> from pylstar.Letter import Letter
        >>> la = Letter("a")
        >>> lb = Letter("b")
        >>> la != lb
        True
        >>> la != "a"
        True
        >>> la != Letter("a")
        False
        """

        if not isinstance(other, Letter):
            return True
        return self.symbols != other.symbols
    
    def __str__(self):
        str_name = "None"
        if self.symbols is not None:
            str_name = ','.join([repr(s) for s in self.symbols])
        
        return "Letter({})".format(str_name)

    def __repr__(self):
        return self.__str__()

    @property
    def symbols(self):
        """Symbols that are represented by the letter"""
        return self.__symbols
    
    @symbols.setter
    def symbols(self, symbols):    
        self.__symbols = symbols

        
@PylstarLogger
class EmptyLetter(Letter):

    def __init__(self):
        super(EmptyLetter, self).__init__()

    def __str__(self):
        return "EmptyLetter"
