

# constants
MASK_329 = (1 << 329) - 1

def rotl(val: int, shift: int) -> int:
    """left rotation of 329 bits"""
    shift %= 329
    return ((val << shift) | (val >> (329 - shift))) & MASK_329

if __name__ == "__main__":
    print(rotl(124, 13))