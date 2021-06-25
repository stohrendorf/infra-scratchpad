"""String-related utility functions."""

from typing import Iterable, Optional, Tuple

from infra.nla import alphabet_fi
from infra.utils import split_every


def all_string_indices(haystack: str, needle: str) -> Iterable[int]:
    """
    Find all indices of a given needle in a haystack.

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


def char_idx(char: str) -> Optional[int]:
    """
    Get the index of an uppercase character.

    :param char: The input character.
    :return: The index.

    >>> char_idx("A"), char_idx("B"), char_idx("Ä"), char_idx("-")
    (0, 1, 27, None)
    """
    assert len(char) == 1
    try:
        return alphabet_fi.index(char)
    except ValueError:
        return None


def insert_spaces(string: str, every: int) -> str:
    """
    Insert spaces at regular intervals.

    :param string: The string to insert the spaces into.
    :param every: The interval to insert spaces at.

    >>> insert_spaces("ABCDEFGH", 3)
    'ABC DEF GH'
    """
    return " ".join(split_every(string, every))


def kasiski_positions(text: str, length: int = 2) -> Iterable[Tuple[str, Tuple[int, ...]]]:
    """
    Find all indices for all n-grams in a string if they occur more than once.

    :param text: The string to analyze.
    :param length: The length of the n-gram.
    :return: An iterable of (n-gram, indices) tuples.

    >>> tuple(kasiski_positions("HELLLLHEHE"))
    (('HE', (0, 6, 8)), ('LL', (2, 3, 4)))
    """
    assert length >= 2

    checked = set()
    for i in range(len(text) + 1 - length):
        ngram = text[i : i + length]
        if ngram in checked:
            continue
        checked.add(ngram)

        indices = tuple(all_string_indices(text, ngram))
        if len(indices) > 1:
            yield ngram, indices
