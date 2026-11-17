

# constants
MASK_329 = (1 << 329) - 1
MASK_11956 = (1 << 11956) - 1
T = (3**8) * (5**4) * (19**4) * (62**4)

def rotl(word: int, shift: int) -> int:
    """left rotation of 329 bits"""
    shift %= 329
    return ((word << shift) | (word >> (329 - shift))) & MASK_329

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


def theta(word: int, r1: int, r2: int, r3: int) -> int:
    return word ^ rotl(word, r1) ^ rotl(word, r2) ^ rotl(word, r3) 

def x_function(word: int) -> int:
    """
    yi = xi+1xi+2 + xi + xi+2.
    """
    x1 = rotl(word, 1)
    x2 = rotl(word, 2)
    y = ((x1 & x2) ^ word ^ x2) & MASK_329
    return y

def non_linear_layer(state: list[int]) -> list[int]:
    return [
        x_function(state[0]),
        x_function(state[1]),
        x_function(state[2]),
        x_function(state[3]),
        x_function(state[4]),
    ]

def column_parity_mixer(state: list[int], r1: int, r2: int, r3: int) -> list[int]:
    w0, w1, w2, w3, w4 = state
    theta_result = theta(w0 ^ w1 ^ w2 ^ w3 ^ w4, r1, r2, r3)
    return [
        w0 ^ theta_result,
        w1 ^ theta_result,
        w2 ^ theta_result,
        w3 ^ theta_result,
        w4 ^ theta_result
    ]

def affine_layer(state: list[int], alfa: int) -> list[int]:
    r1, r2, r3, i_values, j_values, l_values = rotation_amount(alfa)

    w0, w1, w2, w3, w4 = state

    w0, w1, w2, w3, w4 = column_parity_mixer([w0, w1, w2, w3, w4], r1[0], r2[0], r3[0])
    
    w1 = rotl(w1, 5 + i_values[0])
    w2 = rotl(w2, 10 + i_values[1])
    w3 = rotl(w3, 15 + i_values[2])
    w4 = rotl(w4, 20 + i_values[3])
    w0, w1, w2, w3, w4 = column_parity_mixer([w0, w1, w2, w3, w4], r1[1], r2[1], r3[1])

    w1 = rotl(w1, 19 + j_values[0])
    w2 = rotl(w2, 38 + j_values[1])
    w3 = rotl(w3, 57 + j_values[2])
    w4 = rotl(w4, 76 + j_values[3])
    w0, w1, w2, w3, w4 = column_parity_mixer([w0, w1, w2, w3, w4], r1[2], r2[2], r3[2])

    w1 = rotl(w1, 62 + l_values[0])
    w2 = rotl(w2, 124 + l_values[1])
    w3 = rotl(w3, 186 + l_values[2])
    w4 = rotl(w4, 248 + l_values[3])
    w0, w1, w2, w3, w4 = column_parity_mixer([w0, w1, w2, w3, w4], r1[3], r2[3], r3[3])

    return [w0, w1, w2, w3, w4]

def fasta(K: int):
    K &= MASK_329

    state = [
        K, 
        rotl(K, 1),
        rotl(K, 2),
        rotl(K, 3),
        rotl(K, 4),
    ]

    alfas = [0, 1, 2, 3, 4, 5, 6]

    for i in range(6):
        state = affine_layer(state, alfas[i])
        state = non_linear_layer(state)
    state = affine_layer(state, alfas[6])

    keystream = 0
    for i in range(5):
        keystream |= (state[i] ^ K) << (i * 329)

    return keystream



if __name__ == "__main__":
    print(rotl(124, 13))