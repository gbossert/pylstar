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
import os
import json

# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger
from pylstar.Word import Word
from pylstar.Letter import Letter


@PylstarLogger
class KnowledgeNode(object):

    def __init__(self, input_letter, output_letter):
        self.input_letter = input_letter
        self.output_letter = output_letter
        self.children = []

    def __str__(self, level=0):
        return json.dumps(self.serialize(), sort_keys=True, indent=4, separators=(',', ': '))

    def serialize(self):
        """This method return a serialized representation of the node"""
        node = {
            "input_letter" : self.input_letter.serialize(),
            "output_letter": self.output_letter.serialize(),
            "children" : [c.serialize() for c in self.children]
        }
        return node
    
    @staticmethod
    def deserialize(dict_data, possible_letters):
        if dict_data is None:
            raise Exception("dict_data cannot be None")
        input_letter = Letter.deserialize(dict_data['input_letter'], possible_letters)
        output_letter = Letter.deserialize(dict_data['output_letter'], possible_letters)

        node = KnowledgeNode(input_letter, output_letter)
        for child in dict_data["children"]:
            node.children.append(KnowledgeNode.deserialize(child, possible_letters))

        return node

    def traverse(self, input_letters, output_letters = None):
        self._logger.debug("Traversing children of '{}' with '{}'".format(self, ', '.join([str(l) for l in input_letters])))

        if input_letters[0] != self.input_letter:
            raise Exception("Node cannot be traversed with input letter '{}'".format(input_letters[0]))
        if output_letters is not None and output_letters[0] != self.output_letter:
            raise Exception("Node '{}' cannot be traversed with output letter '{}'".format(self, output_letters[0]))
        if output_letters is not None and len(input_letters) != len(output_letters):
            raise Exception("Specified input and output letters do not have the same length")


        if len(input_letters) < 2:
            return [self.output_letter]

        current_input_letter = input_letters[1]
        current_output_letter = None
        if output_letters is not None:
            current_output_letter = output_letters[1]

        for children in self.children:
            if children.input_letter == current_input_letter:
                new_output_letters = None
                if current_output_letter is not None:
                    if children.output_letter != current_output_letter:
                        raise Exception("Incompatible path found, expected '{}' found '{}".format(children.output_letter.symbols, current_output_letter.symbols))
                    new_output_letters = output_letters[1:]

                new_input_letters = input_letters[1:]

                return [self.output_letter] + children.traverse(new_input_letters, output_letters = new_output_letters)

        if output_letters is not None:
            new_children = KnowledgeNode(input_letter = input_letters[1], output_letter = output_letters[1])
            self._logger.debug("Creating a '{}' as a child of '{}'".format(new_children, self))
            self.children.append(new_children)
            new_input_letters = input_letters[1:]
            new_output_letters = output_letters[1:]
            return [self.output_letter] + new_children.traverse(new_input_letters, output_letters = new_output_letters)

        raise Exception("Cannot traverse node '{}' with subsequences '{}'".format(self, ', '.join([str(l) for l in input_letters])))

    @property
    def input_letter(self):
        """Input letter"""
        return self.__input_letter

    @input_letter.setter
    def input_letter(self, input_letter):
        if input_letter is None:
            raise Exception("Input letter cannot be None")
        self.__input_letter = input_letter

    @property
    def output_letter(self):
        """Output letter"""
        return self.__output_letter

    @output_letter.setter
    def output_letter(self, output_letter):
        if output_letter is None:
            raise Exception("Output letter cannot be None")
        self.__output_letter = output_letter


