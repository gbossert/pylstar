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
from pylstar.ActiveKnowledgeBase import ActiveKnowledgeBase
from pylstar.Letter import Letter, EmptyLetter
from pylstar.Word import Word


@PylstarLogger
class FakeActiveKnowledgeBase(ActiveKnowledgeBase):
    """An implementation of an active knowledge base that relies
    on a preseted automata to answer queries.

    
    >>> from pylstar.automata.State import State
    >>> from pylstar.automata.Transition import Transition
    >>> from pylstar.automata.Automata import Automata
    >>> from pylstar.Letter import Letter
    >>> from pylstar.Word import Word
    >>> from pylstar.OutputQuery import OutputQuery
    >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
    >>> l_a = Letter('a')
    >>> l_b = Letter('b')
    >>> l_c = Letter('c')
    >>> l_1 = Letter(1)
    >>> l_2 = Letter(2)
    >>> l_3 = Letter(3)
    >>> s0 = State("S0")
    >>> s1 = State("S1")
    >>> t1 = Transition("t1", output_state=s0, input_letter=l_a, output_letter=l_1)
    >>> t2 = Transition("t2", output_state=s1, input_letter=l_b, output_letter=l_2)
    >>> t3 = Transition("t3", output_state=s0, input_letter=l_c, output_letter=l_3)
    >>> s0.transitions = [t1, t2, t3]
    >>> t4 = Transition("t4", output_state=s1, input_letter=l_a, output_letter=l_1)
    >>> t5 = Transition("t5", output_state=s1, input_letter=l_b, output_letter=l_2)
    >>> t6 = Transition("t6", output_state=s0, input_letter=l_c, output_letter=l_3)
    >>> s1.transitions = [t4, t5, t6]
    >>> automata = Automata(s0)
    >>> kbase = FakeActiveKnowledgeBase(automata)
    >>> w1 = Word([l_a])
    >>> o1 = OutputQuery(w1)    
    >>> w2 = Word([l_b])
    >>> o2 = OutputQuery(w2)    
    >>> w3 = Word([l_a, l_b, l_b, l_b, l_b, l_c, l_c, l_a])
    >>> o3 = OutputQuery(w3)    
    >>> kbase.resolve_query(o1)
    >>> print(o1.output_word)
    [Letter(1)]
    >>> kbase.resolve_query(o2)
    >>> print(o2.output_word)
    [Letter(2)]
    >>> kbase.resolve_query(o3)
    >>> print(o3.output_word)
    [Letter(1), Letter(2), Letter(2), Letter(2), Letter(2), Letter(3), Letter(3), Letter(1)]

    """

    def __init__(self, automata):
        super(FakeActiveKnowledgeBase, self).__init__()
        self.automata = automata

    def start_target(self):
        self._logger.debug("Starting the fake target")

    def stop_target(self):
        self._logger.debug("Stoping the fake target")        

    def submit_word(self, word):
        self._logger.debug("Submiting word '{}' to the fake target".format(word))

        if self.automata is None:
            raise Exception("Automata cannot be None")
        
        current_state = self.automata.initial_state
        output_letters = []
        for letter in word.letters:
            try:
                (current_state, output_letter) = self._next_state(current_state, letter)
            except Exception:
                output_letter = EmptyLetter()
            
            output_letters.append(output_letter)

        output_word = Word(output_letters)
        return output_word

    def _next_state(self, current_state, letter):
        if current_state is None:
            raise Exception("Current state cannot be None")
        if letter is None:
            raise Exception("Letter cannot be None")

        if letter == EmptyLetter:
            return (current_state, EmptyLetter())

        for transition in current_state.transitions:
            if transition.input_letter == letter:
                return (transition.output_state, transition.output_letter)
        raise Exception("State '{}' accepts no transition triggered by letter '{}'".format(current_state, letter))
                
            

        
            

        
        

        

    
