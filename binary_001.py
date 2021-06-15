from utils import binary_decode_multi, rotate_right

# these are the first 7 columns, as they repeat over the whole texture
binary_001 = (
    "01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101",
    "01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101 01001111",
    "01000101 01001111 01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100",
    "01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101 01010010 00100000",
    "01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101",
    "01001111 01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101",
    "01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100",
)

binary_001_input = "OTHER SIDE"

if __name__ == "__main__":
    all_decoded = tuple(map(binary_decode_multi, binary_001))

    for column in all_decoded:
        print(column)

    print()

    print("amount of right rotations from previous column")
    print(all_decoded[0])
    for prev, current in zip(all_decoded, all_decoded[1:] + all_decoded[:1]):
        assert len(prev) == len(current)
        for i in range(len(prev) + 1):
            if rotate_right(prev, i) == current:
                print(current, i)
                break
        else:
            raise RuntimeError
