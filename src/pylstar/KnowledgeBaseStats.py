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
import abc

# +----------------------------------------------------------------------------
# | Pylstar Imports
# +----------------------------------------------------------------------------
from pylstar.tools.Decorators import PylstarLogger


@PylstarLogger
class KnowledgeBaseStats(object):

    def __init__(self):
        self.nb_query = 0
        self.nb_submited_query = 0
        self.nb_letter = 0
        self.nb_submited_letter = 0
        
    def __str__(self):
        return """
\t- nb query= {nb_query}
\t- nb submited query= {nb_submited_query}
\t- nb letter= {nb_letter}
\t- nb submited letter= {nb_submited_letter}

""".format(nb_query = self.nb_query,
               nb_letter = self.nb_letter,
               nb_submited_query = self.nb_submited_query,
               nb_submited_letter = self.nb_submited_letter)

    @property
    def nb_submited_query(self):
        """Number of query submited to the target"""
        return self.__nb_submited_query

    @nb_submited_query.setter
    def nb_submited_query(self, nb_submited_query):
        if nb_submited_query is None:
            raise Exception("Nb submited query cannot be None")
        nb_submited_query = int(nb_submited_query)
        if nb_submited_query < 0:
            raise Exception("Nb submited query must be > 0")
        
        self.__nb_submited_query = nb_submited_query

    @property
    def nb_submited_letter(self):
        """Number of letter submited to the target"""
        return self.__nb_submited_letter

    @nb_submited_letter.setter
    def nb_submited_letter(self, nb_submited_letter):
        if nb_submited_letter is None:
            raise Exception("Nb submited letter cannot be None")
        nb_submited_letter = int(nb_submited_letter)
        if nb_submited_letter < 0:
            raise Exception("Nb submited letter must be > 0")
        
        self.__nb_submited_letter = nb_submited_letter

    
    @property
    def nb_letter(self):
        """Number of letters triggered while infering"""
        return self.__nb_letter

    @nb_letter.setter
    def nb_letter(self, nb_letter):
        if nb_letter is None:
            raise Exception("Nb letter cannot be None")
        nb_letter = int(nb_letter)
        if nb_letter < 0:
            raise Exception("Nb letter must be > 0")
        
        self.__nb_letter = nb_letter

    @property
    def nb_query(self):
        """Number of queries triggered while infering"""
        return self.__nb_query

    @nb_query.setter
    def nb_query(self, nb_query):
        if nb_query is None:
            raise Exception("Nb query cannot be None")
        nb_query = int(nb_query)
        if nb_query < 0:
            raise Exception("Nb query must be > 0")
        
        self.__nb_query = nb_query
        
        

    
