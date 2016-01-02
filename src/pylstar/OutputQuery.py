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
class OutputQuery(object):
    """An output query is a query made of an input word and an output word.
    An input word is the word that is sent to the teacher which answers with the output word

    Input and output words always have the same size, EmptyLetters can be inserted to ensure this.

    An output query cannot be created without specifing its input word
    
    >>> from pylstar.OutputQuery import OutputQuery
    >>> output_query = OutputQuery(None)
    Traceback (most recent call last):
    ...
    Exception: Input word cannot be None


    """
    

    def __init__(self, word):
        self.input_word = word
        self.output_word = None

    def is_queried(self):
        """This method returns True is the query was queried

        >>> from pylstar.OutputQuery import OutputQuery
        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> w1 = Word([Letter("a")])
        >>> output_query = OutputQuery(w1)
        >>> output_query.is_queried()
        False
        >>> print output_query
        OutputQuery(I = [Letter('a')], O = None)

        """
        return self.output_word is not None

    def __str__(self):
        return "OutputQuery(I = {}, O = {})".format(self.input_word, self.output_word)

    def multiply(self, queries):
        if queries is None:
            raise Exception("Queries cannot be None")

        return [OutputQuery(self.input_word + query.input_word) for query in queries]
        
    @property
    def input_word(self):
        """Input word that makes the query"""
        return self.__input_word
    
    @input_word.setter
    def input_word(self, input_word):
        if input_word is None:
            raise Exception("Input word cannot be None")
        
        self.__input_word = input_word


        
        
