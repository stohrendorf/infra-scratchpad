"""
Stuff related to https://stalburg.net/Letter_box
"""

from typing import Tuple, Dict

from utils import find_string

rag_data = {
    "G3": "EQGREIHYEWHKUTOPKTTHISNOBER",
    "G4": "BXRAPRLGGBDJETEAUEVQIYSNEGE",
    "G5": "UHXTEMGLJFQTMPKRLSFERGEJROD",
    "G6": "AZOZRISVUHRYEROTEEISLSONG4O",
    "G7": "WPMPKUCYRMOYYWCOXHABIVKUUFD",
    "G8": "UJYAEDHYEQITWNQKPYTEAWEJSHG",
    "G9": "OBVNLSBYSRTNIESHTDHOTRMILYS",
    "YT": "LGJVZUNTTISRAGHTPEWDNLAPAWM",
    "XT": "DMYFUDKINHTYXOPOYBÖÄÅPFHSRE",
}


def print_string_code(string: str):
    print(f"{string=}")
    for char, codes in find_string(rag_data, string):
        code_str = ", ".join(f"{row}:{col}" for row, col in codes)
        print(char, code_str)


def print_rag(data: Dict[str, str]):
    for key, values in data.items():
        print(key, values)


def decode(data: Dict[str, str], *coords: Tuple[int, int, int]) -> str:
    """
    The decryption algorithm used in https://stalburg.net/Letter_box.
    :param data: The reference dictionary.
    :param coords: A list of tuples containing the =, X and Y coordinates.
    :return: The decoded string, with unknown values replaced with a "?".
    """
    decoded = {
        idx - 1: data[f"G{row}"][col - 1] if f"G{row}" in data else "?"
        for idx, col, row in coords
    }
    max_idx = max(co[0] - 1 for co in coords)
    result = ""
    for i in range(max_idx + 1):
        if i not in decoded:
            result += "?"
        else:
            result += decoded[i]
    return result


def solve_g1_g2_g3(data: Dict[str, str]):
    print("G1", decode(data, (1, 3, 4), (2, 6, 6), (3, 7, 5), (4, 10, 6), (5, 12, 8)))
    print("G2", decode(data, (1, 4, 7), (2, 9, 3), (4, 7, 6), (5, 11, 7), (6, 4, 9)))
    print("G3", decode(data, (2, 5, 3), (1, 4, 5), (3, 7, 4), (4, 8, 5)))


if __name__ == "__main__":
    solve_g1_g2_g3(rag_data)
