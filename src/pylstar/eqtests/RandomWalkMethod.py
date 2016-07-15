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
    the same transitions in the targeted automata.

    >>> from pylstar.LSTAR import LSTAR
    >>> from pylstar.automata.State import State
    >>> from pylstar.automata.Transition import Transition
    >>> from pylstar.automata.Automata import Automata
    >>> from pylstar.Letter import Letter
    >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
    >>> from pylstar.eqtests.RandomWalkMethod import RandomWalkMethod
    >>> symbol_a = "a"
    >>> symbol_b = "b"
    >>> symbol_c = "c"
    >>> symbol_1 = 1
    >>> symbol_2 = 2
    >>> symbol_3 = 3
    >>> l_a = Letter(symbol_a)
    >>> l_b = Letter(symbol_b)
    >>> l_c = Letter(symbol_c)
    >>> l_1 = Letter(symbol_1)
    >>> l_2 = Letter(symbol_2)
    >>> l_3 = Letter(symbol_3)
    >>> s0 = State("S0")
    >>> s1 = State("S1")
    >>> s2 = State("S2")
    >>> t1 = Transition("t1", output_state=s0, input_letter=l_a, output_letter=l_1)
    >>> t2 = Transition("t2", output_state=s1, input_letter=l_b, output_letter=l_2)
    >>> t3 = Transition("t3", output_state=s2, input_letter=l_c, output_letter=l_3)
    >>> s0.transitions = [t1, t2, t3]
    >>> t4 = Transition("t4", output_state=s1, input_letter=l_a, output_letter=l_2)
    >>> t5 = Transition("t5", output_state=s1, input_letter=l_b, output_letter=l_3)
    >>> t6 = Transition("t6", output_state=s0, input_letter=l_c, output_letter=l_1)
    >>> s1.transitions = [t4, t5, t6]
    >>> t7 = Transition("t7", output_state=s2, input_letter=l_a, output_letter=l_2)
    >>> t8 = Transition("t8", output_state=s2, input_letter=l_b, output_letter=l_3)
    >>> t9 = Transition("t9", output_state=s1, input_letter=l_c, output_letter=l_1)
    >>> s2.transitions = [t7, t8, t9]
    >>> automata = Automata(s0)
    >>> kbase = FakeActiveKnowledgeBase(automata)
    >>> input_vocabulary = [symbol_a, symbol_b, symbol_c]
    >>> input_letters = [Letter(s) for s in input_vocabulary]
    >>> eqTests = RandomWalkMethod(kbase, input_letters, 10000, 0.75)
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5, eqtests=eqTests)
    >>> infered_automata = lstar.learn()
    >>> print infered_automata.build_dot_code()
    digraph G {
    "0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="0"];
    "2" [shape=ellipse, style=filled, fillcolor=white, URL="2"];
    "1" [shape=ellipse, style=filled, fillcolor=white, URL="1"];
    "0" -> "0" [fontsize=5, label="a / 1", URL="t0"];
    "0" -> "1" [fontsize=5, label="b / 2", URL="t1"];
    "0" -> "2" [fontsize=5, label="c / 3", URL="t2"];
    "2" -> "2" [fontsize=5, label="a / 2", URL="t6"];
    "2" -> "2" [fontsize=5, label="b / 3", URL="t7"];
    "2" -> "1" [fontsize=5, label="c / 1", URL="t8"];
    "1" -> "1" [fontsize=5, label="a / 2", URL="t3"];
    "1" -> "1" [fontsize=5, label="b / 3", URL="t4"];
    "1" -> "0" [fontsize=5, label="c / 1", URL="t5"];
    }

    
    >>> from pylstar.LSTAR import LSTAR
    >>> from pylstar.automata.State import State
    >>> from pylstar.automata.Transition import Transition
    >>> from pylstar.automata.Automata import Automata
    >>> from pylstar.Letter import Letter
    >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
    >>> # input symbols
    >>> symbol_hello = "hello"
    >>> symbol_bye = "bye"
    >>> symbol_pass_valid = "pass valid"
    >>> symbol_pass_invalid = "pass invalid"
    >>> symbol_cmd1 = "cmd1"
    >>> symbol_cmd2 = "cmd2"
    >>> # output symbols
    >>> symbol_pass_request = "pass?"
    >>> symbol_ack = "ack"
    >>> symbol_welcome = "welcome"
    >>> symbol_error = "error"
    >>> # create a letter for each symbol
    >>> l_hello = Letter(symbol_hello)
    >>> l_bye = Letter(symbol_bye)
    >>> l_pass_valid = Letter(symbol_pass_valid)
    >>> l_pass_invalid = Letter("pass invalid")
    >>> l_cmd1 = Letter(symbol_cmd1)
    >>> l_cmd2 = Letter(symbol_cmd2)
    >>> l_welcome = Letter(symbol_welcome)
    >>> l_ack = Letter(symbol_ack)
    >>> l_pass_request = Letter(symbol_pass_request)
    >>> l_error = Letter(symbol_error)
    >>> # create the infered automata
    >>> s0 = State("S0")
    >>> s1 = State("S1")
    >>> s2 = State("S2")
    >>> t1 = Transition("t1", output_state=s1, input_letter=l_hello, output_letter=l_pass_request)
    >>> t2 = Transition("t2", output_state=s0, input_letter=l_bye, output_letter=l_ack)
    >>> t3 = Transition("t3", output_state=s0, input_letter=l_pass_valid, output_letter=l_error)
    >>> t4 = Transition("t4", output_state=s0, input_letter=l_pass_invalid, output_letter=l_error)
    >>> t5 = Transition("t5", output_state=s0, input_letter=l_cmd1, output_letter=l_error)
    >>> t6 = Transition("t6", output_state=s0, input_letter=l_cmd2, output_letter=l_error)
    >>> s0.transitions = [t1, t2, t3, t4, t5, t6]
    >>> t7 = Transition("t7", output_state=s1, input_letter=l_hello, output_letter=l_error)
    >>> t8 = Transition("t8", output_state=s0, input_letter=l_bye, output_letter=l_ack)
    >>> t9 = Transition("t9", output_state=s2, input_letter=l_pass_valid, output_letter=l_welcome)
    >>> t10 = Transition("t10", output_state=s1, input_letter=l_pass_invalid, output_letter=l_error)
    >>> t11 = Transition("t11", output_state=s1, input_letter=l_cmd1, output_letter=l_error)
    >>> t12 = Transition("t12", output_state=s1, input_letter=l_cmd2, output_letter=l_error)
    >>> s1.transitions = [t7, t8, t9, t10, t11, t12]
    >>> t13 = Transition("t13", output_state=s2, input_letter=l_hello, output_letter=l_error)
    >>> t14 = Transition("t14", output_state=s0, input_letter=l_bye, output_letter=l_ack)
    >>> t15 = Transition("t15", output_state=s2, input_letter=l_pass_valid, output_letter=l_error)
    >>> t16 = Transition("t16", output_state=s2, input_letter=l_pass_invalid, output_letter=l_error)
    >>> t17 = Transition("t17", output_state=s2, input_letter=l_cmd1, output_letter=l_ack)
    >>> t18 = Transition("t18", output_state=s2, input_letter=l_cmd2, output_letter=l_ack)
    >>> s2.transitions = [t13, t14, t15, t16, t17, t18]
    >>> automata = Automata(s0)
    >>> kbase = FakeActiveKnowledgeBase(automata)
    >>> input_vocabulary = [symbol_hello, symbol_bye, symbol_pass_valid, symbol_pass_invalid, symbol_cmd1, symbol_cmd2]
    >>> input_letters = [Letter(s) for s in input_vocabulary]
    >>> eqTests = RandomWalkMethod(kbase, input_letters, 10000, 0.75)
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5, eqtests=eqTests)
    >>> infered_automata = lstar.learn()
    >>> print infered_automata.build_dot_code()
    digraph G {
    "0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="0"];
    "1" [shape=ellipse, style=filled, fillcolor=white, URL="1"];
    "2" [shape=ellipse, style=filled, fillcolor=white, URL="2"];
    "0" -> "1" [fontsize=5, label="hello / pass?", URL="t0"];
    "0" -> "0" [fontsize=5, label="bye / ack", URL="t1"];
    "0" -> "0" [fontsize=5, label="pass valid / error", URL="t2"];
    "0" -> "0" [fontsize=5, label="pass invalid / error", URL="t3"];
    "0" -> "0" [fontsize=5, label="cmd1 / error", URL="t4"];
    "0" -> "0" [fontsize=5, label="cmd2 / error", URL="t5"];
    "1" -> "1" [fontsize=5, label="hello / error", URL="t6"];
    "1" -> "0" [fontsize=5, label="bye / ack", URL="t7"];
    "1" -> "2" [fontsize=5, label="pass valid / welcome", URL="t8"];
    "1" -> "1" [fontsize=5, label="pass invalid / error", URL="t9"];
    "1" -> "1" [fontsize=5, label="cmd1 / error", URL="t10"];
    "1" -> "1" [fontsize=5, label="cmd2 / error", URL="t11"];
    "2" -> "2" [fontsize=5, label="hello / error", URL="t12"];
    "2" -> "0" [fontsize=5, label="bye / ack", URL="t13"];
    "2" -> "2" [fontsize=5, label="pass valid / error", URL="t14"];
    "2" -> "2" [fontsize=5, label="pass invalid / error", URL="t15"];
    "2" -> "2" [fontsize=5, label="cmd1 / ack", URL="t16"];
    "2" -> "2" [fontsize=5, label="cmd2 / ack", URL="t17"];
    }



    """
    

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

        
