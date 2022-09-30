from parser import Parser
from lexer import Lexer
from utils.tokens import Token
from utils.nodes import Nodes
from utils.error import Error

def transpile(code) -> tuple[list[Token], list[Nodes]]:
    # file = open("test.hlbf", "r").read()
    file = code

    __tokens__ = Lexer(file).generate_tokens()

    parser = Parser(__tokens__)

    __nodes__ = parser.generate_nodes()

    BUFFER_END_INDEX = 4 # Five bits of buffer data
    pointer = 0
    compiled = []

    # for node in __nodes__:

    #     node_name = node.__class__.__name__

    #     if node_name == "VariableInitializationNode":
    #         pass

    #     if node_name == "VariableAssignmentNode":
    #         pass
    
    # return [__tokens__, __nodes__]
    # print(__tokens__)
    print(__nodes__)

file = open("test.hlbf", "r")
transpile(file.read())
file.close()

        

# for node in __nodes__:

#     node_name = node.__class__.__name__

#     if node_name == "VariableInitializationNode":
#         pass

#     if node_name == "VariableAssignmentNode":
#         var = [var for var in parser.variables if var.name == node.name][0]
#         addr = var.address + BUFFER_END_INDEX + 1
#         pointer, temp = utils.move_to_cell(addr, pointer)
#         compiled.append(temp)
#         del temp
#         if var.datatype == "INTEGER":
#             bin_int = bin(node.value)[2:len(bin(node.value))]
#             while len(bin_int) < 32:
#                 bin_int = '0' + bin_int
#             cells = utils.split_string(bin_int, 8)
#             for cell in cells: # leaves you on the cell after the four bits of integer data
#                 compiled.append("[-]")
#                 lshift = 0
#                 lshift_str = ""
#                 while pointer != BUFFER_END_INDEX: # last bit of available buffer
#                     pointer -= 1
#                     lshift += 1
#                     lshift_str += "<"
#                     compiled.append("<")
#                 compiled.append(f"[-]<[-]{utils.generate_bf_number(int(cell, 2))}")
#                 rshift_str = ""
#                 while lshift > 0:
#                     rshift_str += ">"
#                     lshift -= 1
#                 compiled.append(f"[-{rshift_str}+{lshift_str}]{rshift_str}")
#                 for i in range(len(rshift_str)):
#                     pointer += 1
#                 compiled.append(">")
#                 pointer += 1
#         if var.datatype == "BOOLEAN":
#             b = "+" if node.value == True else ""
#             compiled.append(f"[-]{b}")
#         if var.datatype == "STRING":
#             ascii_arr = [ord(c) for c in node.value]


# # print("".join(compiled))




# # for byte in int_temp:
# #     val = int(byte, 2)
# #     for x in range(val):
# #         compiled.append("+")
# #     compiled.append(">")

# # print("".join(compiled))
