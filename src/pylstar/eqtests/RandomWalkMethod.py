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
import random

# +----------------------------------------------------------------------------
# | pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Word import Word
from pylstar.OutputQuery import OutputQuery


@PylstarLogger
class RandomWalkMethod(object):
    """This algorithm performs a random walk accross the hypothesis states.
    The output symbols produced while triggering transitions are compared to the ones produced when trigerring
    the same transitions in the targeted automata"""
    

    def __init__(self, knowledge_base, input_letters, max_steps, restart_probability):
        self.knowledge_base = knowledge_base
        self.input_letters = input_letters
        self.max_steps = max_steps
        self.restart_probability = restart_probability

    def find_counterexample(self, hypothesis):
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")

        
        self._logger.info("Starting the RandomWalk Algorithm to search for a counter-example")
        
        i_step = 0
        first_step_after_restart = True
        current_state = hypothesis.initial_state

        input_word = Word()
        hypothesis_output_word = Word()
        force_restart = False
        while i_step < self.max_steps:

            # should we restart
            if not first_step_after_restart:
                if force_restart or random.random() < self.restart_probability:
                    current_state = hypothesis.initial_state
                    first_step_after_restart = True

                    counterexample_query = self.__check_equivalence(input_word, hypothesis_output_word)
                    if counterexample_query is not None:
                        return counterexample_query
                    
                    input_word = Word()
                    hypothesis_output_word = Word()
                    force_restart = False
            else:
                first_step_after_restart = False

            try:
                (new_state, input_letter, output_letter) = self.__walk(current_state)
                current_state = new_state
                input_word.letters.append(input_letter)
                hypothesis_output_word.letters.append(output_letter)
                
            except Exception, e:
                self._logger.warn(e)
                force_restart = True

            i_step += 1

    def __check_equivalence(self, input_word, expected_output_word):
        if input_word is None:
            raise Exception("Input word cannot be None")
            
        if expected_output_word is None:
            raise Exception("Expected word cannot be None")

        query = OutputQuery(input_word)
        self.knowledge_base.resolve_query(query)

        if query.output_word != expected_output_word:
            self._logger.info("Found a counter-example : input: '{}', expected: '{}', observed: '{}'".format(input_word, expected_output_word, query.output_word))
            return query
        return None

    def __walk(self, current_state):
        if current_state is None:
            raise Exception("Current state cannot be None")

        picked_transition = random.choice(current_state.transitions)
        if picked_transition is None:
            raise Exception("Found a state that accepts no more transition")
        
        (output_letter, output_state) = current_state.visit(picked_transition.input_letter)

        return (output_state, picked_transition.input_letter, output_letter)

        
