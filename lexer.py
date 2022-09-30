import string
from utils.tokens import Token, TokenType

WHITESPACE = " \n\t"
DIGITS = "1234567890"
MATH_OPERANDS = "+-*/"
SCOPING = "(){}"
KEYWORDS = ["function", "while", "return", "const", "import", "throw"]
VAR_NAMES = string.ascii_letters + "_"
COMPARISONS = "=><|&!"
STRINGS = "'" + '"'
STRING_CHARS = string.printable[0:len(string.printable)-4] + " "
DATATYPES: list[tuple[str, str]] = [("int", "INTEGER"), ("str", "STRING"), ("bool", "BOOLEAN")]

class Lexer:

    def __init__(self, input: str):
        self.input = iter(input)
        self.tokens: list[Token] = []
        self.advance()
    
    def advance(self):
        try:
            self.current_char = next(self.input)
        except StopIteration:
            self.current_char = None
    
    def generate_tokens(self):
        while self.current_char != None:

            if self.current_char == "#": # comment
                while self.current_char != "\n":
                    self.advance()
            
            if self.current_char in WHITESPACE:
                self.advance()

            if self.current_char in DIGITS:
                self.tokens.append(self.generate_number())
            if self.current_char in VAR_NAMES: # also accounts for booleans, keywords and datatyping
                self.tokens.append(self.generate_variable())
            if self.current_char in COMPARISONS: # also accounts for assignment
                self.tokens.append(self.generate_comparison())
            if self.current_char in STRINGS:
                self.tokens.append(self.generate_string())
            if self.current_char in MATH_OPERANDS: # also accounts for "->" operator
                self.tokens.append(self.generate_math_oper())
            if self.current_char == "@":
                self.tokens.append(self.generate_decorator())

            if self.current_char in SCOPING:
                self.tokens.append(Token(TokenType.SCOPING, self.current_char))
            if self.current_char == ";":
                self.tokens.append(Token(TokenType.ENDLINE, ";"))
            if self.current_char == ",":
                self.tokens.append(Token(TokenType.COMMA, ","))
            if self.current_char == ".":
                self.tokens.append(Token(TokenType.PERIOD, "."))
            
            self.advance()
        
        return self.tokens
    
    def generate_number(self):
        with_dot = "." + DIGITS
        number_str = self.current_char
        dot_number = 0
        self.advance()
        while self.current_char != None and self.current_char in with_dot:
            number_str += self.current_char
            if self.current_char == ".":
                dot_number += 1
            self.advance()
        if dot_number == 0:
            return Token(TokenType.INTEGER, int(number_str))
        elif dot_number == 1:
            return Token(TokenType.FLOAT, number_str)
        else:
            raise Exception("Invalid float! Too many dots in float")
    
    def generate_variable(self):
        variable_str = self.current_char
        self.advance()
        while self.current_char != None and self.current_char in VAR_NAMES:
            variable_str += self.current_char
            self.advance()
        if variable_str == "false":
            return Token(TokenType.BOOLEAN, False)
        elif variable_str == "true":
            return Token(TokenType.BOOLEAN, True)
        elif variable_str in KEYWORDS:
            return Token(TokenType.KEYWORD, variable_str)
        for datatype in DATATYPES:
            if variable_str == datatype[0]:
                return Token(TokenType.DATATYPE, datatype[1])

        return Token(TokenType.VARIABLE, variable_str)

    def generate_comparison(self):
        comparison_str = self.current_char
        self.advance()
        while self.current_char != None and self.current_char in COMPARISONS:
            comparison_str += self.current_char
            self.advance()
        if comparison_str == "=":
            return Token(TokenType.ASSIGNMENT, "=")
        return Token(TokenType.COMPARISON, comparison_str)
    
    def generate_string(self):
        open_char = self.current_char
        string_str = ""
        self.advance()
        while self.current_char != None and self.current_char in STRING_CHARS and self.current_char != open_char:
            string_str += self.current_char
            self.advance()
        # self.advance()
        return Token(TokenType.STRING, string_str)
    
    def generate_math_oper(self):
        oper_str = ""
        while self.current_char != None and self.current_char in MATH_OPERANDS:
            oper_str += self.current_char
            self.advance()
            if oper_str == "-" and self.current_char == ">":
                return Token(TokenType.KEYWORD, "->")
        return Token(TokenType.MATHOPERAND, oper_str)
    
    def generate_decorator(self):
        self.advance()
        token = self.generate_variable()
        token.type = TokenType.DECORATOR
        return token
