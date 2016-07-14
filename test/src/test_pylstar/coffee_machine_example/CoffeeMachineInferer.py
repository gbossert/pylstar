#!/usr/bin/env python

import subprocess
import sys
import os
import time

sys.path.append("../../../../src")
from pylstar.LSTAR import LSTAR
from pylstar.NetworkActiveKnowledgeBase import NetworkActiveKnowledgeBase

class CoffeeMachineKnowledgeBase(NetworkActiveKnowledgeBase):

    def __init__(self, executable):
        super(CoffeeMachineKnowledgeBase, self).__init__("127.0.0.1", 3000)
        self.__sp = None
        self.__executable = executable

    def start(self):
        print("Starting coffeemachine target")
        coffee_path = self.__executable
        self.__sp = subprocess.Popen("/usr/bin/python {}".format(coffee_path), shell=True)
        time.sleep(5)
        
    def stop(self):
        print("Stoping coffeemachine")
        if self.__sp is not None:
            self.__sp.kill()


def main():

    usage = "Usage: CoffeeMachineInferer.py 1|2"

    if len(sys.argv)!= 2:
        print(usage)
        sys.exit(-1)

    id_coffee_machine = sys.argv[1]
    if id_coffee_machine == "1":
        executable = "CoffeeMachine1.py"
    elif id_coffee_machine == "2":
        executable = "CoffeeMachine2.py"
    else:
        print(usage)
        sys.exit(-1)
              
    
    input_vocabulary = [
        "REFILL_WATER",
        "REFILL_COFFEE",
        "PRESS_BUTTON_A",
        "PRESS_BUTTON_B",
        "PRESS_BUTTON_C"    
    ]
    coffeeBase = CoffeeMachineKnowledgeBase(executable)
    try:
        coffeeBase.start()
        lstar = LSTAR(input_vocabulary, coffeeBase, max_states = 10)
        coffee_state_machine = lstar.learn()
    finally:
        coffeeBase.stop()
        
    dot_code = coffee_state_machine.build_dot_code()
    print(dot_code)

    output_file = "coffee_machine_{}.dot".format(id_coffee_machine)

    with open(output_file, "w") as fd:
        fd.write(dot_code)

    print("==> Coffee machine {} Automata dumped in {}".format(id_coffee_machine, output_file))
    print("Knowledge base stats: {}".format(coffeeBase.stats))


if __name__ == "__main__":
    main()
