"""Transposition cipher function."""

from typing import List, Sequence, Tuple, TypeVar, Union

from infra.string import all_string_indices, split_every


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


T = TypeVar("T")
IndexableT = Union[List[T], Union[T], str]


def columnar_encode_shuffle(data: IndexableT, key: str) -> IndexableT:
    """
    Shuffle data with a columnar transposition cipher.

    :param data: The data to be shuffled.
    :param key: The encoding key.
    :return: The shuffled data.

    >>> "".join(columnar_encode_shuffle("HELLOWORLD", "ALBERTHART"))
    'HRLLOEOLWD'
    """
    assert len(data) == len(key)
    return [data[src_idx] for src_idx in get_encoding_mapping(key)]


def columnar_encode(plaintext: str, key: str, null_char: str = "") -> str:
    """
    Apply a columnar transposition cipher.

    :param plaintext: The text to be encoded.
    :param key: The encoding key.
    :param null_char: The null char for irregular texts.
    :return: The encoded string.

    >>> columnar_encode("this is a test", "somekey")
    'stis ei hat st'
    """
    assert len(null_char) in (0, 1)

    def prepare_row(row: str) -> str:
        adjusted_row = row if not null_char else row.ljust(len(key), null_char)
        return columnar_encode_shuffle(adjusted_row, key[: len(adjusted_row)])

    rows = [prepare_row(row) for row in split_every(plaintext, len(key))]
    return "".join(row[i] for i in range(len(key)) for row in rows if i < len(row))


def columnar_decode_shuffle(data: IndexableT, key: str) -> IndexableT:
    """
    Shuffle data with a columnar transposition cipher.

    :param data: The encoded data to be shuffled.
    :param key: The encoding key.
    :return: The shuffled data.

    >>> "".join(columnar_decode_shuffle("HRLLOEOLWD", "ALBERTHART"))
    'HELLOWORLD'
    """
    assert len(data) == len(key)
    decoding_mapping = tuple(
        dst for dst, _ in sorted(enumerate(get_encoding_mapping(key)), key=lambda dst_src: dst_src[1])
    )
    return [data[src_idx] for src_idx in decoding_mapping]


def columnar_decode(encoded: str, key: str) -> str:
    """
    Apply a columnar transposition cipher for deciphering.

    :param encoded: The text to be decoded.
    :param key: The encoding key.
    :return: The decoded string.

    >>> columnar_decode("stis ei hat st", "somekey")
    'this is a test'
    """
    split_data = split_every(encoded, (len(encoded) + len(key) - 1) // len(key))
    columns = columnar_decode_shuffle(split_data, key[: min(len(key), len(split_data))])
    rows = max(len(column) for column in columns)
    return "".join(column[i] for i in range(rows) for column in columns if i < len(column))


def transpose(strings: Sequence[str]) -> Tuple[str, ...]:
    """
    Transpose a list of strings.

    :param strings: The strings to transpose.
    :return: The transposed strings.

    >>> transpose(("HELLO", "WORLD"))
    ('HW', 'EO', 'LR', 'LL', 'OD')
    """
    if not strings:
        return ()

    first_length = len(strings[0])
    assert all(first_length == len(s) for s in strings)

    return tuple("".join(column[x] for column in strings) for x in range(first_length))
