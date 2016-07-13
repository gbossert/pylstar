# pylstar : An implementation of the LSTAR Grammatical Inference Algorithm

[![Build Status](https://travis-ci.org/gbossert/pylstar.svg?branch=master)](https://travis-ci.org/gbossert/pylstar)
[![Coverage Status](https://coveralls.io/repos/gbossert/pylstar/badge.svg?branch=master&service=github)](https://coveralls.io/github/gbossert/pylstar?branch=master)


**Warning : This implementation is only intented for testing purposes : Work in Progress.**

## About  LSTAR
The LSTAR Grammatical inference algorithm can be use to infer the automata that best describes a targeted determinist reactive systems if a Minimally Adequate Teacher (MAT) exists for it. As stated by G. Holzman in its reference book, a MAT is "an Oracle that give answers to membership queries and strong equivalence queries".

**The general idea of the algorithm** :

1. create an observation table with the list of input messages accepted by the target.
2. while the observation table is not closed and complete do :
  1. stimulate the target with crafted input requests.
  2. store request outputs in the observation table.  
3. build an hypothesis automata out of the observation table.
4. search for a counter-example by comparing the behavior of the hypothesis against the target.
5. if a counter-example is found.
  1. update the observation table according to the counter-example.
  2. returns to step 2.
6. if no counter-example was found, the hypothesis is said valid (up to specific probability).

## About pylstar
pylstar is a free and open source Python implementation of the LSTAR Grammatical inference algorithm.
It should be noted that per default this implementation follows the original description of the Angluin's algorithm and relies on *WMethod* to produce the required equivalence queries. However, a *Random Walk* equivalency test method is also available.

One that wants to use *pylstar* must write a class that exposes the Minimaly Adequate Teacher of the targeted reactive System. This can be done by subclassing `pylstar.ActiveKnowledgeBase.ActiveKnowledgeBase`. If the targeted process is a network server, one can solely subclass `pylstar.NetworkActiveKnowledgeBase`.

For example, the following class could be use to create a MAT out of a coffee machine (`coffeemachine.py`) that exposes an API on `localhost:3000` :

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

With your MAT implementation, the following snippet can be used to trigger the automatic inference of the coffee machine. This code returns a `pylstar.automata.Automata.Automata` (and prints its DOT code) that best describes the behavior of your coffee machine.

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

A runnable example of the coffee machine inference is available in `test/src/test_pylstar/coffee_machine_example`.

## Installation

Pylstar is a typical python library. It relies on a `setup.py` file to describe its installation process:
```bash
# python setup.py install 
```

## Testing and documentations

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
