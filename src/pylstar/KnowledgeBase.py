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
import abc

# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger
from pylstar.KnowledgeTree import KnowledgeTree


@PylstarLogger
class KnowledgeBase(object):
    """An abstract class that implements a knowledge base.

    This knowledge base stores all the query results in a tree.

    >>> from pylstar.KnowledgeBase import KnowledgeBase
    >>> from pylstar.OutputQuery import OutputQuery
    >>> from pylstar.Word import Word
    >>> from pylstar.Letter import Letter
    >>> word1 = Word([Letter('a'), Letter('b')])
    >>> query1 = OutputQuery(word1)
    >>> kbase = KnowledgeBase()
    >>> kbase.resolve_query(query1)
    Traceback (most recent call last):
    ...
    Exception: Passive inference process
    >>> word2 = Word([Letter('a'), Letter('b'), Letter('c')])
    >>> word3 = Word([Letter('1'), Letter('2'), Letter('3')])
    >>> kbase.add_word(input_word = word2, output_word = word3)
    >>> word4 = Word([Letter('a'), Letter('d'), Letter('e')])
    >>> word5 = Word([Letter('1'), Letter('4'), Letter('5')])
    >>> kbase.add_word(input_word = word4, output_word = word5)
    >>> word6 = Word([Letter('f'), Letter('g')])
    >>> word7 = Word([Letter('6'), Letter('7')])
    >>> kbase.add_word(input_word = word6, output_word = word7)
    >>> kbase.resolve_query(query1)
    >>> print query1.output_word
    [Letter('1'), Letter('2')]
    >>> word8 = Word([Letter('a'), Letter('d'), Letter('e')])
    >>> query2 = OutputQuery(word8)
    >>> kbase.resolve_query(query2)
    >>> print query2.output_word
    [Letter('1'), Letter('4'), Letter('5')]
    



    
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.knowledge_tree = KnowledgeTree()

    def __str__(self):
        return str(self.knowledge_tree)

    def resolve_query(self, query):
        """This method can be use to interogate the cache for
        the output word associated with the specified query. If no
        previous knowledge can be found for this query, the input word
        is submitted to the target.

        """
        if query is None:
            raise Exception("Query cannot be None")
        
        query.output_word = self._resolve_word(query.input_word)

    def _resolve_word(self, word):
        if word is None:
            raise Exception("Word cannot be None")

        try:
            return self.knowledge_tree.get_output_word(word)
        except Exception:        
            self._logger.debug("Knowledge base has no previous knowledge for '{}'".format(word))
            output = self._execute_word(word)
            if output is not None:
                self.knowledge_tree.add_word(input_word = word, output_word = output)
            return output
    

    def _execute_word(self, word):
        """This method must be overwritten by subclasses that implements
        an active learning process.
        """
        raise Exception("Passive inference process")
        
    def add_word(self, input_word, output_word):
        """This method stores in the knowledge base the relationship between
        the specified input_word and output_word
        """
        self._logger.debug("adding : {}".format(','.join([str(l) for l in input_word.letters])))
        self.knowledge_tree.add_word(input_word, output_word)

        

        
        

        
        

    
