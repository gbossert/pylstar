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
import tempfile
import os
from datetime import datetime
import time

# +----------------------------------------------------------------------------
# | pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.ObservationTable import ObservationTable
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Letter import Letter
from pylstar.eqtests.WpMethodEQ import WpMethodEQ
from pylstar.eqtests.RandomWalkMethod import RandomWalkMethod


@PylstarLogger
class LSTAR(object):
    """TODO : Describe here the inner working of the LSTAR Algorithm


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
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5)
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
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5)
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
    >>> t4 = Transition("t4", output_state=s2, input_letter=l_a, output_letter=l_3)
    >>> t5 = Transition("t5", output_state=s0, input_letter=l_b, output_letter=l_1)
    >>> t6 = Transition("t6", output_state=s1, input_letter=l_c, output_letter=l_2)
    >>> s1.transitions = [t4, t5, t6]
    >>> t7 = Transition("t7", output_state=s1, input_letter=l_a, output_letter=l_2)
    >>> t8 = Transition("t8", output_state=s2, input_letter=l_b, output_letter=l_3)
    >>> t9 = Transition("t9", output_state=s0, input_letter=l_c, output_letter=l_1)
    >>> s2.transitions = [t7, t8, t9]
    >>> automata = Automata(s0)
    >>> kbase = FakeActiveKnowledgeBase(automata)
    >>> input_vocabulary = [symbol_a, symbol_b, symbol_c]
    >>> lstar = LSTAR(input_vocabulary, kbase, max_states = 5)
    >>> infered_automata = lstar.learn()
    >>> print infered_automata.build_dot_code()
    digraph G {
    "0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="0"];
    "2" [shape=ellipse, style=filled, fillcolor=white, URL="2"];
    "1" [shape=ellipse, style=filled, fillcolor=white, URL="1"];
    "0" -> "0" [fontsize=5, label="a / 1", URL="t0"];
    "0" -> "1" [fontsize=5, label="b / 2", URL="t1"];
    "0" -> "2" [fontsize=5, label="c / 3", URL="t2"];
    "2" -> "1" [fontsize=5, label="a / 2", URL="t6"];
    "2" -> "2" [fontsize=5, label="b / 3", URL="t7"];
    "2" -> "0" [fontsize=5, label="c / 1", URL="t8"];
    "1" -> "2" [fontsize=5, label="a / 3", URL="t3"];
    "1" -> "0" [fontsize=5, label="b / 1", URL="t4"];
    "1" -> "1" [fontsize=5, label="c / 2", URL="t5"];
    }

    
    
    """

    def __init__(self, input_vocabulary, knowledge_base, max_states, tmp_dir=None, eqtests=None):
        """Implementation of the LSTAR algorithm.

        Per default, WPMethod is used for equivalence tests. However, one can prefer a RandomWalkMethod
        by specifying the following 'eqtests' parameter:
        
        eqtests = RandomWalkMethod(self.knowledge_base, self.input_letters, 10000, 0.7)

        """


    
        self.input_letters = [Letter(symbol) for symbol in input_vocabulary]
        self.knowledge_base = knowledge_base
        self.tmp_dir = tmp_dir
        self.observation_table = ObservationTable(self.input_letters, self.knowledge_base)
        self.max_states = max_states
        self.eqtests = eqtests
        self.__f_stop = False

    def stop(self):
        """This method can be use to trigger the end of the learning process"""
        
        self._logger.info("Stopping the LSTAR learning process.")
        self.__f_stop = True
        
    def learn(self):
        self._logger.info("Starting the LSTAR learning process.")

        # intialization
        self.__initialize()

        f_hypothesis_is_valid = False
        i_round = 1
        
        while not f_hypothesis_is_valid and not self.__f_stop:
        
            hypothesis = self.build_hypothesis(i_round)

            self.__serialize_hypothesis(i_round, hypothesis)

            counterexample = self.eqtests.find_counterexample(hypothesis)
            if counterexample is not None:
                self._logger.info("Counterexample '{}' found.".format(counterexample))
                self.fix_hypothesis(counterexample)
            else:
                f_hypothesis_is_valid = True

            i_round += 1

        self.__serialize_observation_table(i_round)

        self._logger.info("Automata successfully computed")
        return hypothesis

    def __serialize_hypothesis(self, i_round, hypothesis):
        if i_round is None:
            raise Exception("i_round cannot be None")
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")

        dot_code = hypothesis.build_dot_code()
        filepath = os.path.join(self.tmp_dir, "hypothesis_{}.dot".format(i_round))
        with open(filepath, 'w') as fd:
            fd.write(dot_code)

        self._logger.info("Hypothesis produced on round '{}' stored in '{}'".format(i_round, filepath))

    def __serialize_observation_table(self, i_round):
        if self.observation_table is None:
            raise Exception("Observation table cannot ne Bone")
        
        serialized_table = self.observation_table.serialize()
        str_date = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
        filepath = os.path.join(self.tmp_dir, "observation_table_{}_{}.raw".format(i_round, str_date))
        with open(filepath, 'w') as fd:
            fd.write(serialized_table)

        self._logger.info("Observation table serialized in '{}'".format(filepath))
        
    def fix_hypothesis(self, counterexample):
        if counterexample is None:
            raise Exception("counterexample cannot be None")
        self._logger.debug("fix hypothesis with counterexample '{}'".format(counterexample))

        input_word = counterexample.input_word
        output_word = counterexample.output_word        
        self.observation_table.add_counterexample(input_word, output_word)

    def build_hypothesis(self, i_round):
        if i_round is None:
            raise Exception("i_round cannot be None")

        f_consistent = False
        f_closed = False
        self._logger.info("Building the hypothesis ({} round)".format(i_round))
        while not f_consistent or not f_closed:

            if not self.observation_table.is_closed():
                self._logger.info("Observation table is not closed.")
                self.observation_table.close_table()
                f_closed = False
            else:
                self._logger.info("Observation table is closed")
                f_closed = True

            inconsistency = self.observation_table.find_inconsistency()
            if inconsistency is not None:
                self._logger.info("Observation table is not consistent.")
                self.observation_table.make_consistent(inconsistency)
                f_consistent = False
            else:
                self._logger.info("Observation table is consistent")
                f_consistent = True

            self.__serialize_observation_table(i_round)
                                
        self._logger.info("Hypothesis computed")
        return self.observation_table.build_hypothesis()
            

    def __initialize(self):
        """Initialization of the observation table"""
        
        self.observation_table.initialize()

        self._logger.info("Observation table is initialized")
        self._logger.info("\n"+str(self.observation_table))        

    @property
    def input_vocabulary(self):
        """Input_vocabulary to use  """
        return self.__input_vocabulary
    
    @input_vocabulary.setter
    def input_vocabulary(self, input_vocabulary):
        if input_vocabulary is None:
            raise ValueError("Input_vocabulary cannot be None")
        if len(input_vocabulary) == 0:
            raise ValueError("Input vocabulary cannot be empty")
        self.__input_vocabulary = input_vocabulary

    @property
    def knowledge_base(self):
        """Membership Knowledge_base"""
        return self.__knowledge_base
    
    @knowledge_base.setter
    def knowledge_base(self, knowledge_base):
        if knowledge_base is None:
            raise ValueError("Knowledge_base cannot be None")
        self.__knowledge_base = knowledge_base

    @property
    def tmp_dir(self):
        """Temporary directory that host serialized observation tables and hypothesis"""
        return self.__tmp_dir

    @tmp_dir.setter
    def tmp_dir(self, value):
        if value is None:
            self.__tmp_dir = tempfile.mkdtemp(prefix='pylstar_')
        else:
            self.__tmp_dir = value

    @property
    def eqtests(self):
        return self.__eqtests

    @eqtests.setter
    def eqtests(self, eqtests):
        if eqtests is None:
            self.__eqtests = WpMethodEQ(self.knowledge_base, self.max_states, self.input_letters)
        else:
            self.__eqtests = eqtests
    
        
