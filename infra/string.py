from typing import Iterable


def all_string_indices(haystack: str, needle: str) -> Iterable[int]:
    """
    Finds all indices of a given needle in a haystack.
    :return: An iterable of the found indices.

    >>> list(all_string_indices("ABA", "A"))
    [0, 2]
    """
    start = -1
    while True:
        try:
            start = haystack.index(needle, start + 1)
            yield start
        except ValueError:
            break


def char_idx(char: str) -> int:
    """
    The index of an uppercase character.
    :param char: The input character.
    :return: The index.

    >>> char_idx("A"), char_idx("B")
    (1, 2)
    """
    assert len(char) == 1
    return ord(char) - ord("A") + 1


def insert_spaces(string: str, every: int) -> str:
    """
    Insert spaces at regular intervals.
    :param string: The string to insert the spaces into.
    :param every: The interval to insert spaces at.

    >>> insert_spaces("ABCDEFGH", 3)
    'ABC DEF GH'
    """
    return " ".join(
        string[every * i : every * (i + 1)]
        for i in range((len(string) + every - 1) // every)
    )
