"""The solution of https://stalburg.net/Bunker_computer_code."""

from typing import Dict, Tuple

from infra.ciphers.transposition import transposed
from other.body_message import body_code

bunker_computer_code_1 = (
    ("Underground", "Trees", "Lead", "Message"),
    ("Knowledge", "Research", "Body", "Question"),
    ("UGU", "Us", "Diving", "People"),
    ("Raven", "Tunnel", "Open", "Machine"),
    ("Inventor", "Homeless", "Omitted", "Mask"),
    ("Suit", "Institute", "Right", "Man"),
    ("God", "Show", "Truth", "Mines"),
    ("Organization", "AH", "Guard", "City"),
    ("Death", "Legend", "Meaning", "Sewer"),
    ("Green", "Blue", "Water", "World"),
)

bunker_computer_code_2 = (
    "C3.1",
    "F1.2",
    "F4.1",
    "B2.1",
    "A3.2",
    "E4.2",
    "F4.2",
    "G2.6",
    "G3.2",
    "A3.2",
    "G1.5",
    "F1.1",
    "F4.1",
    "G3.3",
    "G3.4",
    "B2.1",
    "G1.4",
    "B2.3",
    "G2.4",
    "H4.5",
)

# This is the patched solution with A3.2=C
bunker_computer_code_2_solution = "WHATCONNECTSALLTHESE"

bunker_computer_code_3 = (
    (
        (
            "1.3",
            "1.1",
            "4.10",
            "1.7",
            "4.7",
        ),
        (
            "1.5",
            "2.8",
            "2.5",
            "4.3",
            "4.4",
        ),
    ),
    (
        (
            "4.5",
            "4.6",
            "2.4",
            "3.8",
            "1.2",
        ),
        (
            "3.2",
            "4.1",
            "4.2",
            "2.7",
            "3.7",
        ),
    ),
    (
        (
            "1.4",
            "2.2",
            "2.6",
            "3.1",
            "1.8",
        ),
        (
            "1.10",
            "1.9",
            "2.10",
            "3.6",
            "3.9",
        ),
    ),
    (
        (
            "3.10",
            "2.1",
            "3.3",
            "1.6",
            "2.9",
        ),
        (
            "4.8",
            "2.4",
            "4.9",
            "2.3",
            "3.5",
        ),
    ),
)


def _decrypt_bunker_computer_code_2() -> str:
    def decrypt_letter(code: str) -> str:
        body_code_key, letter = code.split(".")
        try:
            return body_code[body_code_key][int(letter) - 1]
        except KeyError:
            return f"[{code}]"

    return "".join(decrypt_letter(code) for code in bunker_computer_code_2)


bunker_computer_code_2_solution_unpatched = _decrypt_bunker_computer_code_2()


def _count_usages(data: Tuple[Tuple[str, ...], ...]) -> Dict[str, int]:
    result = {f"{x + 1}.{y + 1}": 0 for y, y_data in enumerate(data) for x in range(len(y_data))}
    for row in bunker_computer_code_3:
        for column in row:
            for code in column:
                result[code] += 1

    return result


def _print_non_unique_code_usage_part_3():
    for code, usage_count in _count_usages(bunker_computer_code_1).items():
        if usage_count != 1:
            column, row = code.split(".")
            print(code, bunker_computer_code_1[int(row) - 1][int(column) - 1], usage_count)


if __name__ == "__main__":
    print(_decrypt_bunker_computer_code_2())
    _print_non_unique_code_usage_part_3()
    for column in transposed(bunker_computer_code_1):
        print("".join(word[0] for word in column))

    def _get_word(co: str):
        x, y = co.split(".")
        return bunker_computer_code_1[int(y) - 1][int(x) - 1]

    for row in bunker_computer_code_3:
        for column in row:
            print(" ".join(map(_get_word, column)))
