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
import uuid

# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.automata.Automata import Automata
from pylstar.automata.State import State
from pylstar.automata.Transition import Transition
from pylstar.Letter import Letter
from pylstar.tools.Decorators import PylstarLogger


@PylstarLogger
class DOTParser(object):
    """A parser for DOT files
    """

    @staticmethod
    def parse(dot_content, vocabulary = None):
        """This method returns the Automata that is represented by the specified DOT.
        
        :param dot_content: the DOT definition of the automata to build
        :type dot_content: str
        :rtype: pylstar.automata.Automata.Automata
        
        >>> from pylstar.automata.State import State
        >>> from pylstar.Letter import Letter
        >>> from pylstar.automata.Transition import Transition
        >>> from pylstar.automata.Automata import Automata
        >>> la = Letter('A')
        >>> lb = Letter('B')
        >>> l0 = Letter(0)
        >>> l1 = Letter(1)
        >>> q0 = State("Q0")
        >>> q1 = State("Q1")
        >>> q2 = State("Q2")
        >>> t0 = Transition("t0", q0, la, l0)
        >>> q0.transitions.append(t0)
        >>> t1 = Transition("t1", q1, lb, l1)
        >>> q0.transitions.append(t1)
        >>> t2 = Transition("t2", q0, la, l0)
        >>> q1.transitions.append(t2)
        >>> t3 = Transition("t3", q2, lb, l1)
        >>> q1.transitions.append(t3)
        >>> t4 = Transition("t4", q0, la, l1)
        >>> q2.transitions.append(t4)
        >>> automata = Automata(initial_state = q0, name = "Example")
        >>> dot_automata = DOTParser.build_dot_code(automata)
        >>> parsed_automata = DOTParser.parse(dot_automata)
        >>> print(parsed_automata.name)
        Example
        >>> print(DOTParser.build_dot_code(parsed_automata))
        digraph "Example" {
        "Q0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="Q0"];
        "Q1" [shape=ellipse, style=filled, fillcolor=white, URL="Q1"];
        "Q2" [shape=ellipse, style=filled, fillcolor=white, URL="Q2"];
        "Q0" -> "Q0" [fontsize=5, label="A / 0", URL="t0"];
        "Q0" -> "Q1" [fontsize=5, label="B / 1", URL="t1"];
        "Q1" -> "Q0" [fontsize=5, label="A / 0", URL="t2"];
        "Q1" -> "Q2" [fontsize=5, label="B / 1", URL="t3"];
        "Q2" -> "Q0" [fontsize=5, label="A / 1", URL="t4"];
        }

        """

        
        if dot_content is None:
            raise Exception("dot_content cannot be None")
        dot_content = str(dot_content).strip()
        if len(dot_content) == 0:
            raise Exception("dot_content cannot be Empty")

        automata = None

        if not dot_content.startswith("digraph "):
            raise Exception("Dot_content must starts with digraph")

        i_start_graph_def = dot_content.find('{')
        if i_start_graph_def == -1:
            raise Exception("Cannot find '{' that indicates beginning of the graph definition")

        # extracts the automata name
        automata_name = dot_content[len("digraph "):i_start_graph_def].strip()
        if len(automata_name) == 0:
            raise Exception("Name of the automata cannot be None")

        automata_name = automata_name.replace('"', '')
        
        graph_def = dot_content[i_start_graph_def+1:].strip()
        graph_entries = graph_def.split(";")

        states = []
        # parses all the state definitions and their transitions
        for graph_entry in graph_entries:
            try:
                DOTParser.__parse_graph_entry(graph_entry, states)                    
            except Exception:
                pass

        automata = Automata(states[0], name=automata_name)

        return automata
    
    @staticmethod
    def __parse_graph_entry(graph_entry, states):
        if graph_entry is None:
            raise Exception("Graph entry cannot be None")
        graph_entry = str(graph_entry).strip()
        if len(graph_entry) == 0:
            raise Exception("Graph entry cannot be None")

        # parse first object
        i_start_first_obj = graph_entry.find('"')
        if i_start_first_obj == -1:
            raise Exception("Cannot find first object definition")

        i_end_first_obj = graph_entry.find('"', i_start_first_obj+1)
        if i_end_first_obj == -1:
            raise Exception("Cannot find first object definition")

        first_obj_name = graph_entry[i_start_first_obj+1:i_end_first_obj].strip()
        if len(first_obj_name) == 0:
            raise Exception("Cannot parse the name of the first object")

        first_state = None
        for state in states:
            if state.name == first_obj_name:
                first_state = state                

        if first_state is None:
            first_state = State(name=first_obj_name)
            states.append(first_state)

        remainder = graph_entry[i_end_first_obj+1:].strip()

        if remainder.startswith("->"):

            remainder = remainder[2:].strip()

            # parses the second state of the transition
            i_start_second_obj = remainder.find('"')
            if i_start_second_obj == -1:
                raise Exception("Cannot find second object definition")

            i_end_second_obj = remainder.find('"', i_start_second_obj+1)
            if i_end_second_obj == -1:
                raise Exception("Cannot find second object definition")

            second_obj_name = remainder[i_start_second_obj+1:i_end_second_obj].strip()
            if len(second_obj_name) == 0:
                raise Exception("Cannot find the name of the destination state")

            second_state = None
            for state in states:
                if state.name == second_obj_name:
                    second_state = state
                    
            if second_state is None:
                second_state = State(name=second_obj_name)
                states.append(second_state)

            # parses the transition input and output letters
            remainder = remainder[i_end_second_obj+2:]
            i_start_transition_details = remainder.find('[')
            if i_start_transition_details == -1:
                raise Exception("Cannot find transition details")
            
            transition_details = remainder[i_start_transition_details:]

            # parses the transition label
            i_start_label = transition_details.find('label=')
            if i_start_label == -1:
                raise Exception("Cannot find label of the transition")
            i_end_label = transition_details[i_start_label + len('label="'):].find('"')
            label = transition_details[i_start_label + len('label="'): i_start_label + len('label="')+i_end_label].strip()

            if len(label) == 0:
                raise Exception("Cannot find label")

            # parses input and output letters out of the label
            (input, output) = label.split('/')

            input_letter = Letter(input.strip())
            output_letter = Letter(output.strip())            

            # parses the transition name (url)
            i_start_url = transition_details.find('URL=')
            if i_start_url != -1:
                i_end_url = transition_details[i_start_url + len('URL="'):].find('"')
                url = transition_details[i_start_url + len('url="'): i_start_url + len('url="')+i_end_url].strip()
                t_name = url
            else:
                t_name = str(uuid.uuid4())

            transition = Transition(t_name, second_state, input_letter, output_letter)
            first_state.transitions.append(transition)    

    @staticmethod
    def build_dot_code(automata):
        """This method returns the DOT code that represents the provided Automata.

        :param automata: The automata the returned DOT code will represent
        :type automata: pylstar.automata.Automata
        :rtype: str        

        >>> from pylstar.automata.State import State
        >>> from pylstar.Letter import Letter
        >>> from pylstar.automata.Transition import Transition
        >>> from pylstar.automata.Automata import Automata
        >>> la = Letter('A')
        >>> lb = Letter('B')
        >>> l0 = Letter(0)
        >>> l1 = Letter(1)
        >>> q0 = State("Q0")
        >>> q1 = State("Q1")
        >>> q2 = State("Q2")
        >>> t0 = Transition("t0", q0, la, l0)
        >>> q0.transitions.append(t0)
        >>> t1 = Transition("t1", q1, lb, l1)
        >>> q0.transitions.append(t1)
        >>> t2 = Transition("t2", q1, la, l0)
        >>> q1.transitions.append(t2)
        >>> t3 = Transition("t3", q2, lb, l1)
        >>> q1.transitions.append(t3)
        >>> t4 = Transition("t4", q0, la, l1)
        >>> q2.transitions.append(t4)
        >>> automata = Automata(initial_state = q0, name = "Example")
        >>> print(DOTParser.build_dot_code(automata))
        digraph "Example" {
        "Q0" [shape=doubleoctagon, style=filled, fillcolor=white, URL="Q0"];
        "Q1" [shape=ellipse, style=filled, fillcolor=white, URL="Q1"];
        "Q2" [shape=ellipse, style=filled, fillcolor=white, URL="Q2"];
        "Q0" -> "Q0" [fontsize=5, label="A / 0", URL="t0"];
        "Q0" -> "Q1" [fontsize=5, label="B / 1", URL="t1"];
        "Q1" -> "Q1" [fontsize=5, label="A / 0", URL="t2"];
        "Q1" -> "Q2" [fontsize=5, label="B / 1", URL="t3"];
        "Q2" -> "Q0" [fontsize=5, label="A / 1", URL="t4"];
        }


        """

        if automata is None:
            raise Exception("Automata cannot be None")
        if not isinstance(automata, Automata):
            raise Exception("Must be an Automata")
        
        dot_code = []
        dot_code.append("digraph \"{}\" {{".format(automata.name))

        # Includes all the states declared in the automata
        states = automata.get_states()
        for state in states:
            color = "white"

            if state == automata.initial_state:
                shape = "doubleoctagon"
            else:
                shape = "ellipse"

            dot_code.append('"{0}" [shape={1}, style=filled, fillcolor={2}, URL="{3}"];'.format(state.name, shape, color, state.name))

        # Adds all the transitions
        for inputState in states:
            for transition in inputState.transitions:
                outputState = transition.output_state
                dot_code.append('"{0}" -> "{1}" [fontsize=5, label="{2}", URL="{3}"];'.format(inputState.name, outputState.name, transition.label, transition.name))

        dot_code.append("}")

        return '\n'.join(dot_code)

