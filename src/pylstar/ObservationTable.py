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
import collections
import itertools
    
# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Letter import Letter, EmptyLetter
from pylstar.Word import Word
from pylstar.OutputQuery import OutputQuery
from pylstar.automata.State import State
from pylstar.automata.Automata import Automata
from pylstar.automata.Transition import Transition



@PylstarLogger
class ObservationTable(object):
    """An observation table consists in a two-dimensional table,
    with rows indexed by prefixes and columns indexed by suffixes.
    Prefixes are divided in two parts, short (S) and long prefixes (SA).

    The content of the observation table is stored in the internal variable 'ot_content'
    such that :
    - O : the set of output letters
    - D : the set of input letters a.k.a Distinguising Set
    - S : the set of short prefixes
    - SA : the set of long prefixes    
    - ot_content : D x {S,SA} -> O
    
    """
    
    def __init__(self, input_letters, knowledge_base):
        self.input_letters = input_letters
        self.knowledge_base = knowledge_base

        self.initialized = False
        self.D = []
        self.S = []
        self.SA = []
        self.ot_content = dict()
        
    def initialize(self):        
        self._logger.debug("Initialization of the observation table""")
        
        if self.initialized:
            raise Exception("Observation table is already initialized")

        self.initialized = True

        self.D = []
        self.S = []
        self.SA = []
        self.ot_content = dict()

        # creates a word for each input letter and register it in D
        for letter in self.input_letters:
            self.__add_word_in_D(Word([letter]))

        # creates a word that contains an EmptyLetter and registers it in S
        self.__add_word_in_S(Word([EmptyLetter()]))
    
        #for letter in self.input_letters:
        #     self.__add_word_in_SA(Word([letter]))

    def find_inconsistency(self):
        """This method returns the inconsistency found in the observation table.
        Returns None if the table is consistent.

        A table is said consistent if every equivalent pair of rows in S remains equivalent
        in SA after appending any symbol of the input vocabulary.

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> from pylstar.Letter import Letter, EmptyLetter
        >>> from pylstar.Word import Word        
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> l_lambda = EmptyLetter()
        >>> l_a = Letter('a')
        >>> l_b = Letter('b')
        >>> ot.input_letters = [l_a, l_b]
        >>> l_0 = Letter(0)
        >>> l_1 = Letter(1)
        >>> w_lambda = Word([l_lambda])
        >>> w_a = Word([l_a])
        >>> w_b = Word([l_b])
        >>> w_aa = Word([l_a, l_a])
        >>> w_ab = Word([l_a, l_b])
        >>> w_ba = Word([l_b, l_a])
        >>> w_bb = Word([l_b, l_b])
        >>> w_0 = Word([l_0])
        >>> w_1 = Word([l_1])        
        >>> ot.D = [w_a, w_b]
        >>> ot.S = [w_lambda, w_a, w_b]
        >>> ot.SA = [w_aa, w_ab, w_ba, w_bb]
        >>> ot.ot_content[w_a] = dict()
        >>> ot.ot_content[w_a][w_lambda] = w_0
        >>> ot.ot_content[w_a][w_a] = w_0
        >>> ot.ot_content[w_a][w_b] = w_1
        >>> ot.ot_content[w_a][w_aa] = w_1
        >>> ot.ot_content[w_a][w_ab] = w_1
        >>> ot.ot_content[w_a][w_ba] = w_0
        >>> ot.ot_content[w_a][w_bb] = w_0
        >>> ot.ot_content[w_b] = dict()
        >>> ot.ot_content[w_b][w_lambda] = w_0
        >>> ot.ot_content[w_b][w_a] = w_0
        >>> ot.ot_content[w_b][w_b] = w_1
        >>> ot.ot_content[w_b][w_aa] = w_1
        >>> ot.ot_content[w_b][w_ab] = w_1
        >>> ot.ot_content[w_b][w_ba] = w_0
        >>> ot.ot_content[w_b][w_bb] = w_0
        >>> print ot #doctest: +NORMALIZE_WHITESPACE
                               | [Letter(a)] | [Letter(b)]
        ---------------------- | ----------- | -----------
        [EmptyLetter]          | [Letter(0)] | [Letter(0)]
        [Letter(a)]            | [Letter(0)] | [Letter(0)]
        [Letter(b)]            | [Letter(1)] | [Letter(1)]
        ~~~                    | ~~~         | ~~~
        [Letter(a), Letter(a)] | [Letter(1)] | [Letter(1)]
        [Letter(a), Letter(b)] | [Letter(1)] | [Letter(1)]
        [Letter(b), Letter(a)] | [Letter(0)] | [Letter(0)]
        [Letter(b), Letter(b)] | [Letter(0)] | [Letter(0)]
        ---------------------- | ----------- | -----------        
        >>> print ot.find_inconsistency()
        ((([Letter(a)], [EmptyLetter]), Letter(a)), [Letter(a)])
        >>> w_aaa = Word([l_a, l_a, l_a])
        >>> w_aab = Word([l_a, l_a, l_b])
        >>> ot.S.append(w_aa)
        >>> ot.SA.remove(w_aa)
        >>> ot.SA.extend([w_aaa, w_aab])
        >>> ot.ot_content[w_a][w_aa] = w_0
        >>> ot.ot_content[w_b][w_aa] = w_0
        >>> ot.ot_content[w_a][w_aaa] = w_1
        >>> ot.ot_content[w_b][w_aaa] = w_0
        >>> ot.ot_content[w_a][w_aab] = w_1 
        >>> ot.ot_content[w_b][w_aab] = w_1               
        >>> print ot #doctest: +NORMALIZE_WHITESPACE
                                          | [Letter(a)] | [Letter(b)]
        --------------------------------- | ----------- | -----------
        [EmptyLetter]                     | [Letter(0)] | [Letter(0)]
        [Letter(a)]                       | [Letter(0)] | [Letter(0)]
        [Letter(b)]                       | [Letter(1)] | [Letter(1)]
        [Letter(a), Letter(a)]            | [Letter(0)] | [Letter(0)]
        ~~~                               | ~~~         | ~~~
        [Letter(a), Letter(b)]            | [Letter(1)] | [Letter(1)]
        [Letter(b), Letter(a)]            | [Letter(0)] | [Letter(0)]
        [Letter(b), Letter(b)]            | [Letter(0)] | [Letter(0)]
        [Letter(a), Letter(a), Letter(a)] | [Letter(1)] | [Letter(0)]
        [Letter(a), Letter(a), Letter(b)] | [Letter(1)] | [Letter(1)]
        --------------------------------- | ----------- | -----------
        >>> print ot.find_inconsistency()
        ((([Letter(a)], [Letter(a), Letter(a)]), Letter(a)), [Letter(a)])


        """
        self._logger.debug("Computes if the observation table is consistent.")

        # find all rows in S
        rows_in_S = {s: self.__get_row(s) for s in self.S}

        # identify all equivalent rows in S
        S_with_same_rows = collections.defaultdict(list)
        for word_in_s, row_s in rows_in_S.iteritems():
            S_with_same_rows[','.join([str(w) for w in row_s])].append(word_in_s)

        # check all equivalent in S are also equivalent in SA for each
        for row_in_S, eq_words_in_S in S_with_same_rows.iteritems():
            if len(eq_words_in_S) > 1:
                for pair_eq_words_in_S in itertools.combinations(eq_words_in_S, 2):
                    inconsistency = self.__is_prefixes_equivalent(pair_eq_words_in_S)
                    if inconsistency is not None:
                        suffix, inconsistency_detail = inconsistency
                        return ((pair_eq_words_in_S, suffix), inconsistency_detail)
        return None

    def __is_prefixes_equivalent(self, eq_words_in_S):
        """This method checks that the specified prefixes are equivalent.

        It returns None, if all the prefixes share the same row value given any
        input letters it get suffixed with
        Returns the letter that makes the eq_words_in_S not equivalent

        """

        if len(eq_words_in_S) < 2:
            raise Exception("At least two words must be provided")

        self._logger.debug("Checking if words '{}' are equivalents".format(','.join([str(s) for s in eq_words_in_S])))

        for input_letter in self.input_letters:
            initial_suffixed_word = Word(eq_words_in_S[0].letters + [input_letter])
            for eq_word_in_S in eq_words_in_S[1:]:                
                eq_suffixed_word = Word(eq_word_in_S.letters + [input_letter])
                for word_in_D in self.D:
                    self._logger.debug(type(word_in_D))
                    if self.ot_content[word_in_D][eq_suffixed_word] !=  self.ot_content[word_in_D][initial_suffixed_word]:
                        return (input_letter, word_in_D)
                
        return None

    def add_counterexample(self, input_word, output_word):
        """This method register the specified counterexample in the observation table.

        In details, it insert all the prefixes of the counterexample to the upper part of the table.
        It also extend SA accordingly.

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
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
        >>> kbase = FakeActiveKnowledgeBase(automata)
        >>> ot = ObservationTable(input_letters = [l_a, l_b], knowledge_base = kbase)
        >>> ot.initialize()
        >>> print ot
                      | [Letter(a)] | [Letter(b)]
        ------------- | ----------- | -----------
        [EmptyLetter] | Letter(0)   | Letter(0)  
        ~~~           | ~~~         | ~~~        
        [Letter(a)]   | Letter(1)   | Letter(1)  
        [Letter(b)]   | Letter(1)   | Letter(1)  
        ------------- | ----------- | -----------
        >>> print ot.is_closed()
        False
        >>> ot.close_table()
        >>> print ot
                               | [Letter(a)] | [Letter(b)]
        ---------------------- | ----------- | -----------
        [EmptyLetter]          | Letter(0)   | Letter(0)  
        [Letter(a)]            | Letter(1)   | Letter(1)  
        ~~~                    | ~~~         | ~~~        
        [Letter(b)]            | Letter(1)   | Letter(1)  
        [Letter(a), Letter(a)] | Letter(1)   | Letter(1)  
        [Letter(a), Letter(b)] | Letter(1)   | Letter(1)  
        ---------------------- | ----------- | -----------
        >>> counter_input_word = Word([l_b, l_b, l_b])
        >>> counter_output_word = Word([l_0, l_1, l_0])
        >>> ot.add_counterexample(counter_input_word, counter_output_word)
        >>> print ot
                                                     | [Letter(a)] | [Letter(b)]
        -------------------------------------------- | ----------- | -----------
        [EmptyLetter]                                | Letter(0)   | Letter(0)  
        [Letter(a)]                                  | Letter(1)   | Letter(1)  
        [Letter(b)]                                  | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b)]                       | Letter(0)   | Letter(0)  
        [Letter(b), Letter(b), Letter(b)]            | Letter(0)   | Letter(0)  
        ~~~                                          | ~~~         | ~~~        
        [Letter(a), Letter(a)]                       | Letter(1)   | Letter(1)  
        [Letter(a), Letter(b)]                       | Letter(1)   | Letter(1)  
        [Letter(b), Letter(a)]                       | Letter(0)   | Letter(0)  
        [Letter(b), Letter(b), Letter(a)]            | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b), Letter(b), Letter(a)] | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b), Letter(b), Letter(b)] | Letter(1)   | Letter(1)  
        -------------------------------------------- | ----------- | -----------
        
        """

        
        if input_word is None or len(input_word) == 0:
            raise Exception("Input word cannot be None or empty")
        if output_word is None or len(output_word) == 0:
            raise Exception("Output word cannot be None or empty")
        if len(input_word) != len(output_word):
            raise Exception("Output word must have the same length then input word")

        for len_prefix in range(1, len(input_word)+1):
            prefix_input = Word(input_word.letters[:len_prefix])
            if prefix_input not in self.S:
                if prefix_input in self.SA:
                    self.remove_row(prefix_input)

                self.__add_word_in_S(prefix_input)

    def remove_row(self, row):
        if row is None:
            raise Exception("Row cannot be None")
        if row in self.S:
            self.S.remove(row)
        if row in self.SA:
            self.SA.remove(row)

        for word_in_D in self.D:
            cel = self.ot_content[word_in_D]
            try:
                cel[row] = None
            except: pass
            

        

    def make_consistent(self,inconsistency):
        """This method makes consistent the observation table.

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
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
        >>> kbase = FakeActiveKnowledgeBase(automata)
        >>> ot = ObservationTable(input_letters = [l_a, l_b], knowledge_base = kbase)
        >>> ot.initialize()
        >>> print ot
                      | [Letter(a)] | [Letter(b)]
        ------------- | ----------- | -----------
        [EmptyLetter] | Letter(0)   | Letter(0)  
        ~~~           | ~~~         | ~~~        
        [Letter(a)]   | Letter(1)   | Letter(1)  
        [Letter(b)]   | Letter(1)   | Letter(1)  
        ------------- | ----------- | -----------
        >>> print ot.is_closed()
        False
        >>> ot.close_table()
        >>> print ot
                               | [Letter(a)] | [Letter(b)]
        ---------------------- | ----------- | -----------
        [EmptyLetter]          | Letter(0)   | Letter(0)  
        [Letter(a)]            | Letter(1)   | Letter(1)  
        ~~~                    | ~~~         | ~~~        
        [Letter(b)]            | Letter(1)   | Letter(1)  
        [Letter(a), Letter(a)] | Letter(1)   | Letter(1)  
        [Letter(a), Letter(b)] | Letter(1)   | Letter(1)  
        ---------------------- | ----------- | -----------
        >>> counter_input_word = Word([l_b, l_b, l_b])
        >>> counter_output_word = Word([l_0, l_1, l_0])
        >>> ot.add_counterexample(counter_input_word, counter_output_word)
        >>> print ot
                                                     | [Letter(a)] | [Letter(b)]
        -------------------------------------------- | ----------- | -----------
        [EmptyLetter]                                | Letter(0)   | Letter(0)  
        [Letter(a)]                                  | Letter(1)   | Letter(1)  
        [Letter(b)]                                  | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b)]                       | Letter(0)   | Letter(0)  
        [Letter(b), Letter(b), Letter(b)]            | Letter(0)   | Letter(0)  
        ~~~                                          | ~~~         | ~~~        
        [Letter(a), Letter(a)]                       | Letter(1)   | Letter(1)  
        [Letter(a), Letter(b)]                       | Letter(1)   | Letter(1)  
        [Letter(b), Letter(a)]                       | Letter(0)   | Letter(0)  
        [Letter(b), Letter(b), Letter(a)]            | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b), Letter(b), Letter(a)] | Letter(1)   | Letter(1)  
        [Letter(b), Letter(b), Letter(b), Letter(b)] | Letter(1)   | Letter(1)  
        -------------------------------------------- | ----------- | -----------
        >>> inconsistency = ot.find_inconsistency()
        >>> print inconsistency
        ((([Letter(b), Letter(b)], [Letter(b), Letter(b), Letter(b)]), Letter(b)), [Letter(a)])
        >>> ot.make_consistent(inconsistency)
        >>> print ot #doctest: +NORMALIZE_WHITESPACE
                                                     | [Letter(a)] | [Letter(b)] | [Letter(b), Letter(a)]
        -------------------------------------------- | ----------- | ----------- | ----------------------
        [EmptyLetter]                                | Letter(0)   | Letter(0)   | Letter(1)
        [Letter(a)]                                  | Letter(1)   | Letter(1)   | Letter(1)
        [Letter(b)]                                  | Letter(1)   | Letter(1)   | Letter(0)
        [Letter(b), Letter(b)]                       | Letter(0)   | Letter(0)   | Letter(0)
        [Letter(b), Letter(b), Letter(b)]            | Letter(0)   | Letter(0)   | Letter(1)
        ~~~                                          | ~~~         | ~~~         | ~~~
        [Letter(a), Letter(a)]                       | Letter(1)   | Letter(1)   | Letter(1)
        [Letter(a), Letter(b)]                       | Letter(1)   | Letter(1)   | Letter(1)
        [Letter(b), Letter(a)]                       | Letter(0)   | Letter(0)   | Letter(1)
        [Letter(b), Letter(b), Letter(a)]            | Letter(1)   | Letter(1)   | Letter(1)
        [Letter(b), Letter(b), Letter(b), Letter(a)] | Letter(1)   | Letter(1)   | Letter(1)
        [Letter(b), Letter(b), Letter(b), Letter(b)] | Letter(1)   | Letter(1)   | Letter(0)
        -------------------------------------------- | ----------- | ----------- | ----------------------
        >>> print ot.find_inconsistency()
        None
        >>> print ot.is_closed()
        True
        >>> automata = ot.build_hypothesis()
        >>> print automata.build_dot_code()
        digraph G {
        "0,0,1" [shape=doubleoctagon, style=filled, fillcolor=white, URL="0,0,1"];
        "1,1,0" [shape=ellipse, style=filled, fillcolor=white, URL="1,1,0"];
        "0,0,0" [shape=ellipse, style=filled, fillcolor=white, URL="0,0,0"];
        "1,1,1" [shape=ellipse, style=filled, fillcolor=white, URL="1,1,1"];
        "0,0,1" -> "1,1,1" [fontsize=5, label="I=\'Letter(a)\' / O=\'Letter(0)\'", URL="t2"];
        "0,0,1" -> "1,1,0" [fontsize=5, label="I=\'Letter(b)\' / O=\'Letter(0)\'", URL="t3"];
        "1,1,0" -> "0,0,1" [fontsize=5, label="I=\'Letter(a)\' / O=\'Letter(1)\'", URL="t4"];
        "1,1,0" -> "0,0,0" [fontsize=5, label="I=\'Letter(b)\' / O=\'Letter(1)\'", URL="t5"];
        "0,0,0" -> "1,1,1" [fontsize=5, label="I=\'Letter(a)\' / O=\'Letter(0)\'", URL="t0"];
        "0,0,0" -> "0,0,1" [fontsize=5, label="I=\'Letter(b)\' / O=\'Letter(0)\'", URL="t1"];
        "1,1,1" -> "1,1,1" [fontsize=5, label="I=\'Letter(a)\' / O=\'Letter(1)\'", URL="t6"];
        "1,1,1" -> "1,1,1" [fontsize=5, label="I=\'Letter(b)\' / O=\'Letter(1)\'", URL="t7"];
        }

        """

        if inconsistency is None:
            raise Exception("Inconsistency cannot be None")
        # verify both words of inconsistency share the same last letter        
        suffix = inconsistency[0][1]
        inconsistent_suffix = inconsistency[1]

        new_col_word = Word([suffix] + inconsistent_suffix.letters)
        self.__add_word_in_D(new_col_word)
        

    def is_closed(self):
        """This method returns True if the observation table is closed.

        The Observation table is said closed if all the rows in SA also exist in S.

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> from pylstar.Letter import Letter, EmptyLetter
        >>> from pylstar.Word import Word        
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> ot.initialize()
        >>> l_lambda = EmptyLetter()
        >>> l_a = Letter('a')
        >>> l_b = Letter('b')
        >>> l_0 = Letter(0)
        >>> l_1 = Letter(1)
        >>> w_lambda = Word([l_lambda])
        >>> w_a = Word([l_a])
        >>> w_b = Word([l_b])
        >>> w_aa = Word([l_a, l_a])
        >>> w_ab = Word([l_a, l_b])
        >>> w_0 = Word([l_0])
        >>> w_1 = Word([l_1])        
        >>> ot.D = [w_lambda, w_a]
        >>> ot.S = [w_lambda, w_a]
        >>> ot.SA = [w_b, w_aa, w_ab]
        >>> ot.ot_content[w_lambda] = dict()
        >>> ot.ot_content[w_lambda][w_lambda] = w_0
        >>> ot.ot_content[w_lambda][w_a] = w_1
        >>> ot.ot_content[w_lambda][w_b] = w_1
        >>> ot.ot_content[w_lambda][w_aa] = w_0
        >>> ot.ot_content[w_lambda][w_ab] = w_1        
        >>> ot.ot_content[w_a] = dict()
        >>> ot.ot_content[w_a][w_lambda] = w_1
        >>> ot.ot_content[w_a][w_a] = w_0
        >>> ot.ot_content[w_a][w_b] = w_0
        >>> ot.ot_content[w_a][w_aa] = w_1
        >>> ot.ot_content[w_a][w_ab] = w_1
        >>> print ot
                               | [EmptyLetter] | [Letter(a)]
        ---------------------- | ------------- | -----------
        [EmptyLetter]          | [Letter(0)]   | [Letter(1)]
        [Letter(a)]            | [Letter(1)]   | [Letter(0)]
        ~~~                    | ~~~           | ~~~        
        [Letter(b)]            | [Letter(1)]   | [Letter(0)]
        [Letter(a), Letter(a)] | [Letter(0)]   | [Letter(1)]
        [Letter(a), Letter(b)] | [Letter(1)]   | [Letter(1)]
        ---------------------- | ------------- | -----------
        >>> ot.is_closed()
        False
        >>> ot.S.append(w_ab)
        >>> ot.SA.remove(w_ab)
        >>> w_aba = Word([l_a, l_b, l_a])
        >>> w_abb = Word([l_a, l_b, l_b])        
        >>> ot.SA.extend([w_aba, w_abb])
        >>> ot.ot_content[w_lambda][w_aba] = w_0
        >>> ot.ot_content[w_lambda][w_abb] = w_1
        >>> ot.ot_content[w_a][w_aba] = w_1
        >>> ot.ot_content[w_a][w_abb] = w_0
        >>> print ot
                                          | [EmptyLetter] | [Letter(a)]
        --------------------------------- | ------------- | -----------
        [EmptyLetter]                     | [Letter(0)]   | [Letter(1)]
        [Letter(a)]                       | [Letter(1)]   | [Letter(0)]
        [Letter(a), Letter(b)]            | [Letter(1)]   | [Letter(1)]
        ~~~                               | ~~~           | ~~~        
        [Letter(b)]                       | [Letter(1)]   | [Letter(0)]
        [Letter(a), Letter(a)]            | [Letter(0)]   | [Letter(1)]
        [Letter(a), Letter(b), Letter(a)] | [Letter(0)]   | [Letter(1)]
        [Letter(a), Letter(b), Letter(b)] | [Letter(1)]   | [Letter(0)]
        --------------------------------- | ------------- | -----------
        >>> ot.is_closed()
        True
        
        """
        self._logger.debug("Computes if the observation table is closed")

        for sa in self.SA:
            row_sa = self.__get_row(sa)
            found = False
            for s in self.S:
                if self.__get_row(s) == row_sa:
                    found = True
                    break
            if not found :
                return False
        return True

    def close_table(self):
        """This method closes the observation table.

        To close the observation table, it moves every row from SA to S that
        have no equivalent in S

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.FakeActiveKnowledgeBase import FakeActiveKnowledgeBase
        >>> from pylstar.Letter import Letter, EmptyLetter
        >>> from pylstar.Word import Word
        >>> from pylstar.automata.State import State
        >>> from pylstar.automata.Transition import Transition
        >>> from pylstar.automata.Automata import Automata
        >>> l_lambda = EmptyLetter()
        >>> l_a = Letter('a')
        >>> l_b = Letter('b')
        >>> l_1 = Letter(1)
        >>> l_2 = Letter(2)
        >>> l_3 = Letter(3)
        >>> s0 = State("S0")
        >>> s1 = State("S1")
        >>> t1 = Transition("T1", s0, l_a, l_1)
        >>> t2 = Transition("T2", s1, l_b, l_2)
        >>> t3 = Transition("T3", s1, l_a, l_1)
        >>> t4 = Transition("T4", s0, l_b, l_3)
        >>> s0.transitions = [t1, t2]
        >>> s1.transitions = [t3, t4]
        >>> automata = Automata(s0)
        >>> kbase = FakeActiveKnowledgeBase(automata)
        >>> ot = ObservationTable(input_letters = [l_a, l_b], knowledge_base = kbase)
        >>> ot.initialize()
        >>> print ot
                      | [Letter(a)] | [Letter(b)]
        ------------- | ----------- | -----------
        [EmptyLetter] | Letter(1)   | Letter(2)  
        ~~~           | ~~~         | ~~~        
        [Letter(a)]   | Letter(1)   | Letter(2)  
        [Letter(b)]   | Letter(1)   | Letter(3)  
        ------------- | ----------- | -----------
        >>> ot.is_closed()
        False
        >>> ot.close_table()
        >>> print ot
                               | [Letter(a)] | [Letter(b)]
        ---------------------- | ----------- | -----------
        [EmptyLetter]          | Letter(1)   | Letter(2)  
        [Letter(b)]            | Letter(1)   | Letter(3)  
        ~~~                    | ~~~         | ~~~        
        [Letter(a)]            | Letter(1)   | Letter(2)  
        [Letter(b), Letter(a)] | Letter(1)   | Letter(3)  
        [Letter(b), Letter(b)] | Letter(1)   | Letter(2)  
        ---------------------- | ----------- | -----------
        >>> ot.is_closed()
        True

        
        """

        for word_in_sa in self.SA:
            row_sa = self.__get_row(word_in_sa)
            found = False
            for word_in_s in self.S:
                row_s = self.__get_row(word_in_s)
                if row_s == row_sa:
                    found = True
                    break
            if not found:
                self._logger.debug("Row attached to SA '{}' ({}) could not be found in S".format(word_in_sa, row_sa))
                self.SA.remove(word_in_sa)
                self.__add_word_in_S(word_in_sa)
        
        self._logger.debug("Closing the observation table.")

    def __get_row(self, row_name):
        """This method returns the specified row

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable([], kbase)
        >>> ot.initialize()
        >>> w_a = Word([Letter('a')])
        >>> w_b = Word([Letter('b')])
        >>> w_c = Word([Letter('c')])
        >>> w_aa = Word([Letter('aa')])
        >>> w_ba = Word([Letter('ba')])
        >>> w_1 = Word([Letter('1')])
        >>> w_2 = Word([Letter('2')])
        >>> w_3 = Word([Letter('3')])                
        >>> ot.D.extend([w_a, w_b, w_c])
        >>> ot.S.extend([w_a, w_b])
        >>> ot.SA.extend([w_aa, w_ba])        
        >>> ot.ot_content[w_a] = dict()
        >>> ot.ot_content[w_a][w_a] = w_1
        >>> ot.ot_content[w_a][w_b] = w_1
        >>> ot.ot_content[w_a][w_aa] = w_3
        >>> ot.ot_content[w_a][w_ba] = w_3
        >>> ot.ot_content[w_b] = dict()
        >>> ot.ot_content[w_b][w_a] = w_2
        >>> ot.ot_content[w_b][w_b] = w_2
        >>> ot.ot_content[w_b][w_aa] = w_2
        >>> ot.ot_content[w_b][w_ba] = w_2
        >>> ot.ot_content[w_c] = dict()
        >>> ot.ot_content[w_c][w_a] = w_3
        >>> ot.ot_content[w_c][w_b] = w_3
        >>> ot.ot_content[w_c][w_aa] = w_1
        >>> ot.ot_content[w_c][w_ba] = w_1
        >>> print ', '.join([str(w) for w in ot._ObservationTable__get_row(w_a)])
        [Letter(1)], [Letter(2)], [Letter(3)]
        >>> print ', '.join([str(w) for w in ot._ObservationTable__get_row(w_b)])
        [Letter(1)], [Letter(2)], [Letter(3)]
        >>> print ', '.join([str(w) for w in ot._ObservationTable__get_row(w_aa)])
        [Letter(3)], [Letter(2)], [Letter(1)]
        >>> print ', '.join([str(w) for w in ot._ObservationTable__get_row(w_ba)])
        [Letter(3)], [Letter(2)], [Letter(1)]


"""
        
        if row_name is None:
            raise Exception("Row_name cannot be None")

        row = []

        for word_in_D in self.D:
            cel = self.ot_content[word_in_D]
            
            for r,v in cel.iteritems():
                if r == row_name:
                    row.append(v)
        return row
        
        

    def __add_word_in_D(self, word):
        """

        A 'None' word cannot be inserted in D

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> ot._ObservationTable__add_word_in_D(None)
        Traceback (most recent call last):
        ...
        Exception: Word cannot be None


        A word cannot be inserted twice in D

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> w = Word([Letter("a")])
        >>> ot._ObservationTable__add_word_in_D(w)
        >>> ot._ObservationTable__add_word_in_D(w)
        Traceback (most recent call last):
        ...
        Exception: Word '[Letter(a)]' is already registered in D

        

        """
        if word is None:
            raise Exception("Word cannot be None")

        if word in self.D:
            raise Exception("Word '{}' is already registered in D".format(word))

        if word in self.ot_content.keys():
            raise Exception("Word '{}' is already registered in the content of the observation table".format(word))

        self._logger.debug("Registering word '{}' in D".format(word))
        self.D.append(word)

        # computes the value of all existing S and SA for the newly inserted word
        cels = dict()

        for word_in_S_or_SA in self.S + self.SA:
            # formulates a new OutputQuery and executes it
            output_query = OutputQuery(word_in_S_or_SA + word)
            self.__execute_query(output_query)
            if not output_query.is_queried():
                raise Exception("Query '{}' could not be queried".format(output_query))
            cels[word_in_S_or_SA] = output_query.output_word.last_letter()

        self.ot_content[word] = cels        
            
        
    def __add_word_in_S(self, word):
        """Add the specified word in S. In details, it does the following:
        - add the specified word in the list of words in S
        - executes the output queries (word + word_in_D) and store the results in DxS
        - recomputes new SAs made with the specified word + word_in_D        


        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> ot.initialize()
        >>> w = Word([Letter("a")])
        >>> ot._ObservationTable__add_word_in_S(w)

        """

        if word is None:
            raise Exception("Word cannot be None")

        if word in self.S:
            raise Exception("Word '{}' is already registered in S".format(word))

        if word in self.SA:
            raise Exception("Word '{}' is already registered in SA".format(word))

        self._logger.debug("Registering word '{}' in S".format(word))

        self.S.append(word)

        for word_in_D in self.D:

            cel = self.ot_content[word_in_D]
            # if word in cel.keys():
            #     raise Exception("Word '{}' already exists in observation table with D='{}'".format(word, word_in_D))
            # formulates a new OutputQuery and execute it            
            output_query = OutputQuery(word + word_in_D)
            self._logger.debug("Execute query : {}".format(output_query))
            self.__execute_query(output_query)
            if not output_query.is_queried():
                raise Exception("Query '{}' could not be queried".format(output_query))

            cel[word] = output_query.output_word.last_letter()

        for input_letter in self.input_letters:
            if isinstance(word.letters[0], EmptyLetter):
                new_word = Word([input_letter])
            else:
                new_word = word + Word([input_letter])
            self._logger.debug("Adding word: {}".format(new_word))            
            if new_word not in self.S:
                self.__add_word_in_SA(new_word)

    def __add_word_in_SA(self, word):
        """Add the specified word in SA. In details, it does the following:


        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [], knowledge_base = kbase)
        >>> ot.initialize()
        >>> w = Word([Letter("a")])
        >>> ot._ObservationTable__add_word_in_SA(w)

        """

        if word is None:
            raise Exception("Word cannot be None")

        if word in self.SA:
            raise Exception("Word '{}' is already registered in SA".format(word))

        if word in self.S:
            raise Exception("Word '{}' is already registered in S".format(word))

        self._logger.debug("Registering word '{}' in SA".format(word))

        self.SA.append(word)

        for word_in_D in self.D:
            cel = self.ot_content[word_in_D]
            if word in cel.keys():
                raise Exception("Word '{}' already exists in observation table with D='{}'".format(word, word_in_D))
            # formulates a new OutputQuery and executes it
            output_query = OutputQuery(word + word_in_D)
            self._logger.debug("Execute query : {}".format(output_query))            
            self.__execute_query(output_query)
            if not output_query.is_queried():
                raise Exception("Query '{}' could not be queries".format(output_query))

            cel[word] = output_query.output_word.last_letter()
        
    def __execute_query(self, query):
        """This method triggers the execution of the specified query.
        
        An exception is raised if the query is None or if its execution failed

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> kbase = KnowledgeBase()
        >>> oTable = ObservationTable([], knowledge_base = kbase)
        >>> oTable._ObservationTable__execute_query(None)
        Traceback (most recent call last):
        ...
        Exception: Query cannot be None
        
        """
        if query is None:
            raise Exception("Query cannot be None")

        try:
            self.knowledge_base.resolve_query(query)
        except Exception, e:
            self._logger.error(e)

    def build_hypothesis(self):
        """This method returns and Automata that follows the observation table.

        If the observation table is closed and consistent, it is possible to construct
        an hypothesis automata. Each state of the automata maps to a row of S in the observation table.        

        >>> from pylstar.ObservationTable import ObservationTable
        >>> from pylstar.KnowledgeBase import KnowledgeBase
        >>> from pylstar.Letter import Letter, EmptyLetter
        >>> from pylstar.Word import Word
        >>> l_lambda = EmptyLetter()
        >>> l_a = Letter('a')
        >>> l_b = Letter('b')
        >>> l_y = Letter('y')
        >>> l_z = Letter('z')
        >>> w_lambda = Word([l_lambda])
        >>> w_a = Word([l_a])
        >>> w_b = Word([l_b])
        >>> w_aa = Word([l_a, l_a])
        >>> w_ab = Word([l_a, l_b])
        >>> w_aaa = Word([l_a, l_a, l_a])
        >>> w_aab = Word([l_a, l_a, l_b])
        >>> kbase = KnowledgeBase()
        >>> ot = ObservationTable(input_letters = [l_a, l_b], knowledge_base = kbase)
        >>> ot.D.extend([w_a, w_b, w_aa])
        >>> ot.S.extend([w_lambda, w_a, w_aa])
        >>> ot.SA.extend([w_b, w_ab, w_aaa, w_aab])
        >>> ot.ot_content[w_a] = dict()
        >>> ot.ot_content[w_a][w_lambda] = l_z
        >>> ot.ot_content[w_a][w_a] = l_y
        >>> ot.ot_content[w_a][w_aa] = l_z
        >>> ot.ot_content[w_a][w_b] = l_y
        >>> ot.ot_content[w_a][w_ab] = l_z
        >>> ot.ot_content[w_a][w_aaa] = l_z
        >>> ot.ot_content[w_a][w_aab] = l_y
        >>> ot.ot_content[w_b] = dict()
        >>> ot.ot_content[w_b][w_lambda] = l_z
        >>> ot.ot_content[w_b][w_a] = l_y
        >>> ot.ot_content[w_b][w_aa] = l_z
        >>> ot.ot_content[w_b][w_b] = l_y
        >>> ot.ot_content[w_b][w_ab] = l_z
        >>> ot.ot_content[w_b][w_aaa] = l_z
        >>> ot.ot_content[w_b][w_aab] = l_y
        >>> ot.ot_content[w_aa] = dict()
        >>> ot.ot_content[w_aa][w_lambda] = l_y
        >>> ot.ot_content[w_aa][w_a] = l_z
        >>> ot.ot_content[w_aa][w_aa] = l_z
        >>> ot.ot_content[w_aa][w_b] = l_z
        >>> ot.ot_content[w_aa][w_ab] = l_y
        >>> ot.ot_content[w_aa][w_aaa] = l_y
        >>> ot.ot_content[w_aa][w_aab] = l_z        
        >>> print ot
                                          | [Letter(a)] | [Letter(b)] | [Letter(a), Letter(a)]
        --------------------------------- | ----------- | ----------- | ----------------------
        [EmptyLetter]                     | Letter(z)   | Letter(z)   | Letter(y)             
        [Letter(a)]                       | Letter(y)   | Letter(y)   | Letter(z)             
        [Letter(a), Letter(a)]            | Letter(z)   | Letter(z)   | Letter(z)             
        ~~~                               | ~~~         | ~~~         | ~~~                   
        [Letter(b)]                       | Letter(y)   | Letter(y)   | Letter(z)             
        [Letter(a), Letter(b)]            | Letter(z)   | Letter(z)   | Letter(y)             
        [Letter(a), Letter(a), Letter(a)] | Letter(z)   | Letter(z)   | Letter(y)             
        [Letter(a), Letter(a), Letter(b)] | Letter(y)   | Letter(y)   | Letter(z)             
        --------------------------------- | ----------- | ----------- | ----------------------
        >>> print ot.is_closed()
        True
        >>> print ot.find_inconsistency()
        None
        >>> automata = ot.build_hypothesis()
        >>> print automata.build_dot_code()
        digraph G {
        "z,z,y" [shape=doubleoctagon, style=filled, fillcolor=white, URL="z,z,y"];
        "y,y,z" [shape=ellipse, style=filled, fillcolor=white, URL="y,y,z"];
        "z,z,z" [shape=ellipse, style=filled, fillcolor=white, URL="z,z,z"];
        "z,z,y" -> "y,y,z" [fontsize=5, label="I='Letter(a)' / O='Letter(z)'", URL="t4"];
        "z,z,y" -> "y,y,z" [fontsize=5, label="I='Letter(b)' / O='Letter(z)'", URL="t5"];
        "y,y,z" -> "z,z,z" [fontsize=5, label="I='Letter(a)' / O='Letter(y)'", URL="t0"];
        "y,y,z" -> "z,z,y" [fontsize=5, label="I='Letter(b)' / O='Letter(y)'", URL="t1"];
        "z,z,z" -> "z,z,y" [fontsize=5, label="I='Letter(a)' / O='Letter(z)'", URL="t2"];
        "z,z,z" -> "y,y,z" [fontsize=5, label="I='Letter(b)' / O='Letter(z)'", URL="t3"];
        }

        """

        states = []
        transitions = []
        initial_state = None
        words_and_states = []
        long_state_name_to_states = dict()        
        
        # find all rows in S
        rows_in_S = {s: self.__get_row(s) for s in self.S}

        # get all unique rows
        S_with_same_rows = collections.defaultdict(list)
        for word_in_s, row_s in rows_in_S.iteritems():
            S_with_same_rows[','.join([str(w) for w in row_s])].append(word_in_s)        

        # build the list of states of the hypothesis (and identify the initial state)
        for long_state_name, words_in_S in S_with_same_rows.iteritems():
            state_name = ''.join(long_state_name.replace("Letter(", "").replace(')', ''))
            state = State(name = state_name)
            states.append(state)

            words_and_states.append((words_in_S[0], state))
            long_state_name_to_states[long_state_name] = state
            
            # check if its the initial state
            epsilon_word_found = Word([EmptyLetter()]) in words_in_S
            self._logger.debug("state  :{} , {} / {}".format(long_state_name, words_in_S, epsilon_word_found))
            
            if initial_state is None and epsilon_word_found:
                initial_state = state
            elif epsilon_word_found and initial_state is not None:
                raise Exception("Multiple initial state found.")

        if initial_state is None:
            raise Exception("Can't find any initial state")

        # computes the transitions for each state of the automata
        for word, state in words_and_states:

            for input_letter in self.input_letters:

                # computes the output state
                new_word = word + Word([input_letter])
                row_new_word = self.__get_row(new_word)

                output_state_name = ','.join([str(w) for w in row_new_word])
                if output_state_name not in long_state_name_to_states.keys():
                    raise Exception("Cannot find a state with following name : '{}'".format(output_state_name))

                output_state = long_state_name_to_states[output_state_name]
                output_letter = self.ot_content[Word([input_letter])][word]

                transition_name = "t{}".format(len(transitions))
                transition = Transition(name = transition_name,
                                        output_state = output_state,
                                        input_letter = input_letter,
                                        output_letter = output_letter)
                state.transitions.append(transition)
                transitions.append(transition)
                
                                                    
        return Automata(initial_state = initial_state)

    def __str__(self):
        result = []

        # lets build a matrix out of the observation table
        # a matrix : a list of list a.k.a a list of rows
        matrix = []

        # adding header
        header_row = [''] + [str(d) for d in self.D]
        matrix.append(header_row)
        
        for row_name in self.S:
            row_result = [str(row_name)] + [str(w) for w in self.__get_row(row_name)]
            matrix.append(row_result)

        matrix.append(['~~~']*len(header_row))

        for row_name in self.SA:
            row_result = [str(row_name)] + [str(w) for w in self.__get_row(row_name)]
            matrix.append(row_result)

        self._logger.debug(matrix)

        cs = zip(*matrix)
        c_ws = [max(len(value) for value in c) for c in cs]
        line = ["-"*w for w in c_ws]
        matrix.insert(1, line)
        matrix.append(line)
        format = ' | '.join(['%%-%ds' % w for w in c_ws])
        # Format data
        result = [(format % tuple(r)) for r in matrix]
        return '\n'.join(result)        

    @property
    def knowledge_base(self):
        """The knowledge base plays the role of a proxy between the algorithm and the System Under Learning.
        """
        return self.__knowledge_base
    
    @knowledge_base.setter
    def knowledge_base(self, knowledge_base):
        if knowledge_base is None:
            raise Exception("Knowledge base cannot be None")
        
        self.__knowledge_base = knowledge_base

        
        
        
            

        

        