@PylstarLogger
class KnowledgeTree(object):
    """A pythonic implementation of a tree that hosts query results.

    >>> from pylstar.KnowledgeTree import KnowledgeTree
    >>> from pylstar.Word import Word
    >>> from pylstar.Letter import Letter
    >>> tree = KnowledgeTree()
    >>> input_word = Word([Letter("a"), Letter("b")])
    >>> output_word = Word([Letter(1), Letter(2)])
    >>> tree.get_output_word(input_word)
    Traceback (most recent call last):
    ...
    Exception: No path found
    >>> tree.add_word(input_word, output_word)
    >>> print tree.get_output_word(input_word)
    [Letter(1), Letter(2)]


    """

    def __init__(self, cache_file_path = None):
        self.__cache_file_path = cache_file_path
        self.__nb_added_word = 0
        self.roots = []

    def __str__(self):
        result = '\n'.join([root.__str__(level=1).rstrip() for root in self.roots])
        return 'Tree (\n{}\n)'.format(result)


    def get_output_word(self, input_word):
        if input_word is None:
            raise Exception("Input word cannot be None")

        for root in self.roots:
            try:
                return Word(root.traverse(input_word.letters))
            except Exception, e:
                self._logger.debug(e)

        raise Exception("No path found")

    def add_word(self, input_word, output_word):
        """This method can be use to associate an input word to an output word

        >>> from pylstar.KnowledgeTree import KnowledgeTree
        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> tree = KnowledgeTree()
        >>> input_word = Word([Letter("a"), Letter("b")])
        >>> output_word = Word([Letter(1), Letter(2)])
        >>> tree.add_word(input_word, output_word)

        The same association can be inserted twice iif both input and output are equivalent
        to the previously inserted association

        >>> from pylstar.KnowledgeTree import KnowledgeTree
        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> tree = KnowledgeTree()
        >>> input_word = Word([Letter("a"), Letter("b")])
        >>> output_word = Word([Letter(1), Letter(2)])
        >>> tree.add_word(input_word, output_word)
        >>> input_word2 = Word([Letter("a"), Letter("b")])
        >>> output_word2 = Word([Letter(1), Letter(2)])
        >>> tree.add_word(input_word2, output_word2)
        >>> output_word3 = Word([Letter(1), Letter(1)])
        >>> tree.add_word(input_word2, output_word3)
        Traceback (most recent call last):
        ...
        Exception: Incompatible path found, expected 'set([2])' found 'set([1])




        """

        if input_word is None:
            raise Exception("Input word cannot be None")
        if output_word is None:
            raise Exception("Output word cannot be None")
        if len(input_word) != len(output_word):
            raise Exception("Input and output words do not have the same size")

        self.__add_letters(input_word.letters, output_word.letters)

        self.__nb_added_word += 1
        if self.__cache_file_path is not None and self.__nb_added_word % 100 == 0:
            self.write_cache()

    def write_cache(self):
        """This method writes the content of the knowledge tree to the self.cache_file_path.

        >>> cache_file = "/tmp/test_ktree_cache.dump"
        >>> from pylstar.KnowledgeTree import KnowledgeTree
        >>> from pylstar.Word import Word
        >>> from pylstar.Letter import Letter
        >>> l_a = Letter("a")
        >>> l_b = Letter("b")
        >>> l_c = Letter("c")
        >>> l_1 = Letter(1)
        >>> l_2 = Letter(2)
        >>> l_3 = Letter(3)
        >>> tree = KnowledgeTree(cache_file_path = cache_file)
        >>> input_word = Word([l_a, l_b])
        >>> output_word = Word([l_1, l_2])
        >>> tree.add_word(input_word, output_word)
        >>> tree.write_cache()        
        >>> input_word = Word([l_a, l_c])
        >>> output_word = Word([l_1, l_3])
        >>> tree.add_word(input_word, output_word)
        >>> tree.write_cache()
        >>> tree2 = KnowledgeTree(cache_file_path = cache_file)
        >>> tree2.load_cache(possible_letters = [l_a, l_b, l_c, l_1, l_2, l_3])
        >>> print tree2.get_output_word(input_word)
        [Letter(1), Letter(3)]
        
        """

        if self.__cache_file_path is None:
            raise Exception("Cache file path cannot be None")

        self._logger.info("Writing the knowledge tree in cache '{}'".format(self.__cache_file_path))

        if os.path.exists(self.__cache_file_path):
            self._logger.info("Removing previous cache file '{}'".format(self.__cache_file_path))
            os.remove(self.__cache_file_path)

        nodes = [ root.serialize() for root in self.roots ]
        with open(self.__cache_file_path, "w") as fd:
            str_content = json.dumps(nodes, sort_keys=True, indent=4, separators=(',', ': '))
            fd.write(str_content)

    def load_cache(self, possible_letters):
        """This method loads the content of the cache in the knowledge tree

        See doctest declared in method "write_cache"
    
        """
        if self.__cache_file_path is None:
            raise Exception("Cache file path cannot be None")
        self._logger.info("Loading cache from '{}'".format(self.__cache_file_path))

        json_content = None
        
        with open(self.__cache_file_path, "r") as fd:
            json_content = json.loads(fd.read())

        for content in json_content:
            self.roots.append(KnowledgeNode.deserialize(content, possible_letters))
        
    def __add_letters(self, input_letters, output_letters):
        self._logger.debug("Adding letters '{}' / '{}'".format(', '.join([str(l) for l in input_letters]), ', '.join([str(l) for l in output_letters])))

        retained_root = None

        for root in self.roots:
            if root.input_letter == input_letters[0]:
                if root.output_letter != output_letters[0]:
                    raise Exception("Incompatible path found, expected '{}' found '{}".format(root.output_letter, output_letters[0]))
                retained_root = root
                break

        if retained_root is None:
            retained_root = KnowledgeNode(input_letters[0], output_letters[0])
            self._logger.debug("Creating '{}' as a new root".format(retained_root))
            self.roots.append(retained_root)

        return retained_root.traverse(input_letters, output_letters)
