def find_factors(n):
    unorganized_factors: list[int] = []
    factors: list[tuple[int, int]] = []

    for i in range(1, n + 1):
        if n % i == 0:
            unorganized_factors.append(i)
    
    length = len(unorganized_factors) / 2
    for i in range(int(length)):
        f1 = unorganized_factors[i]
        f2 = unorganized_factors[len(unorganized_factors) - 1 - i]
        factors.append((f1, f2))

    return factors

def find_min_factor_pair(factors):
    min_factor_sum = 0
    for index, factor in enumerate(factors):
        if factor[0] + factor[1] < factors[min_factor_sum][0] + factors[min_factor_sum][1]:
            min_factor_sum = index
    return min_factor_sum

def generate_bf_number(number: int):
    if number == 0 or number == 1:
        return "" if number == 0 else "+"
    min_factor_pair_index = 0
    min_factor_sum = 20
    decrement = -1

    while min_factor_sum >= 20:
        decrement += 1
        if (number - decrement) == 0:
            factors = find_factors(number)
            min_factor_pair_index = find_min_factor_pair(factors)
            break
        factors = find_factors(number - decrement)
        min_factor_pair_index = find_min_factor_pair(factors)
        min_factor_sum = factors[min_factor_pair_index][0] + factors[min_factor_pair_index][1]
    
    min_factors = factors[min_factor_pair_index]
    f1_string = "".join(["+" for i in range(min_factors[0])])
    f2_string = "".join(["+" for i in range(min_factors[1])])
    increment = "".join(["+" for i in range(decrement)])
    return f"{f1_string}[->{f2_string}<]>{increment}"

def split_string(string: str, chunk_size: int):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

def move_to_cell(cell: int, pointer_pos: int) -> tuple[int, str]:
    output = ""
    while cell > pointer_pos:
        pointer_pos += 1
        output += ">"
    while cell < pointer_pos:
        pointer_pos -= 1
        output += "<"
    return (pointer_pos, output)

def int_to_8bit(n) -> str:
    while n > 255:
        n -= 255
    bnr = bin(n).replace('0b','')
    while len(bnr) < 8:
        bnr = f"0{bnr}"
    return bnr

def bin_to_int(n) -> int:
    return int(n, 2)

# 
# 128 132 30 0
# binary = bin(0)[2:len(bin(0))] + bin(30)[2:len(bin(30))] + bin(132)[2:len(bin(132))] + bin(128)[2:len(bin(128))]
# print(int(binary, 2))