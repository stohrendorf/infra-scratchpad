"""Stuff related to https://stalburg.net/Letter_box."""

from typing import Dict, Iterable, Sequence, Tuple

from infra.dict import find_string_chars
from infra.output import section

scientific_table_001_skin3 = {
    # G3 is G0 in the texture, it's different here to avoid special handling with coordinates
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


def _print_string_code(string: str):
    print(f"{string=}")
    for char, codes in find_string_chars(scientific_table_001_skin3, string):
        code_str = ", ".join(f"{row}:{col}" for row, col in codes)
        print(char, code_str)


def _print_rag(data: Dict[str, str]):
    for key, values in data.items():
        print(key, values)


def decode(data: Dict[str, str], *coords: Tuple[int, int, int]) -> str:
    """
    Decrypt using the algorithm described in https://stalburg.net/Letter_box.

    :param data: The reference dictionary.
    :param coords: A list of tuples containing the =, X and Y coordinates.
    :return: The decoded string, with unknown values replaced with a "?".
    """
    decoded = {idx - 1: data[f"G{row}"][col - 1] if f"G{row}" in data else "?" for idx, col, row in coords}
    max_idx = max(co[0] for co in coords)
    result = ""
    for i in range(max_idx):
        if i not in decoded:
            result += "?"
        else:
            result += decoded[i]
    return result


def solve_g1_g2_g3() -> Dict[str, str]:
    """
    Solve G1 to G3 of the body message.

    :return: The solved codes G1 to G3.
    """

    def decode_reference(reference: Sequence[str]) -> Iterable[Tuple[int, int, int]]:
        assert len(reference) % 5 == 0
        for i in range(0, len(reference), 5):
            x, y, index, x_co, y_co = reference[i : i + 5]
            if x == "Y":
                x, y = y, x
                x_co, y_co = y_co, x_co

            assert (x, y) == ("X", "Y")

            yield int(index), int(x_co), int(y_co)

    g1 = "X,Y,1,3,4,X,Y,2,6,6,Y,X,3,5,7,X,Y,4,10,6,X,Y,5,12,8".split(",")
    g2 = "X,Y,1,4,7,X,Y,2,9,3,X,Y,4,7,6,X,Y,5,11,7,X,Y,6,4,9".split(",")
    g3 = "X,Y,2,5,3,X,Y,1,4,5,X,Y,3,7,4,X,Y,4,8,5".split(",")

    return {
        "G1": decode(scientific_table_001_skin3, *decode_reference(g1)),
        "G2": decode(scientific_table_001_skin3, *decode_reference(g2)),
        "G3": decode(scientific_table_001_skin3, *decode_reference(g3)),
    }


if __name__ == "__main__":
    with section("scientific_table_001_skin3 solution") as s:
        for key, value in solve_g1_g2_g3().items():
            s.print(f"{key} {value}")
