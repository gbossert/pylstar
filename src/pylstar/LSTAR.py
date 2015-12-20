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
import itertools
from collections import deque

# +----------------------------------------------------------------------------
# | pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.ObservationTable import ObservationTable
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Word import Word
from pylstar.Letter import Letter, EmptyLetter
from pylstar.OutputQuery import OutputQuery


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
    "1,2,3,2" [shape=doubleoctagon, style=filled, fillcolor=white, URL="1,2,3,2"];
    "2,3,1,2" [shape=ellipse, style=filled, fillcolor=white, URL="2,3,1,2"];
    "2,3,1,1" [shape=ellipse, style=filled, fillcolor=white, URL="2,3,1,1"];
    "1,2,3,2" -> "1,2,3,2" [fontsize=5, label="I='Letter(a)' / O='Letter(1)'", URL="t0"];
    "1,2,3,2" -> "2,3,1,1" [fontsize=5, label="I='Letter(b)' / O='Letter(2)'", URL="t1"];
    "1,2,3,2" -> "2,3,1,2" [fontsize=5, label="I='Letter(c)' / O='Letter(3)'", URL="t2"];
    "2,3,1,2" -> "2,3,1,2" [fontsize=5, label="I='Letter(a)' / O='Letter(2)'", URL="t6"];
    "2,3,1,2" -> "2,3,1,2" [fontsize=5, label="I='Letter(b)' / O='Letter(3)'", URL="t7"];
    "2,3,1,2" -> "2,3,1,1" [fontsize=5, label="I='Letter(c)' / O='Letter(1)'", URL="t8"];
    "2,3,1,1" -> "2,3,1,1" [fontsize=5, label="I='Letter(a)' / O='Letter(2)'", URL="t3"];
    "2,3,1,1" -> "2,3,1,1" [fontsize=5, label="I='Letter(b)' / O='Letter(3)'", URL="t4"];
    "2,3,1,1" -> "1,2,3,2" [fontsize=5, label="I='Letter(c)' / O='Letter(1)'", URL="t5"];
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
    "pass?,ack,error,error,error,error" [shape=doubleoctagon, style=filled, fillcolor=white, URL="pass?,ack,error,error,error,error"];
    "error,ack,welcome,error,error,error" [shape=ellipse, style=filled, fillcolor=white, URL="error,ack,welcome,error,error,error"];
    "error,ack,error,error,ack,ack" [shape=ellipse, style=filled, fillcolor=white, URL="error,ack,error,error,ack,ack"];
    "pass?,ack,error,error,error,error" -> "error,ack,welcome,error,error,error" [fontsize=5, label="I='Letter(hello)' / O='Letter(pass?)'", URL="t12"];
    "pass?,ack,error,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(bye)' / O='Letter(ack)'", URL="t13"];
    "pass?,ack,error,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(pass valid)' / O='Letter(error)'", URL="t14"];
    "pass?,ack,error,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(pass invalid)' / O='Letter(error)'", URL="t15"];
    "pass?,ack,error,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(cmd1)' / O='Letter(error)'", URL="t16"];
    "pass?,ack,error,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(cmd2)' / O='Letter(error)'", URL="t17"];
    "error,ack,welcome,error,error,error" -> "error,ack,welcome,error,error,error" [fontsize=5, label="I='Letter(hello)' / O='Letter(error)'", URL="t6"];
    "error,ack,welcome,error,error,error" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(bye)' / O='Letter(ack)'", URL="t7"];
    "error,ack,welcome,error,error,error" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(pass valid)' / O='Letter(welcome)'", URL="t8"];
    "error,ack,welcome,error,error,error" -> "error,ack,welcome,error,error,error" [fontsize=5, label="I='Letter(pass invalid)' / O='Letter(error)'", URL="t9"];
    "error,ack,welcome,error,error,error" -> "error,ack,welcome,error,error,error" [fontsize=5, label="I='Letter(cmd1)' / O='Letter(error)'", URL="t10"];
    "error,ack,welcome,error,error,error" -> "error,ack,welcome,error,error,error" [fontsize=5, label="I='Letter(cmd2)' / O='Letter(error)'", URL="t11"];
    "error,ack,error,error,ack,ack" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(hello)' / O='Letter(error)'", URL="t0"];
    "error,ack,error,error,ack,ack" -> "pass?,ack,error,error,error,error" [fontsize=5, label="I='Letter(bye)' / O='Letter(ack)'", URL="t1"];
    "error,ack,error,error,ack,ack" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(pass valid)' / O='Letter(error)'", URL="t2"];
    "error,ack,error,error,ack,ack" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(pass invalid)' / O='Letter(error)'", URL="t3"];
    "error,ack,error,error,ack,ack" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(cmd1)' / O='Letter(ack)'", URL="t4"];
    "error,ack,error,error,ack,ack" -> "error,ack,error,error,ack,ack" [fontsize=5, label="I='Letter(cmd2)' / O='Letter(ack)'", URL="t5"];
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
    "1,2,3" [shape=doubleoctagon, style=filled, fillcolor=white, URL="1,2,3"];
    "2,3,1" [shape=ellipse, style=filled, fillcolor=white, URL="2,3,1"];
    "3,1,2" [shape=ellipse, style=filled, fillcolor=white, URL="3,1,2"];
    "1,2,3" -> "1,2,3" [fontsize=5, label="I='Letter(a)' / O='Letter(1)'", URL="t6"];
    "1,2,3" -> "3,1,2" [fontsize=5, label="I='Letter(b)' / O='Letter(2)'", URL="t7"];
    "1,2,3" -> "2,3,1" [fontsize=5, label="I='Letter(c)' / O='Letter(3)'", URL="t8"];
    "2,3,1" -> "3,1,2" [fontsize=5, label="I='Letter(a)' / O='Letter(2)'", URL="t0"];
    "2,3,1" -> "2,3,1" [fontsize=5, label="I='Letter(b)' / O='Letter(3)'", URL="t1"];
    "2,3,1" -> "1,2,3" [fontsize=5, label="I='Letter(c)' / O='Letter(1)'", URL="t2"];
    "3,1,2" -> "2,3,1" [fontsize=5, label="I='Letter(a)' / O='Letter(3)'", URL="t3"];
    "3,1,2" -> "1,2,3" [fontsize=5, label="I='Letter(b)' / O='Letter(1)'", URL="t4"];
    "3,1,2" -> "3,1,2" [fontsize=5, label="I='Letter(c)' / O='Letter(2)'", URL="t5"];
    }

    
    
    """

    def __init__(self, input_vocabulary, knowledge_base, max_states):
        self.input_letters = [Letter(symbol) for symbol in input_vocabulary]
        self.knowledge_base = knowledge_base
        self.observation_table = ObservationTable(self.input_letters, self.knowledge_base)
        self.max_states = max_states

    def learn(self):
        self._logger.info("Starting the LSTAR learning process.")

        # intialization
        self.__initialize()

        f_hypothesis_is_valid = False

        while not f_hypothesis_is_valid:        
            hypothesis = self.build_hypothesis()

            counterexample = self.find_counterexample(hypothesis)
            if counterexample is not None:
                self._logger.info("Counterexample '{}' found.".format(counterexample))
                self.fix_hypothesis(counterexample)
            else:
                f_hypothesis_is_valid = True

        self._logger.info("Automata successfully computed")
        return hypothesis

    def fix_hypothesis(self, counterexample):
        if counterexample is None:
            raise Exception("counterexample cannot be None")
        self._logger.debug("fix hypothesis with counterexample '{}'".format(counterexample))

        input_word = counterexample.input_word
        output_word = counterexample.output_word        
        self.observation_table.add_counterexample(input_word, output_word)
            
        
        

    def find_counterexample(self, hypothesis):
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")

        W = []

        states = hypothesis.get_states()
        
        # compute all couples of states
        state_couples = itertools.combinations(states, 2)

        # Constructing the characterization set W of the hypothesis
        for couple in state_couples:
            # Computes a distinguishing string for each couple of state
            W.append(self.__compute_distinguishable_string(hypothesis, couple))

        # computes P
        P = self.__computesP(hypothesis)
        self._logger.debug("P= {}".format(P))

        # computes Z
        Z = self.__computesZ(hypothesis, W)
        self._logger.debug("Z= {}".format(Z))

        # T = P . Z
        T =  P + Z
        self._logger.debug("T={}".format(T))

        # check if one of the computed testcase highlights a counterexample
        for i_testcase, testcase_query in enumerate(T[1:]):
            self._logger.debug("Executing testcase {}/{} : {}".format(i_testcase, len(T)-1, testcase_query))

            # computes the hypothesis output
            hypothesis_output_word = hypothesis.play_query(testcase_query)[0]

            self.knowledge_base.resolve_query(testcase_query)
            real_output_word = testcase_query.output_word

            self._logger.debug(real_output_word)
            self._logger.debug(hypothesis_output_word)
            if real_output_word != hypothesis_output_word:
                return testcase_query
        return None

    def __computesZ(self, hypothesis, W):    
        """it follows the formula Z= W U (X^1.W) U .... U (X^(m-1-n).W) U (W^(m-n).W)

        """
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")
        if W is None:
            raise Exception("W cannot be None")
            
        self._logger.debug("Computing Z")

        Z = []
        Z.extend(W)
        
        states = hypothesis.get_states()
        v = self.max_states - len(states)
        if v < 0:
            v = 0
        self._logger.debug("V= {}".format(v))

        output_queries = []
        for input_letter in self.input_letters:
            output_query = OutputQuery(word = Word([input_letter]))
            output_queries.append(output_query)

        X = dict()
        X[0] = W
        for i in range(1, v+1):
            self._logger.debug("Computing X^{}".format(i))
            X[i] = []
            previous_X = X[i-1]
            for x in previous_X:
                X[i].extend(x.multiply(output_queries))
            for w in W:
                for xi in X[i]:
                    if not xi in Z:
                        Z.append(xi)

        return Z

    def __computesP(self, hypothesis):
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")
        self._logger.debug("Computing P")

        P = []
            
        empty_word = Word([EmptyLetter()])
        current_query = OutputQuery(empty_word)
        P.append(current_query)

        open_queries = deque([current_query])
        close_queries = []

        seen_states = set([hypothesis.initial_state])
        while len(open_queries) > 0:
            query = open_queries.popleft()
            tmp_seen_states = set()

            for letter in self.input_letters:
                new_word = query.input_word + Word([letter])
                query_z = OutputQuery(new_word)
                (output_word, visited_states) = hypothesis.play_query(query_z)
                close_queries.append(query_z)
                
                if visited_states[-1] not in seen_states:
                    tmp_seen_states.add(visited_states[-1])
                    open_queries.append(query_z)

            seen_states.update(tmp_seen_states)

        P.extend(close_queries)

        return P
        

    def __compute_distinguishable_string(self, hypothesis, couple):
        self._logger.debug("Computes the distinguishable string for state couple '{}'".format(couple))
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")
        if couple is None:
            raise Exception("couple cannot be None")
            
        self._logger.debug("Computing distinguishing strings for states {}".format(couple))
        queries_to_test = deque([])
        
        empty_word = Word([EmptyLetter()])
        z_query = OutputQuery(empty_word)
        for letter in self.input_letters:
            new_word = z_query.input_word + Word([letter])
            queries_to_test.append(OutputQuery(new_word))

        last_indistinguishable_query = z_query
        distinguishable_query = z_query

        done = False
        i = 0
        while not done:
            query = queries_to_test.popleft()
            if i > self.max_states * self.max_states:
                break

            if not self.__is_distinguishable_states(hypothesis, query, couple):
                done = False
                last_indistinguishable_query = query
                for letter in self.input_letters:
                    new_query = OutputQuery(query.input_word + Word([letter]))
                    queries_to_test.append(new_query)
            else:
                done = True
                distinguishable_query = query

            i = i + 1

        return distinguishable_query
        
    def __is_distinguishable_states(self, hypothesis, query, couple):
        if hypothesis is None:
            raise Exception("Hypothesis cannot be None")
        if query is None:
            raise Exception("query cannot be None")
        if couple is None:
            raise Exception("couple cannot be None")

        output_word_state0 = hypothesis.play_word(query.input_word, couple[0])[0]
        output_word_state1 = hypothesis.play_word(query.input_word, couple[1])[0]
        
        return output_word_state0 != output_word_state1

    def build_hypothesis(self):        

        f_consistent = False
        f_closed = False
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

    
        
