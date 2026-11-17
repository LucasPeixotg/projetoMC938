

# constants
MASK_329 = (1 << 329) - 1
T = (3**8) * (5**4) * (19**4) * (62**4)

def rotl(word: int, shift: int) -> int:
    """left rotation of 329 bits"""
    shift %= 329
    return ((word << shift) | (word >> (329 - shift))) & MASK_329


def x_function(word: int) -> int:
    pass

def rotation_amount(alfa: int) -> list[tuple[int,int,int,int]]:
    B = alfa % T

    r1 = (0, 0, 0, 0)
    for t in range(4):
        r1[t] = 1 + (B % 3)
        B //= 3

    r2 = (0, 0, 0, 0)
    r3 = (0, 0, 0, 0)
    for t in range(4):
        r2[t] = 4 + (B % 3)
        r3[t] = 7 + ((2 * r1[t] + r2[t] + 1) % 3)
        B //= 3

    i_values = (0, 0, 0, 0)
    for t in range(4):
        i_values[t] = B % 5
        B //= 5

    j_values = (0, 0, 0, 0)
    for t in range(4):
        j_values[t] = B % 19
        B //= 19

    l_values = (0, 0, 0, 0)
    for t in range(4):
        l_values[t] = B % 62
        B //= 62

    return r1, r2, r3, i_values, j_values, l_values


def theta(word: int, r1: int, r2: int) -> int:
    r3 = 7 + ((2 * r1 + r2) % 3)
    return word ^ rotl(word, r1) ^ rotl(word, r2) ^ rotl(word, r3) 

def affine_layer(words: list[int], alfa: int):
    pass

if __name__ == "__main__":
    print(rotl(124, 13))