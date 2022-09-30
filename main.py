from transpiler import transpile
from repl import bf_repl, hlbf_repl
CLEAR_CONSOLE = "".join(["\n" for x in range(30)])

def main():
    done = False
    while not done:
        action = input(CLEAR_CONSOLE + "Type the number of the tool you want.\n1. Brainfuck Interpreter\n2. HLBF Compiler\n3. HLBF Interpreter\n4. Exit\n")
        match action:
            case "1":
                bf_repl()
            case "2":
                hlbf_comp()
            case "3":
                hlbf_repl()
            case "4":
                done = True
            case _:
                print("Not a valid tool")
                action = False

def hlbf_comp():
    pass

if __name__ == "__main__":
    main()