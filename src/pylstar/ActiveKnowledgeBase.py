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
from pylstar.KnowledgeBase import KnowledgeBase


@PylstarLogger
class ActiveKnowledgeBase(KnowledgeBase):
    """An abstract class that implements the main mecanism of an active knwoledge base.

    

    """

    def __init__(self):
        super(ActiveKnowledgeBase, self).__init__()

    def _execute_word(self, word):
        """Executes the specified word."""
        
        if word is None:
            raise Exception("Word cannot be None")
        
        self._logger.debug("Execute word '{}'".format(word))

        self.start_target()
        try:
            return self.submit_word(word)
        finally:
            self.stop_target()

    @abc.abstractmethod
    def start_target(self):
        raise NotImplementedError()

    @abc.abstractmethod    
    def stop_target(self):
        raise NotImplementedError()

    @abc.abstractmethod    
    def submit_word(self, word):
        raise NotImplementedError()

        
        

        

    
