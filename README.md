# pylstar : An implementation of the LSTAR Grammatical Inference Algorithm

[![Build Status](https://travis-ci.org/gbossert/pylstar.svg?branch=master)](https://travis-ci.org/gbossert/pylstar)
[![Coverage Status](https://coveralls.io/repos/gbossert/pylstar/badge.svg?branch=master&service=github)](https://coveralls.io/github/gbossert/pylstar?branch=master)

## About pylstar
pylstar is a free and open source Python implementation of the *LSTAR* Grammatical inference algorithm. It can be use to automaticaly infer the state machine that best describe the internal of a deterministic black box. To achieve this, pylstar observes the behavior of the target when stimulated with sequence of messages.

It has succesfully been used to infer various protocols such as Botnet protocols, Smart Cards protocols, Cryptographic protocols and Web Servers.

## Sample usage
One that wants to use *pylstar* must write a class that communicates with the targeted black box (*i.e.* it exposes the Minimaly Adequate Teacher of the targeted reactive System). This can be done by subclassing `pylstar.ActiveKnowledgeBase.ActiveKnowledgeBase`. If the targeted process is a network server, one can solely subclass `pylstar.NetworkActiveKnowledgeBase`.

For example, the following class can be use to start and stop a fake coffee machine (`coffeemachine.py`) through it API (`localhost:3000`). This class inherits from `pylstar.NetworkActiveKnowledgeBase` which exposes methods that can send (and read) network messages to (and by) the coffee machine API.

```python
import time
import subprocess

from pylstar.NetworkActiveKnowledgeBase import NetworkActiveKnowledgeBase

class CoffeeMachineKnowledgeBase(NetworkActiveKnowledgeBase):

    def __init__(self):
        super(CoffeeMachineKnowledgeBase, self).__init__("localhost", 3000)
        self.__sp = None

    def start(self):
    """This methods starts the coffee machine (to be triggered before the learning process)."""
        self.__sp = subprocess.Popen("/usr/bin/python coffeemachine.py", shell=True)
        # lets wait 5 seconds for the coffee machine to start
        time.sleep(5)
        
    def stop(self):
    """This method stops the coffee machine (to be triggered after the learning process)."""
        if self.__sp is not None:
            self.__sp.kill()
```

Given this wrapper, the following snippet can be used to trigger the automatic inference of the coffee machine. This code declares the messages accepted by the API, an instance of our wrapper and returns a `pylstar.automata.Automata.Automata` (and prints its DOT code) that best describes the behavior of the coffee machine.

```python
from pylstar.LSTAR import LSTAR
from CoffeeMachineKnowledgeBase import CoffeeMachineKnowledgeBase

# list of messages accepted by the coffee machine
input_vocabulary = [
    "REFILL_WATER",
    "REFILL_COFFEE",
    "PRESS_BUTTON_A",
    "PRESS_BUTTON_B",
    "PRESS_BUTTON_C"    
]
# instanciates our CoffeeMachine MAT
coffeeBase = CoffeeMachineKnowledgeBase()
try:
    # starts the coffee machine
    coffeeBase.start()
    # learns its grammar
    lstar = LSTAR(input_vocabulary, coffeeBase, max_states = 10)
    # stores the coffee machine state machine
    coffee_state_machine = lstar.learn()

    # displays the DOT code of the state machine
    print(coffee_state_machine.build_dot_code())
finally:
   coffeeBase.stop()
```
The execution of this sample returns the state machine illustrated below:

![State Machine of the CoffeeMachine Implementation](https://rawgithub.com/gbossert/pylstar/next/resources/docs/coffee_machine.svg)

A runnable example of the coffee machine inference is available in `test/src/test_pylstar/coffee_machine_example`.

## Installation

Pylstar is a typical python library. It relies on a `setup.py` file to describe its installation process.The following command can be use to install pylstar on your system:
```bash
# python setup.py install 
```

## Main Features

### Playing with Automata

The implementation of automata in pylstar follows the definition of [Mealy Machines](https://en.wikipedia.org/wiki/Mealy_machine). An automaton is made of a unique initial state, states and transitions.

#### States

A state (`pylstar.automata.state.State`) is defined by its name (`str`) and some transitions (`list<pylstar.automata.transition.Transition>`). Per default, a state has no transition.
```python
from pylstar.automata.State import State

q0 = State(name="Example state")
q1 = State("Another state")
```

N.B: Two states are said equivalent if their name equals.

#### Transitions

A transition (`pylstar.automata.transition.Transition`) denotes a directed edge between two states. An edge is attached to a source state and is defined by a triplet:
* a name (`str`),
* an input letter (`pylstar.Letter.Letter`),
* an output letter (`pylstar.Letter.Letter`),
* a destination state (`pylstar.automata.State.State`).
 
The following snippet defines a transition (`t0`) that can be use to reach "destination state" (`q1`) from "origin state" (`q0`) if input letter "a" (`la`) is received. Executing this transition triggers the emission of letter "0" (`l0`).

```python
from pylstar.letter import Letter
from pylstar.automata.State import State
from pylstar.automata.Transition import Transition

la = Letter("a")
l0 = Letter("0")
q0 = State("origin state")
q1 = State("destination state")
t0 = Transition("Example Transition", q1, la, l0) 
q0.transitions.append(t0)
```

#### Automaton

An automaton (`pylstar.automata.Automata.Automata`) is defined by its initial state (`pylstar.automata.State.State`) and an optional name (`str`). For example, the following snippet illustrates the creation of an automaton:

```python
from pylstar.automata.Automata import Automata
from pylstar.automata.State import State

q0 = State(name="Initial State")
simple_automata = Automata(initial_state = q0, name = "Simple Automata")
```

An automaton exposes the following methods:
- *build_dot_code()* - Returns the DOT code (`str`) that represents the automaton.
- *get_states()* - Returns all the states (`list<pylstar.automata.State.State>`) that can be reached from the initial state of the automaton.
- *play_word(`pylstar.Word.Word` w, `pylstar.automata.State.State` s = None)* - Visits the automaton according to the specified sequence of input messages `w` starting from state `s` (if None, it starts from the initial state). It returns a tupple made of the produced messages and the states reached while visiting the automaton ( `(pylstar.Word.Word, list<pylstar.automata.State.State>)`).

## Tests

This project uses DocTests for testing and documentation purposes.
To trigger the tests, please use the following command:

```bash
$ python setup.py test
```


## References

The LSTAR algorithm was introduced by Dana Angluin in the article
```bibtex
@article{Angluin:1987,
 author = {Angluin, Dana},
 title = {Learning Regular Sets from Queries and Counterexamples},
 journal = {Inf. Comput.},
 issue_date = {November 1, 1987},
 publisher = {Academic Press, Inc.},
} 
```

This implementation also relies on the description of LSTAR provided by Colin de la Higuera in the book
```bibtex
@book{ColindelaHiguera,
  author = {de la Higuera, Colin},
  title = {Grammatical Inference: Learning Automata and Grammars},
  year = {2010},
  isbn = {0521763169, 9780521763165},
  publisher = {Cambridge University Press},
  address = {New York, NY, USA},
}
```

## Bugs and enhancements

I'm almost certain this code contains bugs. Please, report any bug found by opening a ticket and/or by submiting a pull requests.Obvisouly, the projet is opened to any minor and major enhancements.

## Author

* Georges Bossert <gbossert@miskin.fr>

## License

This software is licensed under the GPLv3 License. See the ``COPYING.txt`` file
in the top distribution directory for the full license text.
