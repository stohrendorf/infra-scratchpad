from infra.binary import binary_decode_multi

keypad_003 = (
    "01001110 01001111 01010100",
    "01001000 01001001 01001110",
    "01000111 00100000 01001000",
    "01000101 01010010 01000101",
    "00100000 01011001 01000101",
    "01010100",
)

if __name__ == "__main__":
    for entry in keypad_003:
        print(binary_decode_multi(entry))
