from ast import arg
from utils.nodes import *
from utils.tokens import TokenType, Token

DATATYPES = ["INTEGER", "BOOLEAN", "STRING"]

class Parser():

    def __init__(self, tokens: list[Token]):
        self.tokens = iter(tokens)
        self.nodes: list[Nodes] = []
        self.variables = {} # key is var name, value is var datatype
        self.functions = [
            {
                "name": "<name>",
                "parameters": [
                    "<param_datatype>"
                ],
                "return": "<datatype>"
            }
        ]
        self.advance()
    
    def advance(self) -> None:
        try:
            self.current_token = next(self.tokens)
            # print(self.current_token)
        except StopIteration:
            self.current_token = None
    
    def generate_nodes(self):
        while self.current_token != None:

            try:
                # print(self.current_token.type == TokenType.DATATYPE)
                self.generate_function()
                self.initialize_variable()
            except StopIteration:
                raise Exception("Invalid syntax")
            
            self.advance()
        return self.nodes
    
    def initialize_variable(self):
        create_new_var = False
        if self.current_token.type == TokenType.DATATYPE: # Instantiating a new variable
            create_new_var = True
            var_datatype = self.current_token.value
            self.advance()
            if self.current_token.type != TokenType.VARIABLE: # Invalid variable name
                raise Exception(f"Cannot use {self.current_token.type.name} as a variable name!")
        if self.current_token.type == TokenType.VARIABLE: # Current token is a variable
            var_name = self.current_token.value
            var_exists = var_name in [key for key in iter(self.variables)]
            if var_exists: # Variable already exists in memory
                if create_new_var: # Trying to create a variable that already exists in memory
                    raise Exception(f"Variable {self.current_token.value} already exists!")
                else: # Variable in memory is being accessed
                    self.advance()
                    if self.current_token.type == TokenType.ASSIGNMENT: # Variable is attempted to be re-assigned
                        self.advance()
                        self.assign_variable(var_name, self.current_token)
                    else: # Variable is being accessed in some way that isnt being reassigned
                        self.advance()
                        self.access_variable(var_name) 
            else: # Variable does not exist in memory
                if create_new_var: # Trying to create a new variable
                    self.nodes.append(VariableInitializationNode(var_datatype, var_name))
                    self.variables[var_name] = var_datatype
                    self.advance()
                    if self.current_token.type != TokenType.ENDLINE: # Variable is being instantiated and has code after instatiation
                        if self.current_token.type == TokenType.ASSIGNMENT: # Variable is being instantiated and assigned on one line
                            self.advance()
                            self.assign_variable(var_name, self.current_token)
                        else: # Code after instantiation is not assignment code
                            raise Exception("Statement not terminated with ';'")
                else: # Variable is being accessed without being instantiated
                    raise Exception(f"Cannot access variable {self.current_token.value} before assignment!")
    
    def assign_variable(self, var_name: str, current_token: Token):
        var_datatype = self.variables[var_name]
        if current_token.type == TokenType.VARIABLE: # var_obj is being assigned to a variable
            old_var = current_token.value
            old_var_exists = old_var in [key for key in iter(self.variables)]
            if old_var_exists: # Variable that is being assigned to var_obj exists in memory
                if self.variables[old_var] != var_datatype: # Variable that is being assigned to var_obj is not the same datatype as var_obj
                    raise Exception(f"Variable with type {var_datatype} cannot be assigned to variable with type {self.variables[old_var]}")
                else:
                    self.nodes.append(VariableCopyNode(old_var, var_name))
            else:
                raise Exception(f"Cannot access variable {current_token.value} before assignment!")
        elif current_token.type.name in DATATYPES:
            if var_datatype != current_token.type.name: # Variable is trying to be assigned to the wrong datatype
                raise Exception(f"Variable with type {var_datatype} cannot be assigned to type {current_token.type.name}")
            else: # Variable successfully gets reassigned to a primitive datatype
                self.nodes.append(VariableAssignmentNode(var_name, current_token.value))
                self.advance()
                if self.current_token.type != TokenType.ENDLINE:
                    if self.current_token.type == TokenType.MATHOPERAND or self.current_token.type == TokenType.INTEGER:
                        self.make_expr()
        else:
            raise Exception(f"Variable cannot be assigned to {self.current_token.value}")
    
    def access_variable(self, var_name):
        if self.current_token.value == "(":
            self.advance()
            self.call_function(var_name)
            return
        print("Variable being accessed, and not being assigned")
    
    def make_expr(self): # BAD CODE
        if self.current_token.type == TokenType.INTEGER:
            return self.current_token.value
        else:
            raise Exception("I haven't programmed mathematical expressions yet teehee <3")
        # while self.current_token.type == TokenType.MATHOPERAND:
        #     if self.current_token.value == "(":
        #         while self.current_token.value != ")":

        #             self.advance()
        #     self.advance()
    
    def generate_function(self):
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == "function":
            name = None
            parameters = []
            return_type = None
            code = []
            self.advance()
            if self.current_token.type != TokenType.VARIABLE:
                raise Exception(f"{self.current_token.value} cannot be used as a function name")
            name = self.current_token.value
            if name in [fn["name"] for fn in self.functions]:
                raise Exception(f"Function with name {name} is already declared!")
            self.advance()
            if self.current_token.value != "(":
                raise Exception(f"Invalid function declaration")
            self.advance()
            comma = True
            while self.current_token.value != ")":
                if not comma:
                    raise Exception("Parameters must be separated with a comma")
                if self.current_token.type != TokenType.DATATYPE:
                    raise Exception(f"{self.current_token.value} is not a datatype.")
                param_datatype = self.current_token.value
                self.advance()
                if self.current_token.type != TokenType.VARIABLE:
                    raise Exception(f"{self.current_token.value} is not a valid parameter name")
                param_name = self.current_token.value
                parameters.append((param_datatype, param_name))
                self.advance()
                comma = False if self.current_token.type != TokenType.COMMA else True
                if comma:
                    self.advance()
            self.advance()
            if self.current_token.type != TokenType.KEYWORD or self.current_token.value != "->":
                raise Exception("Functions must have the return operator '->'")
            self.advance()
            if self.current_token.type == TokenType.DATATYPE:
                return_type = self.current_token.value
                self.advance()
            if self.current_token.type != TokenType.SCOPING and self.current_token.value != "{":
                raise Exception("Need '{' in a function lmao")
            curly_braces = 1
            tokens = []
            while curly_braces > 0:
                self.advance()
                if self.current_token == None:
                    raise Exception("Unclosed curly brace!")
                if self.current_token.type == TokenType.SCOPING and self.current_token.value == "{":
                    curly_braces += 1
                if self.current_token.type == TokenType.SCOPING and self.current_token.value == "}":
                    curly_braces -= 1
                tokens.append(self.current_token)
            code = Parser(tokens).generate_nodes()
            self.nodes.append(FunctionDeclarationNode(name, parameters, len(parameters), return_type, code))
            self.functions.append({
                "name": name,
                "parameters": [param[0] for param in parameters],
                "return": return_type
            })
                
        # self.advance()
    def call_function(self, var_name): # starts on the token after the opening '(' for the function
        arguments = []
        while self.current_token.value != ")":
            arg = []
            while self.current_token.type != TokenType.COMMA:
                arg.append(self.current_token)
                self.advance()
            arguments.push(self.generate_nodes(arg))



