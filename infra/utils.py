"""Utility functions."""

from typing import Iterable, List, Sequence, Tuple, TypeVar, Union

T = TypeVar("T")
Rotatable = Union[Sequence[T], str]
Indexable = Union[List[T], Union[T], str]


def chunked(items: Sequence[T], n: int) -> Sequence[Sequence[T]]:
    """
    Yield successive n-sized chunks from lst.
    The last chunk is trunkated as needed.

    :param items: A collection of things to be chunked.
    :param n: The size of each chunk.

     >>> list(chunked([1, 2, 3, 4, 5], 2))
     [[1, 2], [3, 4], [5]]
     >>> list(chunked((1, 1, 1, 1, 1), 2))
     ((1), (1), (1))
    """
    # noinspection PyArgumentList
    return type(items)(type(items)(items[i : i + n]) for i in range(0, len(items), n))


def rotate_left(sequence: Rotatable, n: int) -> Rotatable:
    """
    Rotate a sequence to the left.

    :param sequence: The sequence to rotate.
    :param n: The amount of rotation.
    :return: The rotated sequence.

    >>> rotate_left("hello", 2)
    'llohe'
    """
    return sequence[n:] + sequence[:n]


def rotate_right(sequence: Rotatable, n: int) -> Rotatable:
    """
    Rotate a sequence to the right.

    :param sequence: The sequence to rotate.
    :param n: The amount of rotation.
    :return: The rotated sequence.

    >>> rotate_right("hello", 2)
    'lohel'
    """
    return rotate_left(sequence, len(sequence) - n)


def convert_base(value: int, base: int) -> Iterable[int]:
    """
    Express a number with a specific base.

    :param value: The number to be expressed with a different base.
    :param base: The new base.
    :return: The "digits", starting with the lowest exponent.

    >>> tuple(convert_base(0x6, 2))
    (0, 1, 1)
    >>> tuple(convert_base(0xf, 10))
    (5, 1)
    """
    assert base > 0
    while value != 0:
        yield value % base
        value //= base


def split_every(data: Indexable, every: int) -> Tuple[Indexable]:
    """
    Split data into groups of a given maximum length.

    :param data: The data to split.
    :param every: The maximum length of the resulting sequences.
    :return: The split sequences.

    >>> split_every("ABCDE", 2)
    ('AB', 'CD', 'E')
    """
    return tuple(data[every * i : every * (i + 1)] for i in range((len(data) + every - 1) // every))


def get_pairs(n: int) -> Iterable[Tuple[int, int]]:
    """
    Get pairs of indices that are not equal.

    :param n: The range of indices.
    :return: The pairs of non-equal indices.

    >>> tuple(get_pairs(2))
    ((0, 1), (1, 0))
    >>> tuple(get_pairs(3))
    ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
    """
    return ((a, b) for a in range(n) for b in range(n) if a != b)


def inverse_cumulative_sum(values: Sequence[int]) -> Tuple[int, ...]:
    """
    Calculate the differences between adjacent numbers in a sequence.

    :param values: The values.
    :return: The differences

    >>> inverse_cumulative_sum((1, 3, 8))
    (2, 5)
    """
    return tuple(b - a for a, b in zip(values, values[1:]))


def reverse_sequence(count: int) -> Iterable[int]:
    """
    Get a reverse sequence.

    :param count: How many items to get.
    :return: The reverse sequence.

    >>> tuple(reverse_sequence(5))
    (4, 3, 2, 1, 0)
    """
    yield from range(count - 1, -1, -1)
