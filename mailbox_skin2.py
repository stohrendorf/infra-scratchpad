from utils import binary_decode_multi, insert_spaces

if __name__ == "__main__":
    print(
        binary_decode_multi(
            insert_spaces("0111010001101000011001010010000001110100", 8)
        )
    )
    print(
        binary_decode_multi(
            insert_spaces("0111001001110101011101000110100000100000", 8)
        )
    )
    print(
        binary_decode_multi(
            insert_spaces("0110100101110011001000000110100101101110", 8)
        )
    )
    print(
        binary_decode_multi(
            insert_spaces("0010000001110100011101010110111001101110", 8)
        )
    )
    print(binary_decode_multi(insert_spaces("011001010110110001110011", 8)))
    print()
    print(
        binary_decode_multi(
            insert_spaces("0101001001101111011000100110100101101110", 8)
        )
    )
