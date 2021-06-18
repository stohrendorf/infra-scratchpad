from typing import Dict, Iterable, Tuple, TypeVar, List

from infra.string import all_string_indices
from infra.utils import Rotatable, rotate_left

TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


def find_char(data: Dict[TKey, str], char: str) -> Iterable[Tuple[TKey, int]]:
    """
    Finds all indices of a given char in a dictionary of strings.
    :param data: The dictionary to search in.
    :param char: The char to search for.
    :return: An iterable of tuples containing the dictionary key and the indices of the char in the corresponding dictionary values.

    >>> list(find_char({"A": "BC"}, "C"))
    [('A', 2)]
    """

    assert len(char) == 1
    for key, values in data.items():
        for index in all_string_indices(values, char):
            yield key, index + 1


def find_string_chars(
    data: Dict[TKey, str], string: str
) -> List[Tuple[str, List[Tuple[TKey, int]]]]:
    """
    Finds all dictionary coordinates of the given string chars.
    :param data: The dictionary to search in.
    :param string: The string containing the chars to search for.
    :return: A list of tuples, each tuple containing the char and the corresponding list of coordinates.

    >>> list(find_string_chars({"A": "BC"}, "CD"))
    [('C', [('A', 2)]), ('D', [])]
    """
    return [(char, list(find_char(data, char))) for char in string]


def swap_values(data: Dict[TKey, TValue], a: TKey, b: TKey):
    """
    Swaps the values in a dictionary.
    :param data: The dictionary to modify.
    :param a: The first key to swap.
    :param b: The second key to swap.

    >>> data = {"A": "B", "C": "D"}
    >>> swap_values(data, "A", "C")
    >>> data
    {'A': 'D', 'C': 'B'}
    """
    data[a], data[b] = data[b], data[a]


def rotate_column(data: Dict[TKey, Rotatable], column: int, n: int):
    """
    Rotates a column in a dictionary.
    :param data: The dictionary.
    :param column: The column to rotate.
    :param n: The amount of rotation.

    >>> data = {1: "A", 2: "B", 3: "C"}
    >>> rotate_column(data, 0, 1)
    >>> data
    {1: 'C', 2: 'A', 3: 'B'}
    """
    keys = list(data.keys())
    for _ in range(n):
        prev = data[keys[-1]][column]
        for key in keys:
            s = data[key]
            current = s[column]
            data[key] = s[:column] + prev + s[column + 1 :]
            prev = current


def rotate_value_left(data: Dict[TKey, Rotatable], key: TKey, n: int):
    """
    Rotates a value in a dictionary.
    :param data: The dictionary to modify.
    :param key: The key to rotate the value of.
    :param n: The amount of rotation

    >>> data = {"A": "BCDE"}
    >>> rotate_value_left(data, "A", 1)
    >>> data
    {'A': 'CDEB'}
    """
    data[key] = rotate_left(data[key], n)


def swap_columns(data: Dict[TKey, Rotatable], a: int, b: int):
    """
    Swap two columns of a dictionary.
    :param data: The dictionary to modify.
    :param a: The first column.
    :param b: The second column.

    >>> data = {"A": "BC", "D": "EF"}
    >>> swap_columns(data, 0, 1)
    >>> data
    {'A': 'CB', 'D': 'FE'}
    """
    for key, values in data.items():
        ac = values[a]
        bc = values[b]
        s = values
        s = s[:a] + bc + s[a + 1 :]
        s = s[:b] + ac + s[b + 1 :]
        data[key] = s
