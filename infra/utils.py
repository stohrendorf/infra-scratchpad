"""Utility functions."""

from typing import Iterable, Sequence, TypeVar, Union

T = TypeVar("T")
Rotatable = Union[Sequence[T], str]


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
