from utils.variables import *
from dataclasses import dataclass
import typing

@dataclass
class VariableInitializationNode():
    datatype: str
    name: str

    def __repr__(self):
        return f"{self.datatype} {self.name}"

@dataclass
class VariableAssignmentNode():
    name: str
    value: int | bool | str

    def __repr__(self):
        return f"{self.name} = {self.value}"

@dataclass
class VariableCopyNode():
    original: str
    target: str

    def __repr__(self):
        return f"copy {self.original} to {self.target}"

@dataclass
class IntegerIncrementNode():
    variable: str

    def __repr__(self):
        return(f"{self.variable}++")

@dataclass
class IntegerDecrementNode():
    variable: str

    def __repr__(self):
        return(f"{self.variable}--")

@dataclass
class AddNode():
    a: int | str
    b: int | str

    def __repr__(self):
        left  = str(self.a)
        right = str(self.b)
        return(f"{left} + {right}")

@dataclass
class SubtractNode():
    a: int | str
    b: int | str

    def __repr__(self):
        left  = str(self.a)
        right = str(self.b)
        return(f"{left} - {right}")

@dataclass
class MultiplyNode():
    a: int | Integer
    b: int | Integer

    def __repr__(self):
        left  = str(self.a) if type(self.a) == int else str(self.a.value)
        right = str(self.b) if type(self.b) == int else str(self.b.value)
        return(f"{left} * {right}")

@dataclass
class DivideNode():
    a: int | Integer
    b: int | Integer

    def __repr__(self):
        left  = str(self.a) if type(self.a) == int else str(self.a.value)
        right = str(self.b) if type(self.b) == int else str(self.b.value)
        return(f"{left} / {right}")

@dataclass
class MathExpressionNode():
    operations: list[str]

    def __repr__(self):
        return [operation + "\n" for operation in self.operations]

@dataclass
class FunctionDeclarationNode():
    name: str
    parameters: list[tuple[str, str]] # [(datatype, name)]
    param_count: int
    return_type: str
    code: list

    def __repr__(self):
        return f"function {self.name} with {self.param_count} parameters {[p[0] + ' ' + p[1] for p in self.parameters]} -> {self.return_type} {'{' + ', '.join([str(node) for node in self.code]) + '}'}"

Nodes = VariableInitializationNode | VariableAssignmentNode | VariableCopyNode | IntegerIncrementNode | IntegerDecrementNode | AddNode | SubtractNode | MultiplyNode | DivideNode | FunctionDeclarationNode