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
class State(object):
    """Definition of a state that belongs to an automata
    """

    def __init__(self, name):
        self.name = name
        self.transitions = []

    def __str__(self):
        return self.name
        
    def visit(self, input_letter):
        """This method computes which transition can be triggered given the
        specified input_letter. It returns a tupple made of the output letter
        that is attached to the found transition and the state it reaches.
        """
        
        if input_letter is None:
            raise Exception("input letter cannot be None")

        for transition in self.transitions:
            if transition.input_letter == input_letter:
                return (transition.output_letter, transition.output_state)

        raise Exception("No transition in state '{}' could be found given letter '{}' ".format(self.name, input_letter))
                
        

    
