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
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Word import Word
from pylstar.Letter import EmptyLetter
from pylstar.OutputQuery import OutputQuery


@PylstarLogger
class WpMethodEQ(object):
    """WPmethod algorithm used to trigger an equivalence query"""

    def __init__(self, knowledge_base, max_states, input_letters):
        self.knowledge_base = knowledge_base
        self.max_states = max_states
        self.input_letters = input_letters

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

        distinguishable_query = z_query

        done = False
        i = 0
        while not done:
            query = queries_to_test.popleft()
            if i > self.max_states * self.max_states:
                break

            if not self.__is_distinguishable_states(hypothesis, query, couple):
                done = False
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

