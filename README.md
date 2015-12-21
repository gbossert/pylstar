# pylstar : An implementation of the LSTAR Grammatical Inference Algorithm

[![Build Status](https://travis-ci.org/gbossert/pylstar.svg?branch=master)](https://travis-ci.org/gbossert/pylstar)
[![Coverage Status](https://coveralls.io/repos/gbossert/pylstar/badge.svg?branch=master&service=github)](https://coveralls.io/github/gbossert/pylstar?branch=master)


**Warning : This implementation is only intented for testing purposes : Work in Progress.**

## About  LSTAR
The LSTAR Grammatical inference algorithm is intented to infer the automata that describes a targeted determinist reactive systems if a Minimally Adequate Teacher (MAT) exists for it.
As stated by G. Holzman in its reference book, a MAT is "an Oracle that give answers to membership queries and strong equivalence queries.".

The general idea of the algorithm :

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
It should be noted that this implementation follows the original description of the Angluin's algorithm and relies on *WMethod* to produce the required equivalence queries.

One that wants to use *pylstar* must write a class that exposes the Minimaly Adequate Teacher of the targeted reactive System. This can be done by subclassing `pylstar.ActiveKnowledgeBase.ActiveKnowledgeBase`. For example, the following class could be use to create a MAT out of a coffee machine :
```python
from CoffeeMachineCommandAndControl import CoffeeMachineCommandAndControl
from pylstar.ActiveKnowledgeBase import ActiveKnowledgeBase

class CoffeeMachineMAT(ActiveKnowledgeBase):

    def __init__(self):
        super(ActiveKnowledgeBase, self).__init__()        
        self.coffee_machine = CoffeeMachineCommandAndControl()
    def start_target(self):
        self.coffee_machine_start()
    def stop_target(self):
        self.coffee_machine.stop()
    def submit_word(self, word):
        output_letters = []
        for input_letter in word.letters:
            output_letters.append(self.coffee_machine.execute_command(input_letter))
        return Word(output_letter)
```

With your MAT implementation, the following snippet can be used to trigger the automatic inference of the targeted reactive system. This code returns a `pylstar.automata.Automata.Automata` that best describes the behavior of your coffee machine.

```python
mat = CoffeeMachineMAT()
input_vocabulary = ["REFILL_WATER", 
                    "REFILL_COFFEE", 
                    "PRESS_BUTTON_1", 
                    "PRESS_BUTTION_2", 
                    "PRESS_BUTTON_3"]
lstar = LSTAR(input_vocabulary, mat, max_states = 15)
coffee_machine_automata = lstar.learn()
```

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
