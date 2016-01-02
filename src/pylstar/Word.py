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
from pylstar.Letter import EmptyLetter

@PylstarLogger
class Word(object):
    """A word represents a sequence of letters.

    >>> from pylstar.Word import Word
    >>> from pylstar.Letter import Letter
    >>> l1 = Letter("a")
    >>> l2 = Letter("b")
    >>> w1 = Word([l1, l2])
    >>> print w1
    [Letter('a'), Letter('b')]

    
    """

    def __init__(self, letters = None, normalize=True):

        if normalize:
            self.letters = letters
        else:
            self.letters = []
            for l in letters:
                self.letters.append(l)

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.letters == other.letters

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "[{}]".format(", ".join([str(letter) for letter in self.letters]))

    def __repr__(self):
        return "[{}]".format(", ".join([str(letter) for letter in self.letters]))

    def __len__(self):
        return len(self.letters)

    def last_letter(self):
        return self.letters[-1]

    def __add__(self, other):
        """Two words can be appended to produce a new one

        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> l1 = Letter("a")
        >>> l2 = Letter("b")
        >>> l3 = Letter("c")
        >>> l4 = Letter("d")
        >>> w1 = Word([l1, l2])
        >>> w2 = Word([l3, l4])
        >>> w3 = w1 + w2
        >>> print w3
        [Letter('a'), Letter('b'), Letter('c'), Letter('d')]


        Only two words can be added

        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> l1 = Letter("a")
        >>> w1 = Word([l1])
        >>> w2 = "data"
        >>> w3 = w1 + w2
        Traceback (most recent call last):
        ...
        Exception: Only two words can be added
        
        """

        if not isinstance(other, Word):
            raise Exception("Only two words can be added")

        if len(self.letters) >= 1 and isinstance(self.letters[0], EmptyLetter):
            return Word(self.letters[1:] + other.letters)
            
        return Word(self.letters + other.letters)

    @property
    def letters(self):
        """Letters that are embeded in the current word"""
        return self.__letters
    
    @letters.setter
    def letters(self, letters):
        if letters is None:
            letters = []

        if len(letters) > 1 and isinstance(letters[0], EmptyLetter):
            letters = letters[1:]
        
        self.__letters = []        
        for letter in letters:            
            self.__letters.append(letter)
