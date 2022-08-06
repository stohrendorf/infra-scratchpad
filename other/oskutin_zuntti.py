"""Random riddles posted on discord which are not present in INFRA itself."""

from infra.encodings.binary import binary_decode, invert_bits
from infra.output import section
from infra.utils import convert_base


def _riddle1(s: section):
    code = "37DB 5069 64F8 6C 3076A3 1 A-XB2"
    value, _ = code.split("-")
    decoded_value = int(value.replace(" ", ""), 16) // 0xB2
    decoded_string = "".join(chr(char) for char in convert_base(decoded_value, 0x100))[::-1]
    s.print(decoded_string)


def _riddle2(s: section):
    code = (
        "10101100 10110001 10101000 1110101 10001011 10001101 10001010 10001011 10010111 1110101 10011100 10011110"
        " 10001111 10010110 10001011 10011110 10010011 1110101 10001100 10001010 10011101 10001011 10011010 10001101"
        " 10001101 10011110 10010001 10011010 10011110 10010001 1110101 10001101 10011010 10011011 10010000 10001010"
        " 10011101 10001011 1110101 10001110 10001010 10011110 10001101 10001101 10000110"
    )
    # for whatever reason, the encoded \n's are missing a leading 1
    s.print("".join(chr(0xFF ^ int(byte.rjust(8, "1"), 2)) for byte in code.split()))


def _riddle3(s: section):
    code = "00100000F 00100000O 01010010Ö G11011110 01011000A P10101000 00111101K"
    patched_code = tuple(word if word[0] in ("0", "1") else invert_bits(word[1:]) + word[0] for word in code.split())
    ordered_code = sorted(patched_code, key=lambda word: word[-1])
    decoded = "".join(binary_decode(word[:-1]) for word in ordered_code)
    s.print(decoded)


if __name__ == "__main__":
    with section("riddle 1") as s:
        _riddle1(s)
        s.print()

    with section("riddle 2") as s:
        _riddle2(s)
        s.print()

    with section("riddle 3") as s:
        _riddle3(s)
        s.print()
