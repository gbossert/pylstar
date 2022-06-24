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
# | pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger



@PylstarLogger
class MultipleEqtests:
    """This class allows to combine different eqtests in an inference process.

    
    >>> from pylstar.LSTAR import LSTAR
    >>> from pylstar.automata.State import State
    >>> from pylstar.automata.Transition import Transition
    >>> from pylstar.automata.Automata import Automata
    >>> from pylstar.Letter import Letter
    >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
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
    >>> eqTests = MultipleEqtests([])
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5, eqtests=eqTests)
    >>> infered_automata = lstar.learn()
    >>> print(infered_automata.build_dot_code())
    digraph "Automata" {
    "0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="0"];
    "1" [shape=ellipse, style=filled, fillcolor=white, URL="1"];
    "0" -> "0" [fontsize=5, label="a / 1", URL="t0"];
    "0" -> "1" [fontsize=5, label="b / 2", URL="t1"];
    "0" -> "1" [fontsize=5, label="c / 3", URL="t2"];
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
    >>> from pylstar.eqtests.BDistMethod import BDistMethod
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
    >>> eqTests = MultipleEqtests([BDistMethod(kbase, input_letters, 2)])
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5, eqtests=eqTests)
    >>> infered_automata = lstar.learn()
    >>> print(infered_automata.build_dot_code())
    digraph "Automata" {
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

    """

    def __init__(self, eqtests):
        self.eqtests = eqtests

    def find_counterexample(self, hypothesis):
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")

        for eqmethod in self.eqtests:
            counterexample = eqmethod.find_counterexample(hypothesis)
            if counterexample:
                return counterexample

        return None
