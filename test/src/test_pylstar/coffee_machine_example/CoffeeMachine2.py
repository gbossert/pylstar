#!/usr/bin/env python


import socket
import sys
from thread import *


class WaterIsFullException(Exception):
    pass
class CoffeeIsFullException(Exception):
    pass
class NotEnoughWaterException(Exception):
    pass
class NotEnoughCoffeeException(Exception):
    pass
class InvalidOrderException(Exception):
    pass
class CoffeeMachineIsOff(Exception):
    pass
    

class CoffeeMachine(object):
    """Light implementation of a coffee machine.
    The coffee machine has the following attributes:
    
    * a specific amount of coffee it contains
    * a specific amount of water it contains

    The coffee machine exposes the following commands:
    * a refill_water command that entirely refills the coffee machine with water
    * a refill_coffee command that entirely refills the coffee machine with coffee
    * a press_button_a command that triggers the production of a coffee made of 1 dose of water and 1 dose of coffee
    * a press_button_b command that triggers the production of an expresso coffee made of 1 dose of water and 3 doses of coffee
    * a press_button_c command that switch on/off the coffee machine

    """


    MAX_WATER = 3
    MAX_COFFEE = 3
    
    def __init__(self):
        self._qte_water = 0
        self._qte_coffee = 0
        self._switch_on = False

    def __refill_water(self):
        if self._qte_water == CoffeeMachine.MAX_WATER:
            raise WaterIsFullException()
        
        self._qte_water = CoffeeMachine.MAX_WATER

        return "DONE"

    def __refill_coffee(self):
        if self._qte_coffee == CoffeeMachine.MAX_COFFEE:
            raise CoffeeIsFullException()
        
        self._qte_coffee = CoffeeMachine.MAX_COFFEE
        
        return "DONE"

    def __press_button_a(self):

        if not self._switch_on:
            raise CoffeeMachineIsOff()
        
        if self._qte_water == 0:
            raise NotEnoughWaterException()
        
        if self._qte_coffee == 0:
            raise NotEnoughCoffeeException()

        self._qte_water -= 1
        self._qte_coffee -= 1

        return "NORMAL COFFEE IS SERVED"

    def __press_button_b(self):

        if not self._switch_on:
            raise CoffeeMachineIsOff()
        
        if self._qte_water == 0:
            raise NotEnoughWaterException()
        
        if self._qte_coffee <= 2:
            raise NotEnoughCoffeeException()

        self._qte_water -= 1
        self._qte_coffee -= 2

        return "EXPRESSO IS SERVED"

    def __press_button_c(self):

        if self._qte_water == 1:
            raise NotEnoughWaterException()
        
        self._switch_on = not self._switch_on

        if not self._switch_on:
            return "COFFEE MACHINE IS OFF"
        else:
            return "COFFEE MACHINE IS ON"

    def execute_command(self, command):
        try:
            if command is None:
                raise Exception("Command cannot be None")

            command = command.strip()

            if command == "REFILL_WATER":
                return self.__refill_water()
            elif command == "REFILL_COFFEE":
                return self.__refill_coffee()
            elif command == "PRESS_BUTTON_A":
                return self.__press_button_a()
            elif command == "PRESS_BUTTON_B":
                return self.__press_button_b()
            elif command == "PRESS_BUTTON_C":
                return self.__press_button_c()
            else:
                raise Exception("Unknown command")
            
        except Exception as e:
            print(e)
            return "ERROR"

        
def clientthread(conn):

    coffee_machine = CoffeeMachine()
    #Sending message to connected client
    while True:

        order = conn.recv(1024)
        if not order:
            break
        response = coffee_machine.execute_command(order)+"\n"
        conn.sendall(response)
        
def main():

    host = "127.0.0.1"
    port = 3000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : {}'.format(msg))
        sys.exit()

    s.listen(10)
    print("Server is started and listenning")

    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print("Connected with {}:{}".format(addr[0], addr[1]))
     
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))
 
    s.close()    
    

if __name__ == "__main__":
    main()

    

    
    
