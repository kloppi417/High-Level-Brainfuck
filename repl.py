from transpiler import transpile
from utils.functions import int_to_8bit, bin_to_int

CLEAR_CONSOLE = "".join(["\n" for x in range(30)])

def hlbf_repl():
    print(CLEAR_CONSOLE)
    print("High Level Brainfuck REPL v1.0.0. Type '.exit' to exit")
    done = False
    while not done:
        try:
            cmd = input(">>>")
            if cmd == ".exit":
                done = True
                break
            try:
                out = transpile(cmd)
                print(out[0])
                print(out[1])
            except Exception: # any error here is a proper exception made by the transpiler
                pass
        except KeyboardInterrupt:
            done = True

def bf_repl():
    done = False
    print(CLEAR_CONSOLE + "Brainfuck REPL v1.0.0. Type '.exit' to exit")
    mem = [0 for byte in range(30)]
    p = 0
    while not done:
        try:
            cmd = input(">>>")
            if cmd == ".exit":
                done = True
                break
            match list(cmd):
                case "+": 
                    bit = bin_to_int(mem[p])
                    bit += 1
                    mem[p] = int_to_8bit(bit)
                case "-": 
                    bit = bin_to_int(mem[p])
                    bit -= 1
                    mem[p] = int_to_8bit(bit)
                case ">": 
                    p += 1
                case "<": 
                    p -= 1
                case ".": 
                    pass
                case ",": 
                    pass
                case "[": 
                    pass
                case "]": 
                    pass


        except KeyboardInterrupt:
            done = True