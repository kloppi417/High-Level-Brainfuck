addresses = [-1] # all the addresses in BF memory of variables

def find_valid_address(mem_length: int):
    global addresses
    addresses.sort()
    for index, address in enumerate(addresses): # Search for a gap in memory
        if address == -1: continue
        if address - (addresses[index - 1] + 1) >= mem_length:
            return addresses[index - 1] + 1
    # No gap in memory is found
    return addresses[len(addresses) - 1] + 1

class Primitive:
    def __init__(self, name: str, datatype):
        self.name = name
        self.datatype = datatype



class Integer: # Integers take up 4 bytes of data, being 32-bit signed ints
    def __init__(self, name: str, value: int | None = None):
        global addresses
        self.name = name
        self.value = value
        self.datatype = "INTEGER"
        # self.data_length = 4 # length in bytes
        
        # [addresses.append(self.address + i) for i in range(4)]

class Boolean:
    def __init__(self, name: str, value: bool | None = None):
        global addresses
        self.name = name
        self.value = value
        self.datatype = "BOOLEAN"
        self.data_length = 1
        # self.address = find_valid_address(self.data_length)

        # addresses.append(self.address)

class String: # Strings are an unfixed size, so memory is not allocated at initialization
    def __init__(self, name: str, value: str | None = None):
        global addresses
        self.name = name
        self.value = value
        self.datatype = "STRING"
        self.data_length = len(self.value)
        # self.address = find_valid_address(self.data_length)

        # [addresses.append(self.address + i) for i in range(len(self.value))]