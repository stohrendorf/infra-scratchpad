"""CCITT2 encoding and decoding functions."""

from typing import Iterable

ccitt2_table = {
    0b00011: ("A", "-"),
    0b11001: ("B", "?"),
    0b01110: ("C", ":"),
    0b01001: ("D", "[who's there?]"),
    0b00001: ("E", "3"),
    0b01101: ("F", "[unused]"),
    0b11010: ("G", "[unused]"),
    0b10100: ("H", "[unused]"),
    0b00110: ("I", "8"),
    0b01011: ("J", "[bell]"),
    0b01111: ("K", "("),
    0b10010: ("L", ")"),
    0b11100: ("M", "."),
    0b01100: ("N", ","),
    0b11000: ("O", "9"),
    0b10110: ("P", "0"),
    0b10111: ("Q", "1"),
    0b01010: ("R", "4"),
    0b00101: ("S", "'"),
    0b10000: ("T", "5"),
    0b00111: ("U", "7"),
    0b11110: ("V", "="),
    0b10011: ("W", "2"),
    0b11101: ("X", "/"),
    0b10101: ("Y", "6"),
    0b10001: ("Z", "+"),
    0b01000: ("\r", "\r"),
    0b00010: ("\n", "\n"),
    0b00100: (" ", " "),
    0b00000: ("[unused]", "[unused]"),
}

ccitt2_table_encode_letters = {letter: code for code, (letter, _) in ccitt2_table.items()}
ccitt2_table_encode_symbols = {symbol: code for code, (_, symbol) in ccitt2_table.items()}
ccitt2_table_decode_letters = {code: letter for code, (letter, _) in ccitt2_table.items()}
ccitt2_table_decode_symbols = {code: symbol for code, (_, symbol) in ccitt2_table.items()}

ccitt2_select_letters = 0b11111
ccitt2_select_symbols = 0b11011


def ccitt2_encode(string: str) -> Iterable[int]:
    """
    Encode a string as CCITT2.

    :param string: The string to encode.
    :return: The encoded data.

    >>> list(map(bin, ccitt2_encode("A:")))
    ['0b11', '0b11011', '0b1110']
    """
    mode_letters = True
    current_table = ccitt2_table_encode_letters
    for char in string:
        current = current_table.get(char)
        if current is None:
            current_table = ccitt2_table_encode_symbols if mode_letters else ccitt2_table_encode_letters
            mode_letters = not mode_letters
            current = current_table[char]
            yield ccitt2_select_letters if mode_letters else ccitt2_select_symbols
        yield current


def ccitt2_decode(encoded: Iterable[int]) -> str:
    """
    Decode a CCITT2 encoded string.

    :param encoded: The encoded string.
    :return: The decoded string.

    >>> ccitt2_decode((0b00011, 0b11011, 0b01110))
    'A:'
    """
    current_table = ccitt2_table_decode_letters

    decoded = ""
    for value in encoded:
        if value == ccitt2_select_letters:
            current_table = ccitt2_table_decode_letters
            continue
        elif value == ccitt2_select_symbols:
            current_table = ccitt2_table_decode_symbols
            continue
        current = current_table[value]
        decoded += current

    return decoded
