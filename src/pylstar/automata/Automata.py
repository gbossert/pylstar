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
from pylstar.automata.State import State


@PylstarLogger
class Automata(object):
    """Definition of an automata
    """

    def __init__(self, initial_state, name = "Automata"):
        self.initial_state = initial_state
        self.name = name

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

    @staticmethod
    def create_from_dot_code(dot_code):
        """This statis method returns the Automata object that can represents the provided DOT code

        :param dot_code: DOT definition of the Automata to parse
        :type dot_code: str
        :rtype: pylstar.automata.Automata.Automata
        """

        if dot_code is None:
            raise Exception("Dot code cannot be None")

        if not isinstance(dot_code, str):
            raise Exception("Dot code must be a String")

        from pylstar.automata.DOTParser import DOTParser

        return DOTParser.parse(dot_code)
        
        

    def build_dot_code(self):
        """Returns the dot code representing the automata.

        :rtype: str        

        >>> from pylstar.automata.State import State
        >>> from pylstar.Letter import Letter
        >>> from pylstar.automata.Transition import Transition
        >>> la = Letter('A')
        >>> lb = Letter('B')
        >>> l0 = Letter(0)
        >>> l1 = Letter(1)
        >>> q0 = State("Q0")
        >>> q1 = State("Q1")
        >>> t0 = Transition("t0", q0, la, l0)
        >>> q0.transitions.append(t0)
        >>> t1 = Transition("t1", q1, lb, l1)
        >>> q0.transitions.append(t1)
        >>> t2 = Transition("t2", q1, la, l0)
        >>> q1.transitions.append(t2)
        >>> t3 = Transition("t3", q0, lb, l1)
        >>> q1.transitions.append(t3)
        >>> automata = Automata(initial_state = q0)
        >>> print(automata.build_dot_code())
        digraph "Automata" {
        "Q0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="Q0"];
        "Q1" [shape=ellipse, style=filled, fillcolor=white, URL="Q1"];
        "Q0" -> "Q0" [fontsize=5, label="A / 0", URL="t0"];
        "Q0" -> "Q1" [fontsize=5, label="B / 1", URL="t1"];
        "Q1" -> "Q1" [fontsize=5, label="A / 0", URL="t2"];
        "Q1" -> "Q0" [fontsize=5, label="B / 1", URL="t3"];
        }


        """
        from pylstar.automata.DOTParser import DOTParser

        return DOTParser.build_dot_code(self)

        
    @property
    def initial_state(self):
        """The initial state of the Automata"""
        return self.__initial_state

    @initial_state.setter
    def initial_state(self, state):
        if state is None:
            raise Exception("Initial state cannot be None")
        if not isinstance(state, State):
            raise Exception("Initial state must be a state")
        self.__initial_state = state

    @property
    def name(self):
        """The name of the state machine"""
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise Exception("Name of the automata cannot be None")
        if not isinstance(name, str):
            raise Exception("Name of the automata must be a String")
        self.__name = name
        

    
