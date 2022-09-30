from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    INTEGER      = 1 # 1, 2, 3, etc
    BOOLEAN      = 2 # true, false
    STRING       = 3 # "hi", "hello world"
    FLOAT        = 4 # 69.420, 1.29
    VARIABLE     = 5 # x, y, distance
    ASSIGNMENT   = 6 # =
    SCOPING      = 7 # {, }
    COMPARISON   = 8 # ==, >=, <=, !=, >, <
    KEYWORD      = 9 # function, while
    DATATYPE     = 10 # int, string, bool
    ENDLINE      = 11 # ;
    MATHOPERAND  = 12 # +, -, *, /, (, )
    DECORATOR    = 13 # @
    COMMA        = 14 # ,
    PERIOD       = 15 # .

@dataclass
class Token():
    def __init__(self, type: TokenType, value = None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else '')