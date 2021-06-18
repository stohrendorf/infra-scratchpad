from infra.binary import binary_decode_multi
from infra.string import insert_spaces

mailbox_skin2 = (
    "0111010001101000011001010010000001110100",
    "0111001001110101011101000110100000100000",
    "0110100101110011001000000110100101101110",
    "0010000001110100011101010110111001101110",
    "011001010110110001110011",
    "",
    "0101001001101111011000100110100101101110",
)

if __name__ == "__main__":
    for entry in mailbox_skin2:
        print(binary_decode_multi(insert_spaces(entry, 8)))