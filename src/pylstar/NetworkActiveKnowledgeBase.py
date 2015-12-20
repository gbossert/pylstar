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
import socket

# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger
from pylstar.ActiveKnowledgeBase import ActiveKnowledgeBase
from pylstar.Letter import Letter, EmptyLetter
from pylstar.Word import Word

@PylstarLogger
class NetworkActiveKnowledgeBase(ActiveKnowledgeBase):

    def __init__(self, target_host, target_port, timeout=5):
        super(NetworkActiveKnowledgeBase, self).__init__()        
        self.target_host = target_host
        self.target_port = target_port
        self.timeout = timeout

    def start_target(self):
        pass

    def stop_target(self):
        pass

    def submit_word(self, word):
        self._logger.debug("Submiting word '{}' to the network target".format(word))

        output_letters = []
        
        socket = socket.socket()
        # Reuse the connection
        socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.settimeout(self.timeout)
        socket.connect((self.target_host, self.target_remote))
        try:
            output_letters = [self._submit_letter(socket, letter) for letter in word.letters]
        finally:
            socket.close()

        return Word(letters=output_letters)
            
    def _submit_letter(self, socket, letter):
        output_letter = EmptyLetter()
        try:
            to_send = str(letter.symbol)        
            output_letter = Letter(self._send_and_receive(socket, to_send))
        except Exception, e:
            self._logger.debug(e)
            
        return output_letter
        

    def _send_and_receive(self, socket, data):
        socket.sendall(data)
        return socket.recv(1024)

        
        


        
