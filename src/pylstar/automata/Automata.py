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
from pylstar.Word import Word


@PylstarLogger
class Automata(object):
    """Definition of an automata
    """

    def __init__(self, initial_state):
        self.initial_state = initial_state

    def play_query(self, query):
        return self.play_word(query.input_word, self.initial_state)
        
                   
        
    def play_word(self, input_word, starting_state=None):
        """This method can be used to play the specified word
        accross the current automata.
        It returns a tupple made of the output_word and the visited state
        captured while visiting the automata

        >>> from pylstar.Letter import Letter, EmptyLetter
        >>> from pylstar.Word import Word
        >>> from pylstar.automata.State import State
        >>> from pylstar.automata.Transition import Transition
        >>> from pylstar.automata.Automata import Automata
        >>> l_lambda = EmptyLetter()
        >>> l_a = Letter('a')
        >>> l_b = Letter('b')
        >>> l_0 = Letter(0)
        >>> l_1 = Letter(1)
        >>> s0 = State("S0")
        >>> s1 = State("S1")
        >>> s2 = State("S2")
        >>> s3 = State("S3")
        >>> t1 = Transition("T1", s3, l_a, l_0)
        >>> t2 = Transition("T2", s1, l_b, l_0)        
        >>> s0.transitions = [t1, t2]
        >>> t3 = Transition("T3", s0, l_a, l_1)
        >>> t4 = Transition("T4", s2, l_b, l_1)        
        >>> s1.transitions = [t3, t4]
        >>> t5 = Transition("T5", s3, l_a, l_0)
        >>> t6 = Transition("T6", s0, l_b, l_0)        
        >>> s2.transitions = [t5, t6]        
        >>> t7 = Transition("T7", s3, l_a, l_1)
        >>> t8 = Transition("T8", s3, l_b, l_1)        
        >>> s3.transitions = [t7, t8]
        >>> automata = Automata(s0)
        >>> print(automata.play_word(Word([l_a, l_a, l_a]))[0])
        [Letter(0), Letter(1), Letter(1)]
        >>> print(automata.play_word(Word([l_b, l_b, l_b]))[0])
        [Letter(0), Letter(1), Letter(0)]
        >>> print(automata.play_word(Word([l_b, l_a,  l_b, l_a, l_b]))[0])
        [Letter(0), Letter(1), Letter(0), Letter(1), Letter(0)]
        
        """

        if input_word is None or len(input_word) == 0:
            raise Exception("Input word cannot be None or empty")

        if starting_state is None:
            current_state = self.initial_state
        else:
            current_state = starting_state

        self._logger.debug("Playing word '{}'".format(input_word))

        output_letters = []
        visited_states = []
        
        for letter in input_word.letters:
            (output_letter, output_state) = current_state.visit(letter)
            output_letters.append(output_letter)
            visited_states.append(output_state)

            current_state = output_state

        output_word = Word(letters=output_letters)
        return (output_word, visited_states)        


    def get_states(self):
        """Visits the automata to discover all the available states.

        :return: a list containing all the discovered states.
        :rtype: a :class:`list`
        """

        states = []
        toAnalyze = []
        toAnalyze.append(self.initial_state)
        while (len(toAnalyze) > 0):
            currentState = toAnalyze.pop()
            if currentState is not None:
                found = False
                for tmpState in states:
                        if tmpState.name == currentState.name:
                            found = True
                if not found:
                    for transition in currentState.transitions:
                        outputState = transition.output_state
                        found = False
                        for tmpState in states:
                            if tmpState.name == outputState.name:
                                found = True
                        for tmpState in toAnalyze:
                            if tmpState.name == outputState.name:
                                found = True
                        if not found:
                            toAnalyze.append(outputState)
                    states.append(currentState)
        return states
        

    def build_dot_code(self):
        """Generates the dot code representing the automata.

        :return: a string containing the dot code of the automata.
        :rtype: a :class:`list`
        """
        dotCode = []
        dotCode.append("digraph G {")

        # First we include all the states declared in the automata
        states = self.get_states()
        for state in states:
            color = "white"

            if state == self.initial_state:
                shape = "doubleoctagon"
            else:
                shape = "ellipse"

            dotCode.append('"{0}" [shape={1}, style=filled, fillcolor={2}, URL="{3}"];'.format(state.name, shape, color, state.name))

        for inputState in states:
            for transition in inputState.transitions:
                outputState = transition.output_state
                dotCode.append('"{0}" -> "{1}" [fontsize=5, label="{2}", URL="{3}"];'.format(inputState.name, outputState.name, transition.label, transition.name))

        dotCode.append("}")

        return '\n'.join(dotCode)
        
        

        

    
