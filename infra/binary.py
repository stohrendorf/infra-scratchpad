from typing import Iterable


def binary_decode(binary: str) -> str:
    """
    Decodes an 8-bit binary number.
    :param binary: A binary string.
    :return: The character representation.

    >>> binary_decode("01010011")
    'S'
    """
    assert len(binary) == 8 and all(c in ("0", "1") for c in binary)
    return chr(int(binary, 2))


def binary_decode_multi(words: str) -> str:
    """
    Decodes a string of binary codes.
    :param words: The binary codes.
    :return: The decoded string.

    >>> binary_decode_multi("01010011 01101111")
    'So'
    """
    return "".join(map(binary_decode, words.split()))


def invert_bits(binary: str) -> str:
    assert all(c in ("0", "1") for c in binary)
    return "".join(str(1 - int(c)) for c in binary)


def binary_encode(string: str) -> Iterable[str]:
    for c in map(ord, string):
        yield "".join(str((c >> (7 - i)) & 1) for i in range(8))
