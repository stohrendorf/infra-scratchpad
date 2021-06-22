"""Transposition cipher function."""

from typing import Tuple

from infra.string import all_string_indices


def get_encoding_mapping(key: str) -> Tuple[int]:
    """
    Compute the encoding mapping for columnar transposition ciphers.

    :param key: The encoding key.
    :return: The column indices resulting from the encoding key.

    >>> get_encoding_mapping("ALBERT")
    (0, 2, 3, 1, 4, 5)
    """
    key_chars = sorted(set(key))
    return tuple(src_idx for key_char in key_chars for src_idx in all_string_indices(key, key_char))


def columnar_encode(plaintext: str, key: str) -> str:
    """
    Encode a string with a columnar transposition cipher.

    :param plaintext: The plaintext to be encoded.
    :param key: The encoding key.
    :return: The encoded text.

    >>> columnar_encode("HELLOWORLD", "ALBERTHART")
    'HRLLOEOLWD'
    """
    assert len(plaintext) == len(key)
    return "".join(plaintext[src_idx] for src_idx in get_encoding_mapping(key))


def columnar_decode(encoded: str, key: str) -> str:
    """
    Decode a string with a columnar transposition cipher.

    :param encoded: The encoded text to be decoded.
    :param key: The encoding key.
    :return: The decoded text.

    >>> columnar_decode("HRLLOEOLWD", "ALBERTHART")
    'HELLOWORLD'
    """
    assert len(encoded) == len(key)
    decoding_mapping = tuple(
        dst for dst, _ in sorted(enumerate(get_encoding_mapping(key)), key=lambda dst_src: dst_src[1])
    )
    return "".join(encoded[src_idx] for src_idx in decoding_mapping)


assert columnar_decode(columnar_encode("ABCDEF", "HELLOW"), "HELLOW") == "ABCDEF"
